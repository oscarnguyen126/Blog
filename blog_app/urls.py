from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('categories', views.category_create, name='categories'),
    path('categories/<int:id>', views.category_detail, name='categories_detail'),
    path('categories/<int:id>/update', views.update_category, name='update_category'),
    path('categories/<int:id>/delete', views.delete_category, name='delete_category'),
    path('tags/', views.create_tag, name='create_tag'),
    path('new/', views.create_blog, name='create_blog'),
    path('myblogs/', views.my_blog, name='my_blog'),
    path('myblogs/<int:id>', views.my_blog_detail, name='my_blog_detail'),
    path('myblogs/<int:id>/edit', views.my_blog_edit, name='my_blog_edit'),
    path('myblogs/<int:id>/delete', views.my_blog_delete),
    path('<int:id>', views.blog_detail, name='blog_detail'),
    path('<int:id>/edit/', views.edit_blog, name='edit_blog'),
    path('user/<int:id>/blogs', views.filter_by_user, name='filter_by_user'),
    path('user/<int:id>/blogs/<int:pk>', views.user_blog_detail, name='user_blog_detail')
]
