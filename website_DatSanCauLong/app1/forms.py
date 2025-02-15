from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from .models import TimeSlotTemplate
from .models import Court
import re
from .models import PaymentAccount
# from .models import TimeSlotTemplate

# Kiểm tra định dạng email
def is_valid_email(email):
    
    try:
        validate_email(email)
    except ValidationError:
        return  False
    else:
        return True

def validate_username_and_otp(cleaned_data, initial_data):
    username = cleaned_data.get('username')
    otp = cleaned_data.get('otp')
    
    errors = {}

    if not is_valid_email(username):
        errors['username'] = "Email không hợp lệ."

    # Kiểm tra mã OTP nếu đã gửi
    if 'otp_sent' in cleaned_data and not otp:
        errors['otp'] = "Vui lòng nhập mã OTP đã gửi."

    if otp and otp != initial_data.get('otp', ''):
        errors['otp'] = "Mã OTP không chính xác."
    
    return errors


class SignUpForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nhập email',
            'id': 'username_SignUp'
        })
    )
    full_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nhập họ và tên',
            'id': 'full_name'
        })
    )
    
    password = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Mật khẩu',
            'id': 'id_password'
        })
    )
    confirm_password = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Nhập lại mật khẩu',
            'id': 'id_confirm_password'
        })
    )
    


    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        

        #  Biến để lưu lỗi
        errors = {}

        if not is_valid_email(username):
            errors['username'] = "Email không hợp lệ."
        
        # Kiểm tra tên người dùng
        if  User.objects.filter(username=username).exists():
            errors['username'] = "Người dùng đã tồn tại."

        if  password != confirm_password:
            errors['confirm_password'] = "Mật khẩu không khớp."
            
        # Nếu có lỗi, thêm vào biểu mẫu
        for field, error in errors.items():
            self.add_error(field, error)

        return cleaned_data  # Trả về dữ liệu đã làm sạch
    


class SignInForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nhập email',
            'id': 'username'
        })
    )
   
    password = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Mật khẩu',
            'id': 'id_password' # Thêm id cho trường mật khẩu
        })
    )
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        errors = {}

        # if not is_valid_email(username):
        #     errors['username'] = "Email không hợp lệ."

        # Nếu người đăng nhập không thuộc group customer thì thông báo lỗi
        user = User.objects.filter(username=username).first()
        if user and user.groups.filter(name='Customer').exists():
            if not is_valid_email(username):
                errors['username'] = "Email không hợp lệ."


        for field, error in errors.items():
            self.add_error(field, error)

        return cleaned_data
    
    
class ForgotPasswordForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nhập email',
            'id': 'id_username_ForgotPassword'

        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        errors = {}

        if not User.objects.filter(username = username).exists():
            errors['username'] = "Người dùng không tồn tại."

        # if not is_valid_email(username):
        #     errors['username'] = "Email không hợp lệ."
        user = User.objects.filter(username=username).first()
        if user and user.groups.filter(name='Customer').exists():
            if not is_valid_email(username):
                errors['username'] = "Email không hợp lệ."

        for field, error in errors.items():
            self.add_error(field, error)

        return cleaned_data
    
class NewPasswordForm(forms.Form):
    new_password = forms.CharField(
        max_length=128,
        required=True,   
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Nhập mật khẩu mới',
            'id': 'id_new_password'
        })
    )
    confirm_new_password = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Nhập lại mật khẩu',
            'id': 'id_confirm_new_password'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")

        errors = {}
        if  new_password != confirm_new_password:
            errors['confirm_new_password'] = "Mật khẩu không khớp."

        for field, error in errors.items():
            self.add_error(field, error)

        return cleaned_data  # Trả về dữ liệu đã làm sạch

   
    
# form này con Lan làm nha.
class TimeSlotTemplateForm(forms.ModelForm):
    class Meta:
        model = TimeSlotTemplate
        fields = ["day_of_week", "time_frame", "fixed_price", "daily_price", "flexible_price", "status"]
   


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Tìm kiếm...',
            'id': 'search_query'
        })
    )
  
# đăng kí tài khoản thanh toán
from django import forms
from app1.models import PaymentAccount
import re

class RegisterPaymentAccountForm(forms.Form):
    accountHolder = forms.CharField(
        label="Tên chủ tài khoản",
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Nhập tên chủ tài khoản'})
    )
    accountNumber = forms.CharField(
        label="Số tài khoản",
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Nhập số tài khoản'})
    )
    paymentMethod = forms.ChoiceField(
        label="Phương thức thanh toán",
        choices=[
            ("", "Chọn phương thức thanh toán"),
            ("bank", "Ngân hàng"),
            ("momo", "Momo")
        ],
        widget=forms.Select()
    )
    bankName = forms.CharField(
        label="Tên ngân hàng",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Nhập tên ngân hàng'})
    )
    phoneNumber = forms.CharField(
        label="Số điện thoại MoMo",
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Nhập số điện thoại MoMo'})
    )

    def clean(self):
        cleaned_data = super().clean()
        accountHolder = cleaned_data.get("accountHolder", "").strip()
        accountNumber = cleaned_data.get("accountNumber", "").strip()
        paymentMethod = cleaned_data.get("paymentMethod")
        bankName = cleaned_data.get("bankName", "").strip()
        phoneNumber = cleaned_data.get("phoneNumber", "").strip()

        errors = {}

        if paymentMethod == "bank":
            if not bankName:
                errors['bankName'] = "Vui lòng nhập tên ngân hàng."
            if not re.match(r'^[A-Z\s]+$', accountHolder):
                errors['accountHolder'] = "Tên chủ tài khoản chỉ được chứa chữ in hoa và khoảng trắng."
            if not accountNumber.isdigit():
                errors['accountNumber'] = "Số tài khoản chỉ được chứa số."
            if len(accountNumber) < 9:
                errors['accountNumber'] = "Số tài khoản phải có ít nhất 9 chữ số."

        elif paymentMethod == "momo":
            if not re.match(r'^[A-Za-zÀ-ỹ\s]+$', accountHolder):
                errors['accountHolder'] = "Tên chủ tài khoản chỉ được chứa chữ cái và khoảng trắng."
            if not phoneNumber.isdigit():
                errors['phoneNumber'] = "Số điện thoại chỉ được chứa số."
            if len(phoneNumber) != 10:
                errors['phoneNumber'] = "Số điện thoại phải có đúng 10 chữ số."

        # Kiểm tra trùng số tài khoản
        if PaymentAccount.objects.filter(accountNumber=accountNumber, paymentMethod=paymentMethod).exists():
            errors['accountNumber'] = "Số tài khoản này đã được sử dụng với phương thức thanh toán này."

        for field, error in errors.items():
            self.add_error(field, error)

        return cleaned_data




from django import forms
from django.contrib.auth.models import User
from app1.models import BadmintonHall, CourtManager, PaymentAccount

class BadmintonHallForm(forms.ModelForm):
    manager_username = forms.CharField(max_length=150, required=True, label="Tên đăng nhập Quản lý")
    manager_email = forms.EmailField(required=True, label="Email Quản lý")
    manager_password = forms.CharField(widget=forms.PasswordInput, required=True, label="Mật khẩu Quản lý")

    class Meta:
        model = BadmintonHall
        fields = ['name', 'address', 'manager_username', 'manager_email', 'manager_password']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        address = cleaned_data.get("address")
        manager_username = cleaned_data.get("manager_username")

        # Kiểm tra trùng lặp chi nhánh
        if BadmintonHall.objects.filter(name=name).exists():
            raise forms.ValidationError("Tên chi nhánh đã tồn tại!")
        if BadmintonHall.objects.filter(address=address).exists():
            raise forms.ValidationError("Địa điểm này đã có chi nhánh khác!")

        # Kiểm tra trùng lặp tài khoản quản lý
        if User.objects.filter(username=manager_username).exists():
            raise forms.ValidationError("Tên đăng nhập của Quản lý đã tồn tại!")

        return cleaned_data

    def save(self, commit=True):
        cleaned_data = self.cleaned_data

        # Tạo BadmintonHall nhưng chưa lưu ngay
        badminton_hall = super().save(commit=False)

        # Tạo User cho CourtManager
        user = User.objects.create_user(
            username=cleaned_data["manager_username"],
            email=cleaned_data["manager_email"],
            password=cleaned_data["manager_password"]
        )

        # Tạo PaymentAccount cho CourtManager
        payment_account = PaymentAccount.objects.create(
        accountHolder=user.username,
        accountNumber="000000",  # Placeholder, cập nhật khi có số tài khoản thực tế
        paymentMethod="bank"  # Sử dụng "bank" hoặc "momo"
)


        # Tạo CourtManager và liên kết với User & PaymentAccount
        court_manager = CourtManager.objects.create(
            user=user,
            payment_account=payment_account
        )

        # Gán CourtManager cho BadmintonHall và lưu vào DB
        badminton_hall.court_manager = court_manager
        if commit:
            badminton_hall.save()

        return badminton_hall

