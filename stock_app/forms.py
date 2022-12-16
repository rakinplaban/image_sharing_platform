
from tkinter.tix import Select
from typing_extensions import Required
from django import forms

from .models import Images, Categories

class Img_form(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['title','location', 'description','url' ]

        labels = {
            'title' : 'Title*',
            'location' : 'Location',
            'description' : 'Description*',
            'url' : '',
        }

        widgets = {
            'title' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Title of image',
                'rows' : 1,
                'cols' : 100,
                'type' : 'text'
            }),

            'url' : forms.ClearableFileInput(attrs={
                'class' : 'dropify',
                'rows' : 1,
                'cols' : 100,
                'type' : 'file',
                'multiple' : True,
                'data-height' : 100,
                # 'id' : 'upload_custom',
            }),

            'location' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'location',
                'rows' : 1,
                'cols' : 100,
                'type' : 'text',
            }),

            'description' : forms.Textarea(attrs={
                'class' : 'form-control',
                'placeholder' : 'Tell something about..',
                'rows' : 3,
                'cols' : 100,
                'type' : 'textarea'
            }),
        }




class Cat_form(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['name', 'slug', 'parent']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['parent'] = Categories.objects.all()

        labels = {
            'name' : 'Name',
            'slug' : 'URL',
            'parent' : 'Parent'
        }

        widgets = {
            'name' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Title of Category',
                'rows' : 1,
                'cols' : 100,
                'type' : 'text'
            }),

            'slug' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Short URL of image',
                'rows' : 1,
                'cols' : 100,
                'type' : 'text'
            }),

            # 'parent' : forms.Select(attrs={
            #     'class' : 'dropdown-toggle',
            #     'type' : 'select'
            # }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].widget.attrs.update({"class": "form-control"})
        # or iterate over field to add class for each field
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':"form-control"})