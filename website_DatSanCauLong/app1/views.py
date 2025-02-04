from django.shortcuts import render
from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, decorators
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .forms import *
from django.db.models import Q
from .utils import send_otp_email, generate_otp
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse

import json


from .forms import TimeSlotTemplateForm

# Create your views here.   

# HÀM KIỂM TRA MÃ OTP ĐỂ TÁI SỬ DỤNG:
# GỬI OTP KHI NGƯỜI DÙNG YÊU CẦU
def handle_send_otp(request, form_input):
    if form_input.is_valid():
        username = form_input.cleaned_data['username']
        otp = generate_otp()
        request.session['otp'] = otp  # Lưu OTP vào session
        request.session['username'] = username  # Lưu username
        request.session['otp_created_at'] = timezone.now().isoformat()  # Lưu thời gian tạo OTP
        send_otp_email(username, otp)
        

def TrangChu_guest(request):
    return render(request, 'app1/TrangChu-guest.html')

def TrangChu_customer(request):
    return render(request, 'app1/TrangChu-customer.html')

def header_guest(request):
    return render(request, 'app1/Header-guest.html')

def header_customer(request):
    return render(request, 'app1/Header-customer.html')

def menu(request):
    return render(request, 'app1/Menu.html')

def menu_manager(request):
    return render(request, 'app1/Menu-manager.html')

def footer(request):
    return render(request, 'app1/Footer.html')

class Sign_Up(View):
    def get(self, request):
        sign_up = SignUpForm()
        context = {'SignUp': sign_up}
        return render(request, 'app1/Sign_up.html', context)
    
    
    def post(self, request):
        print('post')
        sign_up = SignUpForm(request.POST, initial={'otp': request.session.get('otp')})
        context = {'SignUp': sign_up}
        
        # trả về lỗi nếu nhập sai
        if not sign_up.is_valid():
            return render(request, 'app1/Sign_up.html', context)

        # Nếu form hợp lệ, lưu thông tin tạm thời vào session
        username = sign_up.cleaned_data['username']
        full_name = sign_up.cleaned_data['full_name']
        password = sign_up.cleaned_data['password']
        
        request.session['username'] = username
        request.session['full_name'] = full_name
        request.session['password'] = password

        # Gửi OTP sau khi form hợp lệ
        handle_send_otp(request, sign_up)

        context['action'] = 'SIGN_UP'  

        return render(request, 'app1/Enter_OTP.html', context)
    
# Trang nhập mã OTP   
def trangOTP(request):
    
    return render(request, 'app1/Enter_OTP.html')

#  hàm tạo User
def create_user_account(username, full_name, password):
    try:
        # Tạo đối tượng User trong database
        user = User.objects.create_user(username=username, first_name=full_name, password=password)
        user.save()
        return user
    except Exception:
        return None

def validate_otp(request):
   
    otp_session = request.session.get("otp")
    otp_created_at = request.session.get("otp_created_at")

    if not otp_session or not otp_created_at:
        return {"valid": False, "message": "Mã OTP không tồn tại hoặc đã hết hạn."}

    # Kiểm tra thời gian hết hạn của OTP
    otp_created_at = timezone.datetime.fromisoformat(otp_created_at)
    if timezone.now() > otp_created_at + timedelta(minutes=1):
        return {"valid": False, "message": "Mã OTP đã hết hiệu lực. Vui lòng thử lại."}

    return {"valid": True, "otp_session": otp_session}

# Hàm validate OTP và đăng kí user
def validate_otp_and_register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        otp_input = data.get("otp")

        # Kiểm tra mã OTP bằng hàm validate_otp
        otp_validation = validate_otp(request)
        if not otp_validation["valid"]:
            return JsonResponse({"success": False, "message": otp_validation["message"]})

        # So sánh mã OTP người dùng nhập
        if otp_input == otp_validation["otp_session"]:
            # Đăng ký tài khoản (chỉ thực hiện khi OTP đúng)
            username = request.session.get("username")
            full_name = request.session.get("full_name")
            password = request.session.get("password")

            if username and password:
                # Gọi hàm tạo người dùng
                user = create_user_account(username, full_name, password)

                if user:
                    # Xóa thông tin OTP khỏi session
                    request.session.pop("otp", None)
                    request.session.pop("otp_created_at", None)
                    request.session.pop("username", None)
                    request.session.pop("full_name", None)
                    request.session.pop("password", None)

                return JsonResponse({"success": True, "message": "Đăng ký thành công!"})
            return JsonResponse({"success": False, "message": "Lỗi trong quá trình đăng ký tài khoản."})
        else:
            return JsonResponse({"success": False, "message": "Mã OTP không chính xác."})

    return JsonResponse({"success": False, "message": "Yêu cầu không hợp lệ."})


# hàm gửi lại mã OTP:
def resend_otp(request):
    if request.method == "POST":
        # Lấy thông tin từ session
        username = request.session.get('username')
        if not username:
            return JsonResponse({'success': False, 'message': 'Không tìm thấy thông tin người dùng. Vui lòng thử lại.'})

        # Tạo mã OTP mới
        otp = generate_otp()
        request.session['otp'] = otp  # Cập nhật OTP mới vào session
        request.session['otp_created_at'] = timezone.now().isoformat()  # Cập nhật thời gian tạo OTP

        # Gửi email
        send_otp_email(username, otp)

        return JsonResponse({'success': True, 'message': 'Mã OTP đã được gửi lại thành công.'})

    return JsonResponse({'success': False, 'message': 'Yêu cầu không hợp lệ.'})


class Sign_In(View):
    def get(self, request):
        # Kiểm tra xem cookie có lưu email không
        remembered_email = request.COOKIES.get('remembered_email', '')
        sign_in = SignInForm(initial={'username': remembered_email})
        context = {'SignIn': sign_in, 'remember_me': bool(remembered_email)}
        return render(request, 'app1/Sign_in.html', context)

    def post(self, request):
        sign_in = SignInForm(request.POST)
        context = {'SignIn': sign_in}
        
        if not sign_in.is_valid():
            return render(request, 'app1/Sign_in.html', context)

        username = sign_in.cleaned_data['username']
        password = sign_in.cleaned_data['password']
        remember_me = request.POST.get('remember_me')  # Lấy giá trị checkbox "Nhớ tài khoản"
        
        # Xác thực người dùng
        try:
            user = User.objects.get(username=username)
            user = authenticate(username=user.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            response = redirect('TrangChu')
            
            # Lưu username vào cookie nếu chọn "Nhớ tài khoản"
            if remember_me:
                response.set_cookie('remembered_email', username, max_age=7 * 24 * 60 * 60)  # Lưu trong 7 ngày
            else:
                response.delete_cookie('remembered_email')  # Xóa cookie nếu không chọn
            
            return response
        else:
            sign_in.add_error('username', "Email hoặc mật khẩu không đúng.")
            return render(request, 'app1/Sign_in.html', context)

# Quên mật khẩu
class ForgotPassword(View):
    def get(self,request):
        forgot_password=ForgotPasswordForm()
        context = {'Forgot_Password_Form': forgot_password}
        return render(request, 'app1/Forgot_password.html', context)
    
    def post(self, request):
        forgot_password=ForgotPasswordForm(request.POST)
        context = {'Forgot_Password_Form': forgot_password}

        if not forgot_password.is_valid():
            return render(request, 'app1/Forgot_password.html', context)
        
        # Nếu form hợp lệ, lưu thông tin tạm thời vào session
        username = forgot_password.cleaned_data['username']
        request.session['username'] = username
        # Gửi OTP sau khi form hợp lệ
        handle_send_otp(request, forgot_password)

        context['action'] = 'FORGOT_PASSWORD'  

        return render(request, 'app1/Enter_OTP.html', context)

# Hàm validate OTP của quên mật khẩu
def validate_otp_of_ForgotPassword(request):
    if request.method == "POST":
        data = json.loads(request.body)
        otp_input = data.get("otp")

        # Kiểm tra mã OTP bằng hàm validate_otp
        otp_validation = validate_otp(request)
        if not otp_validation["valid"]:
            return JsonResponse({"success": False, "message": otp_validation["message"]})  

        # So sánh mã OTP người dùng nhập
        if otp_input == otp_validation["otp_session"]:
            return JsonResponse({"success": True, "message": "Mã OTP chính xác"})
        else:
            return JsonResponse({"success": False, "message": "Mã OTP không chính xác"})
    
    return JsonResponse({"success": False, "message": "Yêu cầu không hợp lệ."})

# Đổi mật khẩu mới:
class New_password(View):
    def get(self,request):
        New_password = NewPasswordForm() 
        context = {'New_Password_Form': New_password}  
        return render(request, 'app1/New_password.html',context)
    
    def post(self, request):
        New_password = NewPasswordForm(request.POST) 
        context = {'New_Password_Form': New_password}  

        if not New_password.is_valid():
            return render(request, 'app1/New_password.html', context)
        
        username = request.session.get('username')
        
        # lấy mật khẩu mới của người dùng
        new_password = New_password.cleaned_data['new_password']
        # cập nhật mật khẩu mới
        user = User.objects.get(username = username)
       
        user.password = make_password(new_password)
        
        user.save()
        messages.success(request, "Đổi mật khẩu thành công!")
        return redirect('Sign_in')
def History(request):
    return render(request, 'app1/LichSuDatSan.html')

def fee_guest(request):
    return render(request, 'app1/fee-guest.html')

def fee_customer(request):
    return render(request, 'app1/fee_customer.html')

def san_guest(request):
    return render(request, 'app1/San-guest.html')

def san_customer(request):
    return render(request, 'app1/San-customer.html')

def bao_cao(request):
    return render(request, 'app1/BaoCaoDoanhThu.html')

def checkin(request):
    return render(request, 'app1/Chek-in.html')

def dangky(request):
    return render(request, 'app1/DangKiTaiKhoanThanhToan.html')

def lichThiDau(request):
    return render(request, 'app1/LichThiDau.html')

def themSan(request):
    return render(request, 'app1/ThemSanMoi.html')

def booking(request):
    return render(request, 'app1/Book.html')

def payment(request):
    return render(request, 'app1/payment.html')

def manager_taikhoan(request):
    return render(request, 'app1/QuanLyTaiKhoan.html')

def manager_san(request):
    return render(request, 'app1/QuanLyThongTinSan.html')

# def court_badminton(request):
#     get_court = CourtBadminton.objects.all()
#     context = {'courts': get_court}
#     return render(request, 'QuanLiUser/courtbadminton.html', context)

# @decorators.login_required(login_url='login')
# def history_booking(request):
   
#     get_history = CourtBooking.objects.all()
#     context = {'historys': get_history}
#     return render(request,'QuanLiUser/historybooking.html', context)

# def search_court(request):
#     query = request.GET.get('search_court')
#     results = []
#     if query:
#         results = CourtBadminton.objects.filter(court_name__icontains = query)
#     return render(request, 'QuanLiUser/kq_tim_kiem.html.html', {'query': query, 'results': results})

# def search_court_two(request):
#     data = CourtBadminton.objects.values_list('court_name','location','price_per_house')
#     courts, locations, prices = zip(*data)
#     return render(request, 'QuanLiUser/search_court2.html', {'courts': courts, 'locations': locations, 'prices': prices}) 

# def result_search(request):
#     court_name = request.GET.get('court_name')
#     location = request.GET.get('location')
#     prices = request.GET.get('price_per_house')
#     is_available = request.GET.get('is_available')
#     #chuyển sang true false:
#     is_available = True if is_available == '1' else False
#     results = []
#     results = CourtBadminton.objects.filter(
#         (Q(court_name__icontains = court_name) | Q(location__icontains = location)|Q(price_per_house__icontains = prices)) & Q(is_available = is_available)
#     )
#     return render(request, 'QuanLiUser/kq_tim_kiem.html', {'results': results})







# class ForgotPassword(View):

#     def get(self,request):
#         ForgotPassword_Form = ForgotPasswordForm()
#         context = {'form': ForgotPassword_Form}
#         return render(request, 'QuanLiUser/Forgot_Password.html', context)

#     def post(self, request):
#         ForgotPassword_Form= ForgotPasswordForm(request.POST, initial={'otp': request.session.get('otp')})
#         context = {'form': ForgotPassword_Form} 

#         if 'send_otp' in request.POST:
#             handle_send_otp(request, ForgotPassword_Form, context)
#             return render(request, 'QuanLiUser/Forgot_Password.html', context)
        
#         if not ForgotPassword_Form.is_valid():
#             return render(request, 'QuanLiUser/Forgot_Password.html', context )
        
#         # Kiểm tra hiệu lực OTP 
#         if not validate_otp(request):
#             return render(request, 'QuanLiUser/Forgot_Password.html', context)

#         request.session.pop('otp', None)  # Xóa OTP khỏi session
#         return redirect('ChangePassWord')
    
# class ChangePassWord(View):
#     def get(self, request):
#         Change_password = ChangePassword()
#         context = {'form': Change_password}
#         return render(request, 'QuanLiUser/ChangePassword.html', context)

#     def post(self, request):
#         Change_password = ChangePassword(request.POST)
#         context = {'form': Change_password}

#         # Kiểm tra form đổi mật khẩu
#         if not Change_password.is_valid():
#             return render(request, 'QuanLiUser/ChangePassword.html', context)

#         # Lấy username từ session đã lưu
#         username = request.session.get('username')  # Lấy username từ session
#         if not username:
#             messages.error(request, "Không thể xác định người dùng.")
#             return redirect('ForgotPassword')

#         # Lấy mật khẩu mới từ form
#         new_password = Change_password.cleaned_data['new_password']

#         # Cập nhật mật khẩu người dùng
        
#         user = User.objects.get(username=username)
#         user.password = make_password(new_password)
#         user.save()
#         messages.success(request, "Đổi mật khẩu thành công!")
#         return redirect('login')
      




# class DatSan(LoginRequiredMixin,View):
#     login_url = 'login'
#     def get(self, request):
#         get_court = CourtBadminton.objects.all()
#         context = {'courts': get_court}
#         return render(request, 'QuanLiUser/datsan.html', context)
    
#     def post(self,request):
#         court_id = request.POST.get('court')
#         bookingDate = request.POST.get('booking_date')
#         startTime = request.POST.get('start_time')
#         endTime = request.POST.get('end_time')

#         booking = CourtBooking.objects.create(
#             user = request.user,
#             court = CourtBadminton.objects.get(id = court_id),
#             booking_date = bookingDate,
#             start_time = startTime,
#             end_time = endTime
#         )

#         selected_court = CourtBadminton.objects.get(id = court_id)
#         selected_court.is_available = False
#         selected_court.save()

#         messages.success(request, "Đặt sân thành công!")

        
#         return redirect('courtbadminton')  


# import qrcode
# from io import BytesIO
# from base64 import b64encode

# def index(request):
#     return render(request, 'QuanLiUser/index.html') 

# def generate_qr_code(request):
#     qr_code_img = qrcode.make("https://www.google.com/")
#     buffer = BytesIO()
#     qr_code_img.save(buffer)
#     buffer.seek(0)
#     encoded_img = b64encode(buffer.read()).decode()
#     qr_code_data = f'data:image/png;base64,{encoded_img}'
#     return render(request, 'QuanLiUser/qr_code.html', {'qr_code_data': qr_code_data})












def add_timeslot_template(request):
    if request.method == 'POST':
        form = TimeSlotTemplateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Thay 'success_url' bằng URL bạn muốn chuyển hướng đến sau khi lưu thành công
    else:
        form = TimeSlotTemplateForm()
    return render(request, 'app1/add_timeslot_template.html', {'form': form})
