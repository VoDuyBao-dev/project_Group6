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
from django.http import JsonResponse
from .models import *
from django.contrib.auth.decorators import login_required
import json
from .forms import TimeSlotTemplateForm  # Sẽ tạo file form ở bước tiếp theo

from .models import TimeSlotTemplate, Court, Booking, Payment, PaymentAccount, CourtManager, Customer
from django.shortcuts import get_object_or_404
from .models import BadmintonHall
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .context_processors import get_user_role
from app1.forms import RegisterPaymentAccountForm, SearchForm
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import BookingSerializer
from datetime import datetime, timedelta
import logging
from decimal import Decimal, ROUND_HALF_UP


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
        user = User.objects.create_user(username=username,email=username ,first_name=full_name, password=password)
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
                    # Tạo đối tượng Customer liên quan
                    Customer.objects.get_or_create(user=user)

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

            # Xác định loại tài khoản (Customer hoặc CourtManager)
            user_role = None
            if hasattr(user, 'customer'):
                user_role = 'customer'
            elif hasattr(user, 'court_manager'):
                user_role = 'manage'
            elif hasattr(user, 'system_admin'):
                user_role = 'admin'
            else:
                user_role = 'staff'

            # Lưu loại tài khoản vào session
            request.session['user_role'] = user_role

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


# file get_user_role đã chuyển qua processor
def get_menu_by_role(user_role):
    if user_role == 'manage' or user_role == 'admin'or user_role == 'staff':
        return 'app1/Menu-manager.html'
    elif user_role == 'customer' or user_role == None:
        return 'app1/Menu.html'

    
def TrangChu(request):
     
    # Lấy thông tin user_role từ session
    user_role = get_user_role(request)
    menu = get_menu_by_role(user_role)
    
    context = {
        'menu': menu
    }  
    return render(request, 'app1/TrangChu.html', context)

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


def San(request):
    courts = Court.objects.all()
    user_role = get_user_role(request)
    menu = get_menu_by_role(user_role)

    context = {
        'courts': courts,
        'menu': menu
    }
    return render(request, 'app1/San.html', context)


# Tìm kiếm sân
class SearchCourt(View):
    def get(self, request):
        search_court = SearchForm(request.GET)  # Lấy giá trị GET từ người dùng
        results = []
       
        user_role = get_user_role(request)
        menu = get_menu_by_role(user_role)
     
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
            'courts': results,  # Trả về kết quả tìm kiếm
            'menu': menu
        }
        return render(request, 'app1/kqTimKiem.html', context)




# Thôg tin cá nhân
def ThongTinCaNhan(request):
    user = request.user  # Lấy thông tin người dùng đã đăng nhập
    user_role = get_user_role(request)
    menu = get_menu_by_role(user_role)

    # Kiểm tra loại tài khoản
    if hasattr(user, 'customer'):  # Nếu user là Customer
        role = 'customer'
        profile = user.customer  # Lấy thông tin từ bảng Customer
    else:
        role = 'other'  # User không có role cụ thể
        profile = 'none'

    # Truyền thông tin vào context
    context = {
        'user': user,  
        'role': role,  # Truyền loại tài khoản vào template
        'profile': profile,  # Truyền thông tin profile cụ thể
        'menu': menu
    }
    return render(request, 'app1/ThongTinCaNhan.html', context)

def get_role_and_profile(user):
    if hasattr(user, 'customer'):  # Nếu user là Customer
        return 'customer', user.customer
    return 'other', 'none'

# Chỉnh sửa thông tin cá nhân
class ChinhSuaThongTinCaNhan(View):
    
    def get(self, request):
        user = request.user  # Lấy thông tin người dùng đã đăng nhập
        role, profile = get_role_and_profile(user)
        ChinhSuaThongTin = FormChinhSuaThongTinCaNhan(user=user)
        user_role = get_user_role(request)
        menu = get_menu_by_role(user_role)
    
   
        context = {
            "ChinhSuaThongTin" : ChinhSuaThongTin,
            'role': role,  # Truyền loại tài khoản vào template
            'profile': profile,
            'menu': menu
        } 
        return render(request, 'app1/ChinhSuaThongTin.html', context)

    def post(self, request):
        user = request.user
        role, profile = get_role_and_profile(user)
        ChinhSuaThongTin = FormChinhSuaThongTinCaNhan(request.POST, user=user)
        context = {
            "ChinhSuaThongTin" : ChinhSuaThongTin,
            'role': role,  # Truyền loại tài khoản vào template
            'profile': profile,
        }  

        if not ChinhSuaThongTin.is_valid():
            return render(request, 'app1/ChinhSuaThongTin.html', context)
        
        #  Nếu dữ liệu hợp lệ:
        # Lấy dữ liệu
        full_name = ChinhSuaThongTin.cleaned_data['full_name']
        date_of_birth = ChinhSuaThongTin.cleaned_data['date_of_birth']
        if full_name:
            user.first_name = full_name
            user.save()
        # cập nhật ngày sinh cho customer
        if date_of_birth:
            try:
                customer = user.customer # Liên kết OneToOne với Customer
                customer.date_of_birth = date_of_birth
                customer.save()        
            except Exception as e:
                messages.error(request, f"Lỗi khi cập nhật ngày sinh: {str(e)}")
                return render(request, 'app1/ChinhSuaThongTin.html', context)
       
        messages.success(request, "Chỉnh sửa thông tin thành công!")
        return redirect('ThongTinCaNhan')

 

# từ khúc này là con Lan làm có gì thì né né ra nha.


# thêm thời gian(khung giờ) và giá,... của từng loại hình đặt lịch
def manage_time_slots(request):
    if request.method == "POST":
        form = TimeSlotTemplateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("manage_time_slots")  # Reload lại trang sau khi lưu
    else:
        form = TimeSlotTemplateForm()

    time_slots = TimeSlotTemplate.objects.all()
    return render(request, "app1/manage_time_slots.html", {"form": form, "time_slots": time_slots})

# xóa lịch nếu thấy bất ổn nào đó.
def delete_time_slot(request, slot_id):
    slot = get_object_or_404(TimeSlotTemplate, template_id=slot_id)
    slot.delete()
    return redirect("manage_time_slots")

# lấy thông tin từ cơ sở dữ liệu của lịch sau đó hiển thị ra giao diện.
def price_list(request):
    time_slots = TimeSlotTemplate.objects.all()
    user_role = get_user_role(request)
    menu = get_menu_by_role(user_role)
    
    context = {
        'menu': menu,
        "time_slots": time_slots
    }  
    
    return render(request, "app1/price_list.html", context)


# thêm dữ liệu của một sân cầu lông mới(thêm một chi nhánh)
def them_san_moi(request):
    if request.method == "POST":
        name = request.POST.get('name')
        address = request.POST.get('address')

        # Kiểm tra nếu tên hoặc địa chỉ bị bỏ trống
        if not name or not address:
            messages.error(request, "Vui lòng nhập đầy đủ thông tin!")
            return redirect('them_san_moi')

        # Lưu dữ liệu nếu hợp lệ
        BadmintonHall.objects.create(name=name, address=address)
        messages.success(request, "Thêm sân mới thành công!")
        return redirect('them_san_moi')

    halls = BadmintonHall.objects.all()
    return render(request, 'app1/them_san_moi.html', {'halls': halls})


def them_san(request):
    if request.method == "POST":
        badminton_hall_id = request.POST.get('address')
        name = request.POST.get('name')
        image = request.FILES.get('image') 
        status = request.POST.get('status')

        # Kiểm tra nếu tên hoặc địa chỉ bị bỏ trống
        if not name or not badminton_hall_id or not status:
            messages.error(request, "Vui lòng nhập đầy đủ thông tin!")
            return redirect('them_san')
        badminton_hall = get_object_or_404(BadmintonHall, badminton_hall_id=badminton_hall_id)
        # Lưu dữ liệu nếu hợp lệ
        Court.objects.create(badminton_hall=badminton_hall, name=name, image=image, status=status)
        messages.success(request, "Thêm sân mới thành công!")
        return redirect('them_san')

    courts = Court.objects.all()
    badminton_halls = BadmintonHall.objects.all()
    return render(request, 'app1/them_san.html', {"courts": courts, "badminton_halls": badminton_halls})


def getAll_role_User():
    users_with_roles = []

    for user in User.objects.all():
        if hasattr(user, 'system_admin'):  
            role = "Admin"
        elif hasattr(user, 'court_manager'):  
            role = "Quản lý"
        elif hasattr(user, 'court_staff'):  
            role = "Staff"
        else:
            role = "Người dùng"  

        if role != "Admin":
            users_with_roles.append({
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "role": role
            })

    return users_with_roles

@decorators.login_required(login_url='Sign_in')
def Account_Management(request):
    Add_Account_Form = AddAccountForm()
    # Danh sách người dùng kèm vai trò
    users_with_roles = getAll_role_User()

    context = {
        "Add_Account_Form": Add_Account_Form,
        "users_with_roles": users_with_roles
    }
    return render(request, 'app1/QuanLyTaiKhoan.html', context)

def AddAccount_Manage(request):
      
    if request.method == "POST":
        Add_Account_Form = AddAccountForm(request.POST)
        users_with_roles = getAll_role_User()
        context = {
            "Add_Account_Form": Add_Account_Form,
            "users_with_roles": users_with_roles
        }
        if not Add_Account_Form.is_valid():

            return render(request, 'app1/QuanLyTaiKhoan.html', context)

        # Lấy thông tin từ form
        username = Add_Account_Form.cleaned_data['username']
        password = Add_Account_Form.cleaned_data['password']
        role = Add_Account_Form.cleaned_data['role']

        try:
            with transaction.atomic():
                # Tạo user mới
                user = User.objects.create_user(username=username, password=password)

                # Nếu vai trò là quản lý thì tạo CourtManager
                if role == "manage":
                    CourtManager.objects.create(user=user)
                    # Nếu vai trò là quản lý thì tạo CourtManager
                elif role == "staff":
                    CourtStaff.objects.create(user=user)

                elif role == "customer":
                    Customer.objects.create(user=user)
                
                messages.success(request, "Thêm tài khoản mới thành công!")

        except Exception as e:
            messages.error(request, f"Lỗi khi thêm tài khoản: {str(e)}")

        # Redirect về trang quản lý tài khoản
        return redirect('Account_Management')
    elif request.method == "GET":
        # Chuyển hướng về trang quản lý tài khoản nếu truy cập qua GET
        return redirect('Account_Management')
    
    # Nếu không phải POST hoăcj GET, trả về lỗi
    messages.error(request, "Lỗi phương thức.")
    return redirect('Account_Management')
        
# Xóa tài khoản
def delete_user(request, user_id):
    if request.method == "POST":
        try:
            user = User.objects.get(pk=user_id)
            user.delete()
            return JsonResponse({"message": "Tài khoản đã được xóa!"}, status=200)
        except User.DoesNotExist:
            return JsonResponse({"error": "Tài khoản không tồn tại!"}, status=404)
    return JsonResponse({"error": "Yêu cầu không hợp lệ!"}, status=400)


def Update_account(request, user_id):
    if request.method == "POST":
        # Lấy thông tin user cần cập nhật
        user = get_object_or_404(User, id=user_id)

        # Lấy dữ liệu từ form
        new_password = request.POST.get("password", "").strip()
        new_role = request.POST.get("role", "").strip()

        # Cập nhật password nếu có
        if new_password:
            user.set_password(new_password)

        # Xóa tất cả vai trò cũ trước khi thêm vai trò mới
        CourtManager.objects.filter(user=user).delete()
        CourtStaff.objects.filter(user=user).delete()
        Customer.objects.filter(user=user).delete()

        if new_role:
            if new_role == "manage":
                CourtManager.objects.get_or_create(user=user)
                
            elif new_role == "staff":
                CourtStaff.objects.get_or_create(user=user)
                
            elif new_role == "customer":
                Customer.objects.get_or_create(user=user)
                
            
        # Lưu thay đổi
        user.save()

        return JsonResponse({"status": "success", "message": "Tài khoản đã được cập nhật."})

    return JsonResponse({"status": "error", "message": "Yêu cầu không hợp lệ."}, status=400)



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
    user_role = get_user_role(request)
    menu = get_menu_by_role(user_role)
    
    context = {
        'menu': menu,
        "time_slots": time_slots
    }  
    
    return render(request, "app1/price_list.html", context)


# thêm dữ liệu của một sân cầu lông mới(thêm một chi nhánh)
def them_san_moi(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        court_manager_id = request.POST.get('court_manager')  # Lấy ID của CourtManager

        if not name or not address:
            messages.error(request, "Vui lòng nhập đầy đủ thông tin.")
        else:
            # Kiểm tra xem chi nhánh hoặc địa điểm đã tồn tại chưa
            if BadmintonHall.objects.filter(name=name).exists():
                messages.error(request, "Tên chi nhánh đã tồn tại. Vui lòng chọn tên khác.")
            elif BadmintonHall.objects.filter(address=address).exists():
                messages.error(request, "Địa điểm này đã có chi nhánh. Vui lòng chọn địa điểm khác.")
            else:
                badminton_hall = BadmintonHall.objects.create(name=name, address=address)
                court_manager = CourtManager.objects.get(courtManager_id=court_manager_id)
                if court_manager_id:
                    try:
                        # Kiểm tra nếu CourtManager đã có BadmintonHall
                        if hasattr(court_manager, 'badminton_hall'):
                            messages.error(request, "Quản lý này đã được gán cho một chi nhánh khác.")
                        else:
                            badminton_hall.court_manager = court_manager
                            badminton_hall.save()
                            messages.success(request, "Thêm chi nhánh thành công!")
                    except CourtManager.DoesNotExist:
                        messages.error(request, "Quản lý không tồn tại.")
                else:
                    badminton_hall.save()
                    messages.success(request, "Thêm chi nhánh thành công!")

    # Cập nhật danh sách CourtManager chưa có BadmintonHall
    court_managers = CourtManager.objects.filter(badminton_hall__isnull=True)
    
    return render(request, 'app1/them_san_moi.html', {'court_managers': court_managers})


def footer(request):
    Badminton_Halls = BadmintonHall.objects.all()
    return render(request, 'app1/Footer.html', {"Badminton_Halls": Badminton_Halls})


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
        return redirect("them_san")

    badminton_halls = BadmintonHall.objects.all()
    return render(request, 'app1/them_san.html', {"badminton_halls": badminton_halls})


# quản lý thông tin sân cầu lông
def manager_san(request):
    courts = Court.objects.all()
    return render(request, 'app1/QuanLyThongTinSan.html', {'courts': courts})

def edit_court(request, court_id):
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
    court = get_object_or_404(Court, court_id=court_id)
    if request.method == "POST":
        court.delete()
        messages.success(request, "Sân đã được xóa thành công!")
        return redirect("manager_san")
    return redirect("manager_san")




@decorators.login_required(login_url='Sign_in')
def select_court(request):
    if request.method == "POST":
        court_id = request.POST.get("court_id")
        print("DEBUG: Nhận yêu cầu chọn sân, court_id =", court_id)  # Kiểm tra dữ liệu nhận được

        if court_id:
            request.session["selected_court_id"] = court_id
            print("DEBUG: Đã lưu selected_court_id vào session:", request.session["selected_court_id"])  # Kiểm tra lưu session
            return redirect("booking")  # Chuyển đến trang đặt sân
        else:
            messages.error(request, "Không tìm thấy sân! Vui lòng chọn lại.")
            print("DEBUG: Không tìm thấy court_id, quay lại trang San")  # Debug lỗi
            return redirect("San")

    return redirect("San")


class DangKyTaiKhoanThanhToan(View):
    def get(self, request):
        register_payment_Account = RegisterPaymentAccountForm()
        search_court = SearchForm()
        court_managers = CourtManager.objects.all()

        context = {
            'Register_Payment_Account': register_payment_Account,
            'searchCourt': search_court,
            'court_managers': court_managers
        }
        return render(request, 'app1/DangKiTaiKhoanThanhToan.html', context)

    def post(self, request):
        register_payment_Account = RegisterPaymentAccountForm(request.POST)
        search_court = SearchForm()
        court_managers = CourtManager.objects.all()

        if not register_payment_Account.is_valid():
            messages.error(request, "Thông tin nhập không hợp lệ!")
            return render(request, 'app1/DangKiTaiKhoanThanhToan.html', {
                'Register_Payment_Account': register_payment_Account,
                'searchCourt': search_court,
                'court_managers': court_managers
            })

        # Lấy dữ liệu đã được kiểm tra từ form
        cleaned_data = register_payment_Account.cleaned_data
        accountHolder = cleaned_data['accountHolder']
        paymentMethod = cleaned_data['paymentMethod']
        accountNumber = cleaned_data.get('accountNumber', None)
        phoneNumber = cleaned_data.get('phoneNumber', None)
        bankName = cleaned_data.get('bankName', None)
        court_manager_id = request.POST.get('court_manager')

        # Kiểm tra nếu chưa chọn Court Manager
        if not court_manager_id:
            messages.error(request, "Vui lòng chọn Court Manager hợp lệ!")
            return self.render_form_with_errors(request, register_payment_Account, search_court)

        # Lấy Court Manager hoặc trả lỗi 404 nếu không tồn tại
        court_manager = get_object_or_404(CourtManager, courtManager_id=court_manager_id)
        # Kiểm tra Court Manager đã có tài khoản thanh toán chưa
        if PaymentAccount.objects.filter(accountHolder=court_manager.user.username).exists():
            messages.error(request, "Court Manager này đã có tài khoản thanh toán!")
            return self.render_form_with_errors(request, register_payment_Account, search_court)

        # Tạo tài khoản thanh toán
        payment_account = PaymentAccount.objects.create(
            accountHolder=accountHolder,
            accountNumber=accountNumber if paymentMethod == "bank" else None,
            phoneNumber=phoneNumber if paymentMethod == "momo" else None,
            bankName=bankName if paymentMethod == "bank" else None,
            paymentMethod=paymentMethod,
            court_manager = court_manager
        )

        

        messages.success(request, "Đăng ký tài khoản thanh toán thành công!")
        return redirect('DangKyTaiKhoanThanhToan')

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

logger = logging.getLogger(__name__)
@decorators.login_required(login_url='Sign_in')
def booking_view(request, court_id=None):
    if court_id:
        court = get_object_or_404(Court, court_id=court_id)
    else:
        court = None

    if request.method == 'POST':
        try:
            # Lấy dữ liệu từ form
            booking_type = request.POST.get('booking_type')
            date_str = request.POST.get('date')
            start_time_str = request.POST.get('start_time')
            end_time_str = request.POST.get('end_time')

            if not (court and booking_type and date_str and start_time_str and end_time_str):
                messages.error(request, "Vui lòng nhập đầy đủ thông tin!")
                return redirect('booking', court_id=court.court_id)

            # Chuyển đổi kiểu dữ liệu
            booking_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            start_time = datetime.strptime(start_time_str, "%H:%M").time()
            end_time = datetime.strptime(end_time_str, "%H:%M").time()

            # Điều kiện 1: Ngày đặt không được ở trong quá khứ
            today = date.today()
            if booking_date < today:
                messages.error(request, "Không thể đặt sân vào ngày trong quá khứ!")
                return redirect('booking', court_id=court.court_id)

            # Điều kiện 2: Giờ bắt đầu phải nhỏ hơn giờ kết thúc
            if start_time >= end_time:
                messages.error(request, "Giờ bắt đầu phải nhỏ hơn giờ kết thúc!")
                return redirect('booking', court_id=court.court_id)

            # Điều kiện 3: Kiểm tra trùng lịch với các booking đã thanh toán
            conflicting_booking = Booking.objects.filter(
                court=court, date=booking_date, status=True
            ).filter(
                start_time__lt=end_time, end_time__gt=start_time
            ).exists()
            
            if conflicting_booking:
                messages.error(request, "Khung giờ này đã được đặt và thanh toán, vui lòng chọn khung giờ khác!")
                return redirect('booking', court_id=court.court_id)

            # Tìm các time slot templates phù hợp
            day_of_week = booking_date.strftime("%A")
            templates = TimeSlotTemplate.objects.filter(day_of_week=day_of_week, status='available').order_by('time_frame')
            
            total_price = Decimal('0.00')
            current_time = start_time
            
            while current_time < end_time:
                for temp in templates:
                    try:
                        parts = temp.time_frame.replace("h", "").strip().split("-")
                        template_start = datetime.strptime(parts[0].strip().zfill(2) + ":00", "%H:%M").time()
                        template_end = datetime.strptime(parts[1].strip().zfill(2) + ":00", "%H:%M").time()
                        
                        if current_time >= template_start and current_time < template_end:
                            next_time = min(end_time, template_end)
                            duration_hours = Decimal((datetime.combine(booking_date, next_time) - datetime.combine(booking_date, current_time)).total_seconds() / 3600.0)
                            
                            if booking_type == "fixed":
                                total_price += temp.fixed_price * duration_hours
                            elif booking_type == "daily":
                                total_price += temp.daily_price * duration_hours
                            elif booking_type == "flexible":
                                total_price += temp.flexible_price * duration_hours
                            
                            current_time = next_time
                            break
                    except Exception:
                        continue  # Bỏ qua template bị lỗi
                else:
                    messages.error(request, "Không tìm thấy giá cho khung giờ này!")
                    return redirect('booking', court_id=court.court_id)
            
            # Làm tròn đến 3 chữ số thập phân
            total_price = total_price.quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
            
            # Lưu booking vào database
            if hasattr(request.user, 'customer'):
                booking = Booking.objects.create(
                    customer_id=request.user.customer.customer_id,  # Gán đối tượng Customer cho trường customer
                    court=court,
                    booking_type=booking_type,
                    date=booking_date,
                    start_time=start_time,
                    end_time=end_time,
                    status=False,
                    amount=total_price,
                )
            elif hasattr(request.user, 'court_manager'):
                booking = Booking.objects.create(
                    customer_id=request.user.court_manager.courtManager_id,  # Gán đối tượng CourtManager cho trường court_manager
                    court=court,
                    booking_type=booking_type,
                    date=booking_date,
                    start_time=start_time,
                    end_time=end_time,
                    status=False,
                    amount=total_price,
                )
            else:
                messages.error(request, "Bạn không có quyền đặt sân.")
                return redirect('booking', court_id=court.court_id)

            # messages.success(request, f"Bạn đã thanh toán hoá đơn {total_price} thành công.")
            return redirect('payment', booking_id=booking.booking_id, court_id=court.court_id)

        except Exception as e:
            messages.error(request, f"Có lỗi xảy ra: {str(e)}")

    return render(request, 'app1/Book.html', {"court": court})


@decorators.login_required(login_url='Sign_in')
def payment(request, booking_id, court_id):
    user_role = get_user_role(request)
    menu = get_menu_by_role(user_role)
    booking = get_object_or_404(Booking, booking_id=booking_id, court_id=court_id)
    amount = Decimal(booking.amount).quantize(Decimal("0.001"))

    # Kiểm tra xem sân có thuộc một BadmintonHall hay không
    badminton_hall = getattr(booking.court, 'badminton_hall', None)

    # Lấy CourtManager của sân đó (nếu có)
    court_manager = getattr(badminton_hall, 'court_manager', None)

    # Lấy danh sách tài khoản thanh toán của CourtManager (nếu có)
    payment_accounts = court_manager.payment_accounts.all() if court_manager else []

    if request.method == "POST":
        
        # Kiểm tra nếu đã có payment cho booking này thì không tạo mới
        if hasattr(booking, 'payment'):
            messages.warning(request, "Booking này đã được thanh toán.")
            return redirect('payment', booking_id=booking.booking_id, court_id=court_id)

        # Lưu vào database
        payment = Payment.objects.create(
            booking=booking,
            payment_account=payment_accounts.first() if payment_accounts else None,  # Chọn tài khoản đầu tiên
            status=True  # Đánh dấu đã thanh toán
        )

        # Cập nhật trạng thái của booking
        booking.status = True
        booking.save()

        messages.success(request, "Thanh toán thành công!")
        # return redirect('payment', booking_id=booking.booking_id, court_id=booking.court_id)  # Điều hướng đến trang chi tiết booking
        return redirect('History')  # Điều hướng đến trang chi tiết booking
         
    context = {
        'menu': menu,
        'booking': booking, 
        'amount': amount,
        'payment_accounts': payment_accounts
    }
    return render(request, 'app1/payment.html',context)

@login_required
def checkin(request):
    context = {}

    if request.method == "POST":
        booking_id = request.POST.get("booking_id")

        try:
            # Kiểm tra xem có payment không & đã thanh toán chưa
            payment = Payment.objects.get(booking__booking_id=booking_id, status=True)

            # Nếu có payment hợp lệ, lấy thông tin booking
            booking = payment.booking
            customer = Customer.objects.get(customer_id=booking.customer_id)
            user = User.objects.get(id=customer.user_id)

            # Lưu thông tin vào context để truyền sang template
            context["customer_name"] = user.first_name  # Lấy tên khách hàng
            context["court"] = booking.court.name  # Lấy tên sân

            messages.success(request, "Check-in thành công!")  # Thông báo check-in thành công

        except Payment.DoesNotExist:
            # Nếu không tìm thấy payment hợp lệ, báo lỗi
            context["error"] = "Mã đặt lịch không hợp lệ!"

    return render(request, "app1/Check-in.html", context)


@decorators.login_required(login_url='Sign_in')
def History(request):
    user = request.user  
    user_role = get_user_role(request)
    menu = get_menu_by_role(user_role)
    # Lấy Customer từ User
    try:
        customer = Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        customer = None
    if customer is None:
        manager = CourtManager.objects.get(user=user)
    # Nếu customer tồn tại, lấy danh sách booking đã thanh toán (có payment)
    if customer:
        bookings = Booking.objects.filter(
            customer_id=customer.customer_id, 
            payment__isnull=False
        ).select_related('payment')
    elif manager:
        bookings = Booking.objects.filter(
            customer_id=manager.courtManager_id, 
            payment__isnull=False
        ).select_related('payment')
    else:
        bookings = []

    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        try:
            booking = Booking.objects.get(booking_id=booking_id, customer_id=customer.customer_id)
            booking.delete()
            messages.success(request, "Đã hủy đặt sân thành công!")
        except Booking.DoesNotExist:
            messages.error(request, "Không tìm thấy đặt sân này!")

        return redirect("History")  

    return render(request, "app1/LichSuDatSan.html", {"bookings": bookings, 'menu': menu})


def bao_cao(request):
    return render(request, 'app1/BaoCaoDoanhThu.html')
