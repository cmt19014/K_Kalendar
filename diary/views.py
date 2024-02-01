from django.shortcuts import render, redirect, get_object_or_404
from .models import DiaryEntry
from .forms import DiaryEntryForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .forms import SignUpForm
from django.contrib.auth import login, authenticate

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('diary_list')  # ユーザー登録後のリダイレクト先
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# 通常のユーザー向けのログインビュー
class UserLoginView(auth_views.LoginView):
    template_name = 'registration/user_login.html'  # ログインテンプレートのパスを指定

@login_required
def diary_list(request):
    entries = DiaryEntry.objects.filter(user=request.user).order_by('-date')
    return render(request, 'diary/diary_list.html', {'entries': entries})

@login_required
def diary_create(request):
    if request.method == 'POST':
        form = DiaryEntryForm(request.POST)
        if form.is_valid():
            diary_entry = form.save(commit=False)
            diary_entry.user = request.user
            diary_entry.save()
            return redirect('diary_list')
    else:
        form = DiaryEntryForm()
    return render(request, 'diary/diary_form.html', {'form': form})

@login_required
def diary_edit(request, pk):
    entry = get_object_or_404(DiaryEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        form = DiaryEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('diary_list')
    else:
        form = DiaryEntryForm(instance=entry)
    return render(request, 'diary/diary_form.html', {'form': form})
