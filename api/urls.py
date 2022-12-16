from django.urls import path
from . import views
from .views import UserDetailAPI,RegisterUserAPIView,UsertList,UserDetail,ImagesList,ImagesDetail,CategoriesList,CategoriesDetail,Image_categorytList,Image_categoryDetail,LikeList,LikeDetail
urlpatterns = [
  path("get-details",UserDetailAPI.as_view()),
  path('apiregister',RegisterUserAPIView.as_view()),
  path('user/', views.UsertList.as_view(),name="userlist"),
  path('user/<int:pk>/', views.UserDetail.as_view(),name="user_id"),
  path('image/', views.ImagesList.as_view(),name='all_images'),
  path('image/<int:pk>/', views.ImagesDetail.as_view(),name='image'),
  path('category/', views.CategoriesList.as_view(),name='categories'),
  path('category_name/<str:slug>/', views.CategoriesDetail.as_view(),name='category-name'),
  path('image-category/', views.Image_categorytList.as_view()),
  path('image-category/<int:pk>/', views.Image_categoryDetail.as_view()),
  path('likeapi/',views.LikeList.as_view()),
  path('likeapi/<int:pk>/',views.LikeDetail.as_view()),
  path('display-category/',views.Image_category_display.as_view(),name='display-category')
]