import response as response
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.views.generic import ListView
from rest_framework.generics import get_object_or_404

from .forms import UserCreationForm, ProfileForm
from .models import User


# 비밀번호 변경 기능
from .serializers import UserSerializer


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, '패스워드가 성공적으로 업데이트 되었습니다.')
            return redirect('index') # 다음 url로 이동한다.
        else:
            messages.error(request,"다음 에러를 확인해주세요.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html',{'form':form})

# 계정 삭제 기능
@login_required
def delete(request):
    if request.method == "POST":
        request.User.delete()
        return redirect('index')
    return redirect('index')


# New User Registration(회원가입 기능)
def create_user(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password1']
            new_user = User.objects.create_user(username, email, password)
            new_user.save()
            return render(request, 'registration/signup_done.html', {'message': '회원가입이 완료되었습니다.'})
        except:
            return render(request, 'registration/signup_done.html', {'message': '회원이 이미 있음'})
    else:
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})

# 로그아웃 기능
def sign_out(request):
    logout(request)
    return render(request, 'home/base.html')

# 로그인 기능
def sign_in(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username', ''),
                            password=request.POST.get('password', ''))
        if user is not None:
            login(request, user)
            return render(request, 'registration/signup_done.html', {'message': "로그인 되었습니다."})
        else:
            return render(request, 'registration/signup_done.html', {'message': "로그인에 실패하였습니다."})
    else:
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

# User profile (프로필 편집 기능)
def profile(request):
    if request.method == 'GET':
        # form = ImageUploadForm(request.POST, request.FILES)
        return render(request, 'registration/mypage.html') #{'form': form }

    elif request.method == 'POST':
        user = request.user
        # 이미지 저장하기
        # form = ImageUploadForm(request.POST, request.FILES)
        # if form.is_valid():
        #     user.photo = form.cleaned_data['image']
        #     user.save()

        text = request.POST.get('text')
        email = request.POST.get('email')
        birth_date = request.POST.get('birth_date')
        photo = request.POST.get('photo')
        phone_number = request.POST.get('phone_number')
        website = request.POST.get('website')

        user.bio = text
        user.email = email
        user.phone_number = phone_number
        user.website = website

        # 값이 존재할 때만 넣어줌으로써, Validation Error 해결 !
        if birth_date :
            user.date_of_birth = birth_date
        if photo :
            user.photo = photo

        user.save()

        return redirect('member/profile', user)


def profile_update(request):
    user = request.user
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=user)
        if profile_form.is_valid():
            profile_form.save()
        return redirect('people', request.user.username)
    else:
        profile_form = ProfileForm(instance=user)
    return render(request, 'profile/profile_update.html', {'profile_form': profile_form})


class UserList(ListView):
    model = User
    template_name_suffix="_list"

# 게시물의 작성자의 username을 통해 user 페이지에 접근하기

def peoplePage(request,username):
    person = get_object_or_404(User, username=username)
    # serializer = UserSerializer(person)
    # return response(serializer.data)
    person = request.user
    return render(request, "profile/people.html",{'people': person})


def follow(request, user_id):
    people = get_object_or_404(get_user_model(), id=user_id)
    if request.user in people.followers.all():
        # people을 unfollow하기
        people.followers.remove(request.user)
    else:
        # people을 follow하기
        people.followers.add(request.user)
    return redirect('people')

# class Following():
#
#     def get(self, request, *args, pk):
#         if not request.user.is_authenticated:
#             return redirect('login/')
#         else:
#             user = request.user
#             opponent = User.objects.get(pk=pk)
#             if user != opponent:
#                 if not Follow.objects.filter(who=user):
#                     Follow.objects.create(who=user)
#                 if not Follow.objects.filter(who=opponent):
#                     Follow.objects.create(who=user)
#                 I =  Follow.objects.get(who=user.id)
#                 You = Follow.objects.get(who=opponent.id)
#
#                 if str(opponent.id) not in I.following.split():
#                     pass
#
#
#
# def Unfollow():
#     return None
# def peoplePage2(request, pk):
#     people = get_object_or_404(get_user_model(), id=pk)
#     return render(request, "profile/people.html",{'people': people})