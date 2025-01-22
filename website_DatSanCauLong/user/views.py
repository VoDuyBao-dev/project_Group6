from django.shortcuts import render
from django.contrib import messages
# from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

def loginUser(request):    
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # try:
        #     user = User.objects.get(username=username)
        # except:
        #     messages.error(request, "Username does not exist.")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username OR password is incorrect.")
    context = {'page' : page}
    return render(request, 'use/sign.html', context)