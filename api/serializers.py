from cProfile import label
from email.mime import image
from unicodedata import category
from rest_framework import serializers
from stock_app.models import User,Role,Permission,Images,Categories,User_role,Role_permission,Image_category,Like
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from stock_app.models import Images,Categories,Image_category,User

class UserSerializer(serializers.ModelSerializer):
  url = serializers.HyperlinkedIdentityField(
    view_name='user_id',
  )
  class Meta:
    model = User
    fields = ["id", "full_name", "username", "phone","email","address","url"]
    def create(self, validated_data):
          user = User.objects.create(
          username=validated_data['username'],
          email=validated_data['email'],
          full_name=validated_data['full_name'],
          address=validated_data['address'],
          # status=validated_data['status'],
          phone=validated_data['phone'],
        )
          user.set_password(validated_data['password'])
          user.save()
          return user


#Serializer to Register User
class RegisterSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(
    required=True,
    validators=[UniqueValidator(queryset=User.objects.all())]
  )
  password = serializers.CharField(
    write_only=True, required=True, validators=[validate_password])
  confirmation = serializers.CharField(write_only=True, required=True)
  class Meta:
    model = User
    fields = ("full_name", "username", "phone","email","address", 'password', 'confirmation')
    extra_kwargs = {
      'full_name': {'required': True},
      'phone': {'required': False},
      'address': {'required': True},
      # 'status' : {'required':True},
    }
  def validate(self, attrs):
    if attrs['password'] != attrs['confirmation']:
      raise serializers.ValidationError(
        {"password": "Password fields didn't match."})
    return attrs
  def create(self, validated_data):
    user = User.objects.create(
      username=validated_data['username'],
      email=validated_data['email'],
      full_name=validated_data['full_name'],
      address=validated_data['address'],
      # status=validated_data['status'],
      phone=validated_data['phone'],
    )
    user.set_password(validated_data['password'])
    user.save()
    return user


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['full_name','username', 'phone' ,'address' ,'status' ,'email','password']

#         def create(self, validated_data):
#           user = User.objects.create(
#           username=validated_data['username'],
#           email=validated_data['email'],
#           full_name=validated_data['full_name'],
#           address=validated_data['address'],
#           # status=validated_data['status'],
#           phone=validated_data['phone'],
#         )
#           user.set_password(validated_data['password'])
#           user.save()
#           return user

class ImagesSerializer(serializers.ModelSerializer):
    url_img = serializers.HyperlinkedIdentityField(
      view_name='image',
    )
    user = serializers.SerializerMethodField()
    class Meta:
        model = Images
        fields = ['url_img','title','url', 'location' , 'description','user']

    def get_user(self,obj):
      return str(obj.user.username)


class CategoriesSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
      view_name='category-name',
      lookup_field='slug'
    )
    
    class Meta:
        model = Categories
        fields = ['url','name','parent', 'images']

    


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['name','status','slug']


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['name', 'status']

class User_roleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_role
        fields = ['user', 'role']


class Role_permissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role_permission
        fields = ['role','permission']
   


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    class Meta:
        model = Like
        fields = ['image','user', 'timestamp' ]
    
    def get_user(self,obj):
      return str(obj.user.username)

    def get_image(self,obj):
      return str(obj.image.title)


class Image_categorySerializer(serializers.ModelSerializer):
    # category = serializers.SerializerMethodField()
    # images = serializers.SerializerMethodField()
    class Meta:
        model = Image_category
        fields = ['images','category']

    # def get_category(self,obj):
    #   return str(obj.category.name)

    # def get_images(self,obj):
    #   return str(obj.images.title)


class Image_categoryDisplaySerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    class Meta:
        model = Image_category
        fields = ['images','category']

    def get_category(self,obj):
      return str(obj.category.name)

    def get_images(self,obj):
      return str(obj.images.title)