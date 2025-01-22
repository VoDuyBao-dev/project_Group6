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
# from .models import CourtBooking,CourtBadminton, User
from django.db.models import Q
from .utils import send_otp_email, generate_otp
from django.utils import timezone
from datetime import timedelta

# Create your views here.

# HÀM KIỂM TRA MÃ OTP ĐỂ TÁI SỬ DỤNG:
# GỬI OTP KHI NGƯỜI DÙNG YÊU CẦUCẦU
def handle_send_otp(request, form_input, context):
    if form_input.is_valid():
        username = form_input.cleaned_data['username']
        otp = generate_otp()
        request.session['otp'] = otp  # Lưu OTP vào session
        request.session['username'] = username  # Lưu username
        request.session['otp_created_at'] = timezone.now().isoformat()  # Lưu thời gian tạo OTP
        send_otp_email(username, otp)
        messages.info(request, "Mã OTP đã được gửi đến email của bạn.")
   

# KIỂM TRA HIỆU LỰC CỦA MÃ OTP
def validate_otp(request):
    otp_created_at = request.session.get('otp_created_at')  # Thời gian tạo OTP từ session

    if not request.session.get('otp'):
        messages.error(request, "Bạn cần gửi mã OTP trước.")
        return False  # Không hợp lệ
    
    # Kiểm tra thời gian hiệu lực của OTP
    if otp_created_at:
        otp_created_at = timezone.datetime.fromisoformat(otp_created_at)  # Chuyển đổi chuỗi sang datetime
        if timezone.now() > otp_created_at + timedelta(minutes=1):  # Thời gian hiệu lực là 1 phút
            messages.error(request, "Mã OTP đã hết hiệu lực, vui lòng gửi lại.")
            request.session.pop('otp', None)  # Xóa OTP hết hạn
            request.session.pop('otp_created_at', None)  # Xóa thời gian tạo OTP
            return False  # Không hợp lệ
    
    return True  # Hợp lệ



def Forgot_password(request):
    return render(request, 'app1/Forgot_password.html')

def New_password(request):
    return render(request, 'app1/New_password.html')

def TrangChu(request):
    return render(request, 'app1/trangchu.html')


class Sign_Up(View):
    def get(self, request):
        sign_up = SignUpForm()
        context = {'SignUp': sign_up}
        return render(request, 'app1/Sign_up.html', context)
    
    

    def post(self, request):
        sign_up = SignUpForm(request.POST, initial={'otp': request.session.get('otp')})
        context = {'SignUp': sign_up}
        
        # Gửi OTP
        if 'send_otp' in request.POST:
            handle_send_otp(request, sign_up, context)
            return render(request, 'app1/Sign_up.html', context)
        
        # trả về lỗi nếu nhập sai
        if not sign_up.is_valid():
            return render(request, 'app1/Sign_up.html', context)

        # Kiểm tra hiệu lực OTP 
        if not validate_otp(request):
            return render(request, 'app1/Sign_up.html', context)
        
        # user = User(
        #     username=sign_up.cleaned_data['username'],
        #     full_name=sign_up.cleaned_data['full_name'],
        #     gender=sign_up.cleaned_data['gender'],
        #     password=make_password(sign_up.cleaned_data['password'])  # Băm mật khẩu
        # )
        # user.save()
        # request.session.pop('otp', None)  # Xóa OTP khỏi session
        messages.success(request, "Đăng kí thành công!")
        return redirect('login')


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

        email = sign_in.cleaned_data['username']
        password = sign_in.cleaned_data['password']
        remember_me = request.POST.get('remember_me')  # Lấy giá trị checkbox "Nhớ tài khoản"
        
        # Xác thực người dùng
        try:
            user = User.objects.get(email=email)
            user = authenticate(username=user.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            response = redirect('TrangChu')
            
            # Lưu email vào cookie nếu chọn "Nhớ tài khoản"
            if remember_me:
                response.set_cookie('remembered_email', email, max_age=7 * 24 * 60 * 60)  # Lưu trong 7 ngày
            else:
                response.delete_cookie('remembered_email')  # Xóa cookie nếu không chọn
            
            return response
        else:
            sign_in.add_error('username', "Email hoặc mật khẩu không đúng.")
            return render(request, 'app1/Sign_in.html', context)

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

