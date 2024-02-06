from django.urls import path
from . import views

urlpatterns = [
    path('diary_list/', views.diary_list, name='diary_list'), 
    # path('', views.diary_list, name='diary_list'),  # 日記エントリの一覧
    path('check_entry/', views.check_diary_entry, name='check_diary_entry'),
    path('create/', views.diary_create, name='diary_create'),  # 新規エントリの作成
    path('edit/<int:pk>/', views.diary_edit, name='diary_edit'),  # エントリの編集
    path('signup/', views.signup, name='signup'),
    # 他のURLパターンも必要に応じて追加
]
