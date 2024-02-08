from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import DiaryEntry
from .forms import DiaryEntryForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.utils.dateparse import parse_date
from django.urls import reverse
from django.db.models.functions import TruncDay
from django.db.models import Count
import json
from django.utils.dateparse import parse_date
from django.utils.formats import date_format
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse

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
    success_url = 'diary_list/'  # ログイン成功後のリダイレクト先


# @login_required
# def diary_list(request):
#     # 日記が存在する日付のリストを取得
#     diary_dates = DiaryEntry.objects.filter(user=request.user).annotate(date_only=TruncDay('date')).values('date_only').distinct()
#     diary_dates_list = [entry['date_only'] for entry in diary_dates]
#     print(diary_dates_list)
#     entries = DiaryEntry.objects.filter(user=request.user).order_by('-date')
#     diary_dates_json = json.dumps(list(diary_dates))

#     return render(request, 'diary/diary_list.html', {'diary_dates_json': diary_dates_json})
    # return render(request, 'diary/diary_list.html', {'entries': entries, 'diary_dates': diary_dates_list})

@login_required
def diary_list(request):
    # diary_datesを取得するロジック
    diary_entries = DiaryEntry.objects.filter(user=request.user)
    diary_dates = diary_entries.annotate(date_only=TruncDay('date')).values_list('date_only', flat=True).distinct()

    # 日付オブジェクトを文字列に変換
    diary_dates_str = [date.strftime('%Y-%m-%d') for date in diary_dates]

    # 文字列のリストをJSONに変換
    diary_dates_json = json.dumps(diary_dates_str, cls=DjangoJSONEncoder)
    print(diary_dates_json)
    return render(request, 'diary/diary_list.html', {'diary_dates_json': diary_dates_json})



# @login_required
# def diary_create(request):
#     if request.method == 'POST':
#         form = DiaryEntryForm(request.POST)
#         if form.is_valid():
#             diary_entry = form.save(commit=False)
#             diary_entry.user = request.user
#             diary_entry.save()
#             return redirect('diary_list')
#     else:
#         form = DiaryEntryForm()
#     return render(request, 'diary/diary_form.html', {'form': form})

@login_required
def check_diary_entry(request):
    date_str = request.GET.get('date')
    date = parse_date(date_str)
    entry_exists = DiaryEntry.objects.filter(date=date, user=request.user).exists()

    if entry_exists:
        entry = DiaryEntry.objects.get(date=date, user=request.user)
        return HttpResponseRedirect(reverse('diary_edit', args=[entry.pk]))
    else:
        return HttpResponseRedirect(f'/diary/create/?date={date_str}')

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
        entry = get_object_or_404(DiaryEntry, pk=pk, user=request.user)
        formatted_date = date_format(entry.date, "Y年n月j日")
    return render(request, 'diary/diary_form.html', {'form': form, 'pk': pk, 'formatted_date': formatted_date})


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
        # クエリパラメータから日付を取得し、フォームの初期値に設定
        date_str = request.GET.get('date')
        initial = {}
        if date_str:
            date = parse_date(date_str)
            if date:
                initial['date'] = date  # フォームの日付フィールドの初期値として設定
        form = DiaryEntryForm(initial=initial)
        date_str = request.GET.get('date')
        date = parse_date(date_str) if date_str else None
        formatted_date = date_format(date, "Y年n月j日") if date else ''

    return render(request, 'diary/diary_form.html', {'form': form, 'formatted_date': formatted_date})

@login_required
def download_diary(request):
    # ユーザーの日記エントリを取得
    entries = DiaryEntry.objects.filter(user=request.user).order_by('date')
    # テキストファイルの内容を生成
    lines = ["{}, {}\n".format(entry.date.strftime('%Y-%m-%d'), entry.text) for entry in entries]
    content = "".join(lines)
    # レスポンスとしてテキストファイルを返す
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="diary_entries.txt"'
    return response