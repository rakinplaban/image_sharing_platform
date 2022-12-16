from . import views

from django.urls import path
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('',views.index,name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("cat",views.categories,name="cat"),
    path("category/<str:slug>",views.category,name="category"),
    path("search/",views.search,name="search"),
    # path("add-wishlist",views.add_wishlist,name="add_wishlist"),
    # path("remove-wishlist",views.remove_wishlist,name="remove_wishlist"),
    path("like/",views.like,name="like"),
    path('reset_password/',views.reset_password,name="password_reset"),
    path('reset/<uidb64>/<token>',views.reset_password_confirm,name="password_reset_confirm"),
    path('share/<id>',views.shared_img,name="shared"),
    path('delete/<id>',views.delete_img,name="delete"),
    path('update/<id>',views.update_img,name="update"),
    path('add/',views.add_image,name="add"),
    path('adminpanel/',views.admin_panel,name="adminpanel"),
]