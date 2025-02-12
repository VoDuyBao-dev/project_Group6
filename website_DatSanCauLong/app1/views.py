from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, decorators, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .forms import *
from django.db.models import Q
from .utils import send_otp_email, generate_otp
from django.utils import timezone
from datetime import timedelta, datetime
from django.http import JsonResponse
from .models import *

import json


import nanoid
from .models import TimeSlotTemplate, Court, Booking, Payment, PaymentAccount
from .forms import TimeSlotTemplateForm  # Sẽ tạo file form ở bước tiếp theo
from django.shortcuts import get_object_or_404
from .models import BadmintonHall
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver


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

            # Thêm người dùng vào nhóm "Customer" ở giao diện admin
                group, created = Group.objects.get_or_create(name='Customer')
                user.groups.add(group)


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


def redirect_user(user):
    # with open("debug.log", "a") as f:  
    #     f.write(f"User: {user.username}, Nhóm: {[group.name for group in user.groups.all()]}\n")

    if user.groups.filter(name="Admin").exists():
        return redirect('/admin')
    return redirect('TrangChu')

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
            return redirect_user(request.user)

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
            # response = redirect('TrangChu')
            response = redirect_user(user)

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


# def price_list(request):
#     search_court = SearchForm() 
#     context = {'searchCourt': search_court}  
#     return render(request, 'app1/price_list.html',context)

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

# def booking(request):
#     return render(request, 'app1/Book.html')

def payment(request):
    return render(request, 'app1/payment.html')

def manager_taikhoan(request):
    return render(request, 'app1/QuanLyTaiKhoan.html')














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
        


        
    







def header_guest(request):
    return render(request, 'app1/Header-guest.html')

def header_customer(request):
    return render(request, 'app1/Header-customer.html')

def manager_taikhoan(request):
    return render(request, 'app1/QuanLyTaiKhoan.html')

def manager_san(request):
    return render(request, 'app1/QuanLyThongTinSan.html')

def ThongTinCaNhan(request):
    return render(request, 'app1/ThongTinCaNhan.html')

def ChinhSuaThongTin(request):
    return render(request, 'app1/ChinhSuaThongTin.html')





# từ khúc này là con Lan làm có gì thì né né ra nha.


# thêm thời gian(khung giờ) và giá,... của từng loại hình đặt lịch
def manage_time_slots(request):
    if request.method == "POST":
        day_of_week = request.POST.get('day_of_week')
        time_frame = request.POST.get('time_frame')
        fixed_price = request.POST.get('fixed_price')
        daily_price = request.POST.get('daily_price')
        flexible_price = request.POST.get('flexible_price')
        status = request.POST.get('status')

        # Kiểm tra xem có điền đầy đủ thông tin hay không
        if not day_of_week or not time_frame or not fixed_price or not daily_price or not flexible_price or not status:
            messages.error(request, "Vui lòng nhập đầy đủ thông tin!")
            return redirect('manage_time_slots')
        # Kiểm tra xem có trung ngày và giờ không.
        if TimeSlotTemplate.objects.filter(day_of_week=day_of_week).exists() and TimeSlotTemplate.objects.filter(time_frame=time_frame).exists():
            messages.error(request, "Trùng ngày và khung giờ")
            return redirect("manage_time_slots")

        # Lưu dữ liệu nếu hợp lệ
        TimeSlotTemplate.objects.create(day_of_week=day_of_week, time_frame=time_frame, fixed_price=fixed_price, daily_price=daily_price, flexible_price=flexible_price, status=status,)
        messages.success(request, "Thêm lịch và giá thành công.")
        return redirect('manage_time_slots')

    time_slots = TimeSlotTemplate.objects.all()
    return render(request, "app1/manage_time_slots.html", {"time_slots": time_slots})
        

# xóa lịch nếu thấy bất ổn nào đó.
def delete_time_slot(request, slot_id):
    slot = get_object_or_404(TimeSlotTemplate, template_id=slot_id)
    slot.delete()
    return redirect("manage_time_slots")

# lấy thông tin từ cơ sở dữ liệu của lịch sau đó hiển thị ra giao diện.
def price_list(request):
    time_slots = TimeSlotTemplate.objects.all()
    return render(request, "app1/price_list.html", {"time_slots": time_slots})


# thêm dữ liệu của một sân cầu lông mới(thêm một chi nhánh)
def them_san_moi(request):
    if request.method == "POST":
        name = request.POST.get('name')
        address = request.POST.get('address')

        # Kiểm tra nếu tên hoặc địa chỉ bị bỏ trống
        if not name or not address:
            messages.error(request, "Vui lòng nhập đầy đủ thông tin!")
            return redirect('them_san_moi')

        if BadmintonHall.objects.filter(address=address).exists():
            messages.error(request, "Địa điểm này đã có chi nhánh khác!")
            return redirect("them_san_moi")

        # Lưu dữ liệu nếu hợp lệ
        BadmintonHall.objects.create(name=name, address=address)
        messages.success(request, "Thêm sân mới thành công!")
        return redirect('them_san_moi')

    return render(request, 'app1/them_san_moi.html')


def them_san(request):
    if request.method == "POST":
        badminton_hall_id = request.POST.get('address') 
        name = request.POST.get('name')
        image = request.FILES.get('image') 

        # Kiểm tra nếu có trường bị bỏ trống
        if not name or not badminton_hall_id:
            messages.error(request, "Vui lòng nhập đầy đủ thông tin!")
            return redirect('them_san')

        if Court.objects.filter(name=name).exists():
            messages.error(request, "Sân này đã tồn tại!")
            return redirect("them_san")

        # Lấy thông tin nhà thi đấu
        badminton_hall = get_object_or_404(BadmintonHall, badminton_hall_id=badminton_hall_id)

        # Tạo sân mới (ID sẽ tự động được tạo bởi `default=generate_short_id`)
        court = Court.objects.create(
            badminton_hall=badminton_hall,
            name=name,
            image=image,
        )
        messages.success(request, "Thêm sân mới thành công!")

        return redirect('them_san')

    # Hiển thị danh sách sân và nhà thi đấu
    courts = Court.objects.all()
    badminton_halls = BadmintonHall.objects.all()
    return render(request, 'app1/them_san.html', {"courts": courts, "badminton_halls": badminton_halls})


# quản lý thông tin sân cầu lông
def manager_san(request):
    courts = Court.objects.all()
    return render(request, 'app1/QuanLyThongTinSan.html', {'courts': courts})

def edit_court(request, court_id):
    """
    Xử lý cập nhật thông tin sân khi nhận POST từ modal chỉnh sửa.
    Các thông tin cập nhật:
      - Tên sân
      - Trạng thái
      - Tên chi nhánh (cập nhật tên cho BadmintonHall liên quan)
      - Ảnh: Nếu có upload ảnh mới hoặc yêu cầu xóa ảnh hiện tại
    """
    court = get_object_or_404(Court, court_id=court_id)
    if request.method == "POST":
        new_name = request.POST.get("name")
        new_status = request.POST.get("status")
        new_branch_name = request.POST.get("badminton_hall")
        delete_image_flag = request.POST.get("delete_image")  # "yes" nếu người dùng muốn xóa ảnh hiện tại

        if new_name:
            court.name = new_name

        if new_status:
            court.status = new_status

        # Cập nhật tên chi nhánh (BadmintonHall)
        if new_branch_name:
            badminton_hall = court.badminton_hall
            badminton_hall.name = new_branch_name
            badminton_hall.save()

        # Xử lý ảnh:
        # Nếu có yêu cầu xóa ảnh, xóa file ảnh (nếu tồn tại) và gán None
        if delete_image_flag == "yes":
            if court.image:
                court.image.delete(save=False)
            court.image = None
        else:
            # Nếu người dùng upload ảnh mới, thay thế ảnh cũ (nếu có)
            if "image" in request.FILES:
                if court.image:
                    court.image.delete(save=False)
                court.image = request.FILES["image"]

        court.save()
        messages.success(request, "Thông tin sân đã được cập nhật thành công!")
        return redirect("manager_san")

    return redirect("manager_san")

def delete_court(request, court_id):
    """
    Xử lý xóa sân.
    Khi nhận POST từ modal xác nhận, xóa sân và chuyển hướng về trang danh sách.
    Nếu không phải POST, chuyển hướng về danh sách.
    """
    court = get_object_or_404(Court, court_id=court_id)
    if request.method == "POST":
        court.delete()
        messages.success(request, "Sân đã được xóa thành công!")
        return redirect("manager_san")
    return redirect("manager_san")




@login_required
def booking(request, court_id):
    # Lấy đối tượng sân dựa vào court_id
    court = get_object_or_404(Court, court_id=court_id)
    
    if request.method == 'POST':
        # Xử lý dữ liệu đặt sân (như ví dụ trước)
        booking_type = request.POST.get("booking_type")
        date_str = request.POST.get("date")           
        start_time_str = request.POST.get("start_time") # định dạng HH:MM
        end_time_str = request.POST.get("end_time")     # định dạng HH:MM
        # with open("debug.log", "a") as f:
        #     f.write(f"Date received: {date_str}\n")
        #     f.write(f"Start time received: {start_time_str}\n")
        #     f.write(f"End time received: {end_time_str}\n")

        try:
            booking_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            time_obj = datetime.strptime(start_time_str, "%H:%M").time()
            end_time = datetime.strptime(end_time_str, "%H:%M").time()
            
        except Exception as e:
            messages.error(request, "Sai định dạng ngày hoặc thời gian.")
            return redirect("booking", court_id=court_id)

        # Chuyển đổi ngày thành thứ (ví dụ: "Monday")
        day_of_week = booking_date.strftime("%A")
        templates = TimeSlotTemplate.objects.filter(day_of_week=day_of_week, status='available')
        for template in templates:
            # Giả sử trường time_frame có định dạng "05h - 17h"
            with open("debug.log", "a") as f:
                f.write(f"Day: {template.time_frame}\n")
            parts = template.time_frame.split("-")
            if len(parts) == 2:
                # Loại bỏ khoảng trắng và thay "h" thành ":00" để có định dạng HH:MM
                template_start_str = parts[0].strip().replace("h", ":00")
                template_end_str = parts[1].strip().replace("h", ":00")
                try:
                    template_start = datetime.strptime(template_start_str, "%H:%M").time()
                    template_end = datetime.strptime(template_end_str, "%H:%M").time()
                except Exception as e:
                    continue  # Nếu không parse được, bỏ qua template này
                with open("debug.log", "a") as f:
                    f.write(f"Start time : {template_start_str}\n")
                    f.write(f"End time : {template_end_str}\n")
                    f.write(f"End time :\n")

                # Kiểm tra xem khoảng thời gian người dùng chọn có nằm trong khoảng của template không
                if start_time_str >= template_start and end_time_str <= template_end:
                    template = template
                    break


        booking_start = datetime.combine(booking_date, start_time)
        booking_end = datetime.combine(booking_date, end_time)
        duration_hours = (booking_end - booking_start).total_seconds() / 3600.0
# Tính giá dựa vào loại booking và khoảng thời gian đặt
        if booking_type == "fixed":
            price = template.fixed_price * Decimal(duration_hours)
        elif booking_type == "daily":
            price = template.daily_price * Decimal(duration_hours)
        elif booking_type == "flexible":
            price = template.flexible_price * Decimal(duration_hours)
        else:
            price = Decimal('0.00')

        # Tạo Booking và cập nhật trạng thái sân
        booking = Booking.objects.create(
            customer_id=request.user.customer,  # Hoạt động đúng vì request.user.customer là một object
            court_id=court.court_id,  # Lấy ID của court
            booking_type=booking_type,
            date=booking_date,
            start_time=start_time,
            end_time=end_time,
            status=False
        )
        
        messages.success(request, "Vui lòng thanh toán để hoàn tất đặt sân.")
        return render(request, 'app1/payment.html', {
            'booking_id': booking.booking_id,
            'court_id': court.court_id,
        })
    else:
        return render(request, "app1/Book.html", {"court": court})


@login_required
def payment(request, booking_id, court_id):
    # Lấy đối tượng Booking dựa vào booking_id
    booking = get_object_or_404(Booking, booking_id=booking_id)
    court = get_object_or_404(Court, court_id=court_id)
    # Kiểm tra booking có thuộc về khách hàng đang đăng nhập không
    if booking.customer_id != request.user.customer:
        messages.error(request, "Bạn không có quyền truy cập đơn đặt này.")
        return redirect("TrangChu")

    # # Kiểm tra xem Payment đã tồn tại cho booking này chưa (OneToOne)
    # try:
    #     payment = booking.payment
    # except Payment.DoesNotExist:

        payment = Payment.objects.create(
            booking_id=booking,
            customer_id=request.user.customer,
            status=False  # Chưa thanh toán
        )

    if request.method == "POST":
        # Lấy thông tin tài khoản thanh toán được chọn từ form
        payment_account_id = request.POST.get("payment_account")
        if payment_account_id:
            payment_account = get_object_or_404(PaymentAccount, pk=payment_account_id)
            payment.payment_account = payment_account

        # Tích hợp với cổng thanh toán (giả sử thanh toán thành công)
        payment.status = True  # Đánh dấu đã thanh toán
        payment.save()
        court.status = 'booked'
        court.save()
        booking.status = True
        booking.save()
        messages.success(request, "Thanh toán thành công!")
        # Chuyển hướng sang trang chi tiết booking hoặc trang thông báo thanh toán thành công
        return redirect('San')
    else:
        # GET: Hiển thị form thanh toán
        # Lấy danh sách tài khoản thanh toán của khách hàng (giả sử PaymentAccount có trường customer)
        payment_accounts = PaymentAccount.objects.filter(customer=request.user.customer)
        context = {
            "booking": booking,
            "payment": payment,
            "payment_accounts": payment_accounts,
        }
        return render(request, "app1/payment.html", context)

def Payment(request):
    return render(request, 'app1/payment.html')