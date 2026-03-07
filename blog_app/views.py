

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        messages.success(request, 'Account created successfully')
        return redirect('login')

    return render(request, 'register.html')




from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('blog_list')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'login.html')



def logout_view(request):
    logout(request)
    return redirect('login')










from .models import Blog
from .forms import BlogForm


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404




@login_required
def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'blog_list.html', {'blogs': blogs})


# @login_required
# def add_blog(request):
#     if request.method == 'POST':
#         form = BlogForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('blog_list')
#     else:
#         form = BlogForm()
#     return render(request, 'add_blog.html', {'form': form})



@login_required
def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user   #  imp
            blog.save()
            return redirect('blog_list')
    else:
        form = BlogForm()
    return render(request, 'add_blog.html', {'form': form})






# @login_required
# def edit_blog(request, id):
#     blog = get_object_or_404(Blog, id=id)

#     if request.method == 'POST':
#         form = BlogForm(request.POST, request.FILES, instance=blog)
#         if form.is_valid():
#             form.save()
#             return redirect('blog_list')
#     else:
#         form = BlogForm(instance=blog)

#     return render(request, 'edit_blog.html', {'form': form})




@login_required
def edit_blog(request, id):
    blog = get_object_or_404(Blog, id=id, author=request.user)

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_list')
    else:
        form = BlogForm(instance=blog)

    return render(request, 'edit_blog.html', {'form': form})





# @login_required
# def delete_blog(request, id):
#     blog = get_object_or_404(Blog, id=id)
#     blog.delete()
#     return redirect('blog_list')


@login_required
def delete_blog(request, id):
    blog = get_object_or_404(Blog, id=id, author=request.user)
    blog.delete()
    return redirect('blog_list')







import random
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Email not registered')
            return redirect('forgot_password')

        otp = random.randint(100000, 999999)

        # store otp in session
        request.session['reset_otp'] = otp
        request.session['reset_user'] = user.id

        send_mail(
            subject='Password Reset OTP',
            message=f'Your OTP is {otp}',
            from_email='aswinashok178@gmail.com',
            recipient_list=[email],
        )

        messages.success(request, 'OTP sent to your email')
        return redirect('reset_password')

    return render(request, 'forgot_password.html')




def reset_password(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('reset_password')

        if int(otp) != request.session.get('reset_otp'):
            messages.error(request, 'Invalid OTP')
            return redirect('reset_password')

        user_id = request.session.get('reset_user')
        user = User.objects.get(id=user_id)

        user.set_password(password1)
        user.save()

        # clear session
        del request.session['reset_otp']
        del request.session['reset_user']

        messages.success(request, 'Password reset successful')
        return redirect('login')

    return render(request, 'reset_password.html')












# get_object_or_404=
# It tries to get an object from the database
# If the object does not exist, it automatically returns a 404 error page
# Prevents your app from crashing




# from django.http  import HttpResponse
# def session_debug(request):
#     for key, value in request.session.items():
#         print(key, value)
#     return HttpResponse("Session data printed")



# from django.views.generic import ListView, CreateView, UpdateView, DeleteView
# from django.urls import reverse_lazy
# from .models import Blog
# from .forms import BlogForm



# class BlogListView(ListView):
#     model = Blog
#     template_name = 'blog_list.html'
#     context_object_name = 'blogs'



# class BlogCreateView(CreateView):
#     model = Blog
#     form_class = BlogForm
#     template_name = 'add_blog.html'
#     success_url = reverse_lazy('blog_list')




# class BlogUpdateView(UpdateView):
#     model = Blog
#     form_class = BlogForm
#     template_name = 'edit_blog.html'
#     success_url = reverse_lazy('blog_list')




# class BlogDeleteView(DeleteView):
#     model = Blog
#     template_name = 'delete_blog.html'
#     success_url = reverse_lazy('blog_list')



