from django.shortcuts import render
from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, decorators, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .forms import *
from django.db.models import Q
from .utils import send_otp_email, generate_otp
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from .models import *

import json


# from .forms import TimeSlotTemplateForm

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
        

def TrangChu(request):
    search_court = SearchForm() 
    context = {'searchCourt': search_court}  
    return render(request, 'app1/TrangChu.html', context)
def header_user(request):
    search_court = SearchForm() 
    context = {'searchCourt': search_court}  
    return render(request, 'app1/Header-user.html',context)

def menu(request):
    return render(request, 'app1/Menu.html')

# def menu_manager(request):
#     return render(request, 'app1/Menu-manager.html')

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
        # Lấy email từ cookie nếu có
        remembered_email = request.COOKIES.get('remembered_email', '')
        sign_in_form = SignInForm(initial={'username': remembered_email})
        
        context = {
            'SignIn': sign_in_form,
            'remember_me': bool(remembered_email),
        }
        return render(request, 'app1/Sign_in.html', context)

    def post(self, request):
        # Nếu user đã đăng nhập, không cần đăng nhập lại
        if request.user.is_authenticated:
            return redirect('TrangChu')

        # Khởi tạo form với dữ liệu từ request.POST
        sign_in_form = SignInForm(request.POST)
        context = {'SignIn': sign_in_form}

        # Lấy số lần đăng nhập sai từ session (mặc định là 0)
        failed_attempts = request.session.get('failed_attempts', 0)

        # Kiểm tra form hợp lệ
        if not sign_in_form.is_valid():
            return render(request, 'app1/Sign_in.html', context)

        # Lấy dữ liệu từ form
        username = sign_in_form.cleaned_data['username']
        password = sign_in_form.cleaned_data['password']
        remember_me = request.POST.get('remember_me') == 'on'  # Checkbox "Nhớ tài khoản"

        # Xác thực người dùng
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Đăng nhập user vào session
            login(request, user)
            request.session['failed_attempts'] = 0  # Reset số lần sai

            # Chuyển hướng về trang chủ sau khi đăng nhập thành công
            response = redirect('TrangChu')

            # Lưu email vào cookie nếu chọn "Nhớ tài khoản"
            if remember_me:
                response.set_cookie('remembered_email', username, max_age=7 * 24 * 60 * 60)
            else:
                response.delete_cookie('remembered_email')

            return response
        else:
            # Nếu nhập sai 5 lần trở lên, yêu cầu reset mật khẩu
            if failed_attempts >= 4:
                context['error_message'] = "Bạn đã nhập sai quá 5 lần. Vui lòng đặt lại mật khẩu."
            else:
                request.session['failed_attempts'] = failed_attempts + 1
                context['error_message'] = "Email hoặc mật khẩu không đúng."

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
    
# Đăng xuất 
def Logout(request):
    logout(request)
    return redirect('TrangChu')

def History(request):
    return render(request, 'app1/LichSuDatSan.html')

def price_list(request):
    search_court = SearchForm() 
    context = {'searchCourt': search_court}  
    return render(request, 'app1/price_list.html',context)

def San(request):
    courts = Court.objects.all()
    search_court = SearchForm()
    context = {
        'courts': courts,
        'searchCourt': search_court
    }
    return render(request, 'app1/San.html', context)

def bao_cao(request):
    return render(request, 'app1/BaoCaoDoanhThu.html')

def checkin(request):
    return render(request, 'app1/Chek-in.html')

# Tìm kiếm sân
class SearchCourt(View):
    def get(self, request):
        search_court = SearchForm(request.GET)  # Lấy giá trị GET từ người dùng
        results = []

        if search_court.is_valid():
            query = search_court.cleaned_data.get('query', '').strip()
            
            # Chỉ tìm kiếm khi có dữ liệu
            if query:
                # Tìm kiếm sân theo tên hoặc địa chỉ tương đối
                filters = Q()
                filters |= Q(name__icontains=query)  # Tìm tên sân chứa từ khóa
                filters |= Q(badminton_hall_id__address__icontains=query)  # Tìm địa chỉ sân chứa từ khóa
                results = Court.objects.filter(filters).order_by('name')  # Thực hiện tìm kiếm với bộ lọc
                
        context = {
            'searchCourt': search_court,
            'courts': results  # Trả về kết quả tìm kiếm
        }
        return render(request, 'app1/kqTimKiem.html', context)

# Đăng ký tài khoản thanh toán của manager
class DangKyTaiKhoanThanhToan(View):

    def get(self,request):
        register_payment_Account=RegisterPaymentAccountForm()
        search_court = SearchForm()
        context = {
            'Register_Payment_Account': register_payment_Account,
            'searchCourt': search_court
        }
        return render(request, 'app1/DangKiTaiKhoanThanhToan.html', context)

    def post(self,request):
        register_payment_Account=RegisterPaymentAccountForm(request.POST)
        search_court = SearchForm()
        context = {
            'Register_Payment_Account': register_payment_Account,
            'searchCourt': search_court
        }

        if not register_payment_Account.is_valid():
            return render(request, 'app1/DangKiTaiKhoanThanhToan.html', context)
        
        # form hợp lệ thì lấy dữ liệu từ form
        accountHolder = register_payment_Account.cleaned_data['accountHolder']
        accountNumber = register_payment_Account.cleaned_data['accountNumber']
        paymentMethod = register_payment_Account.cleaned_data['paymentMethod']

        payment_account = PaymentAccount.objects.create(
            accountHolder=accountHolder,
            accountNumber=accountNumber,
            paymentMethod=paymentMethod
        )
        messages.success(request, "Đăng ký tài khoản thanh toán thành công!")

        return render(request, 'app1/DangKiTaiKhoanThanhToan.html', context)

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





from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Court, BadmintonHall


def quan_ly_san(request):
    """Trang hiển thị danh sách sân"""
    courts = Court.objects.all()
    return render(request, "app1/QuanLyThongTinSan.html", {"courts": courts})


@csrf_exempt
def them_san(request):
    """Thêm sân mới"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name")
            hall_id = data.get("badminton_hall_id")

            badminton_hall = get_object_or_404(BadmintonHall, badminton_hall_id=hall_id)
            new_court = Court.objects.create(name=name, badminton_hall_id=badminton_hall)
            return JsonResponse({"message": "Thêm sân thành công!", "court_id": new_court.court_id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Phương thức không hợp lệ"}, status=405)


@csrf_exempt
def cap_nhat_trang_thai(request):
    """Cập nhật trạng thái sân"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            court_id = data.get("court_id")
            status = data.get("status")

            court = get_object_or_404(Court, court_id=court_id)
            court.status = status  # Cần thêm field `status` vào model Court
            court.save()

            return JsonResponse({"message": "Cập nhật trạng thái thành công!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Phương thức không hợp lệ"}, status=405)


@csrf_exempt
def xoa_san(request, court_id):
    """Xóa sân khỏi hệ thống"""
    if request.method == "DELETE":
        try:
            court = get_object_or_404(Court, court_id=court_id)
            court.delete()
            return JsonResponse({"message": "Xóa sân thành công!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Phương thức không hợp lệ"}, status=405)






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
        


        
    




















# def add_timeslot_template(request):
#     if request.method == 'POST':
#         form = TimeSlotTemplateForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('success_url')  # Thay 'success_url' bằng URL bạn muốn chuyển hướng đến sau khi lưu thành công
#     else:
#         form = TimeSlotTemplateForm()
#     return render(request, 'app1/add_timeslot_template.html', {'form': form})
