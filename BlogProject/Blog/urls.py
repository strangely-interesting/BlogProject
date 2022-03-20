from django.urls import path
from . import views

app_name = 'Blog'
urlpatterns = [
    path('',views.index,name='index'),
    path('home/', views.PostListView.as_view(), name='home'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_details'),
    path('post/new/', views.PostCreateView.as_view(), name='create_post'),
    path('post/edit/<int:pk>/', views.PostEditView.as_view(), name='edit_post'),
    path('post/delete/<int:pk>/', views.PostDelete.as_view(), name='delete_post'),
    path('like_post/', views.like_post, name='like_post'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('unread/',views.unread,name='unread'),
    path('mark_read/', views.mark_read, name='mark_read'),
    path('mark_all_read/', views.mark_all_read, name='mark_all_read'),
    path('most_liked/', views.get_most_liked, name='most_liked'),
]