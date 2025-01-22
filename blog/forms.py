from django import forms
from .models import Product, ProductImage


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class ProductAdminForm(forms.ModelForm):
    images_upload = forms.FileField(
        required=False,
        widget=MultipleFileInput(attrs={'multiple': True}),
        label="Upload multiple images"
    )

    class Meta:
        model = Product
        fields = [
            'category',
            'name',
            'short_description',
            'full_description',
            'contact',
            'price',
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        uploaded_files = self.files.getlist('images_upload')
        for f in uploaded_files:
            ProductImage.objects.create(product=instance, image=f)
        return instance
