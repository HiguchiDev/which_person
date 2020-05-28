from django.conf.urls import url
from django.contrib.auth import logout
from django.urls import path
from which_person_themes import views

app_name = 'which_person_themes'
urlpatterns = [
    path('', views.themes_list, name='home'),
    path('add/', views.ThemeEditer.as_view(), name='add'),  # 登録
    path('mod/<int:theme_id>/', views.ThemeEditer.as_view(), name='mod'),  # 修正
    path('which/<int:theme_id>/', views.Vote.as_view(), name='which'),
    path('which/cancel/<int:theme_id>/', views.ThemeCanceler.as_view(), name='which_cancel'),
    path('which/voting/<int:theme_id>/<int:choice_num>/', views.VoteingAPI.as_view(), name='voting_api'),
    path('which/can_voting/<int:theme_id>/', views.CanVoteingAPI.as_view(), name='can_voting_api'),
    path('which/vote_qty/<int:theme_id>/', views.VoteQtyGetAPI.as_view(), name='vote_qty_api'),
    path('which/vote_cancel/<int:theme_id>/', views.CancelVoteAPI.as_view(), name='vote_cancel_api'),
    path('which/comment_post/', views.CommentPostAPI.as_view(), name='comment_post_api'),
    path('which/comment_cancel/', views.CommentCancelAPI.as_view(), name='comment_cancel_api'),
    path('which/comment_list/<int:theme_id>/', views.CommentListGetAPI.as_view(), name='comment_list_api'),

]