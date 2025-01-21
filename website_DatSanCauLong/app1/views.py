from django.shortcuts import render


# Create your views here.
def Sign_in(request):
    return render(request, 'app1/Sign_in.html')

def Sign_up(request):
    return render(request, 'app1/Sign_up.html')

def Forgot_password(request):
    return render(request, 'app1/Forgot_password.html')

def New_password(request):
    return render(request, 'app1/New_password.html')


