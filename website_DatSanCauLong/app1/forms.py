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

        if not is_valid_email(username):
            errors['username'] = "Email không hợp lệ."

        if not User.objects.filter(username = username).exists():
            errors['username'] = "Người dùng không tồn tại."


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
class RegisterPaymentAccountForm(forms.Form):
    accountHolder = forms.CharField(
        label="Tên chủ tài khoản",
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nhập tên chủ tài khoản', 
            'required': True
        })
    )
    accountNumber = forms.CharField(
        label="Số tài khoản",
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nhập số tài khoản', 
            'required': True
        })
    )
    paymentMethod = forms.ChoiceField(
        label="Phương thức thanh toán",
        choices=[
            ("", "Chọn phương thức thanh toán"),
            ("bank", "Ngân hàng"),
            ("momo", "Momo")
        ],
        widget=forms.Select(attrs={'required': True})
    )

    def clean(self):
        cleaned_data = super().clean()
        accountHolder = cleaned_data.get("accountHolder").strip()
        accountNumber = cleaned_data.get("accountNumber").strip()
        paymentMethod = cleaned_data.get("paymentMethod")

        errors = {}

        if paymentMethod == "bank":
            if not re.match(r'^[A-Z\s]+$', accountHolder):
                errors['accountHolder'] = "Tên chủ tài khoản chỉ được chứa chữ cái in hoa và khoảng trắng."

            if not accountNumber.isdigit():
                errors['accountNumber'] = "Số tài khoản chỉ được chứa các chữ số."

            if len(accountNumber) < 9:
                errors['accountNumber'] = "Số tài khoản phải có ít nhất 9 chữ số."
        
        elif paymentMethod == "momo":
            if not re.match(r'^[A-Za-zÀ-ỹ\s]+$', accountHolder):
                errors['accountHolder'] = "Tên chủ tài khoản chỉ được chứa chữ cái in hoa, in thường, dấu và khoảng trắng."

            if not accountNumber.isdigit():
                errors['accountNumber'] = "Số tài khoản chỉ được chứa các chữ số."

            if len(accountNumber) < 10:
                errors['accountNumber'] = "Số tài khoản phải có ít nhất 10 chữ số."

        # Kiểm tra trùng số tài khoản
        if PaymentAccount.objects.filter(accountNumber=accountNumber, paymentMethod=paymentMethod).exists():
                errors['accountNumber'] = "Số tài khoản đã tồn tại."
        for field, error in errors.items():
            self.add_error(field, error)

        return cleaned_data  # Trả về dữ liệu đã làm sạch



# Tạo form cho TimeSlotTemplate(thêm khung thời gian và giá)
# class TimeSlotTemplateForm(forms.ModelForm):
#     class Meta:
#         model = TimeSlotTemplate
#         fields = ['day_of_week', 'time_frame', 'fixed_price', 'daily_price', 'flexible_price', 'status']

#Badmintonhall Form
from .models import BadmintonHall

class BadmintonHallForm(forms.ModelForm):
    class Meta:
        model = BadmintonHall
        fields = ['name', 'address']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        address = cleaned_data.get("address")

        if BadmintonHall.objects.filter(name=name).exists():
            raise forms.ValidationError("Tên chi nhánh đã tồn tại!")
        if BadmintonHall.objects.filter(address=address).exists():
            raise forms.ValidationError("Địa điểm này đã có chi nhánh khác!")
        return cleaned_data