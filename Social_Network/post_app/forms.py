# from django import forms
# from .models import Post, Tag, PostImage, PostLink, PostView
# from PIL import Image
# from io import BytesIO
# from django.core.files.base import ContentFile
# 
# 
# class MultipleFileInput(forms.ClearableFileInput):
#     allow_multiple_selected = True
# 
# class MultipleFileField(forms.FileField):
#     def clean(self, data, initial = True):
#         single_file_clean = super().clean
# 
#         if isinstance(data, (list, tuple)):
#             return [single_file_clean(file, initial) for file in data]
#         
#         return single_file_clean(data, initial)
# 
# class PostForm(forms.ModelForm):
#     tags = forms.ModelMultipleChoiceField(
#         label = "Теги",
#         required = False,
#         queryset= Tag.objects.all(),
#         widget = forms.CheckboxSelectMultiple
#     )
# 
#     images = MultipleFileField(
#         label= "Зображення",
#         required=False,
#         widget = MultipleFileInput
#     )
# 
#     class Meta:
#         model = Post
#         fields = ("title", "topic", "content")
#         labels = {
#             "title": "Заголовок публікації",
#             "topic": "Тема публікації",
#             "content": "Контент публікації"
#         }
# 
#     def __init__(self, *args, links = None, images = None, **kwargs):
#         super().__init__(*args, **kwargs)
# 
#         self.fields['tags'].queryset = Tag.objects.all()
# 
#         self.links_list = []
#         self.images_list = []
# 
#         if links is None:
#             links = []
# 
#         for link in links:
#             clean_link = link.strip() 
# 
#             if clean_link:
#                 self.links_list.append(clean_link)
# 
#         if images is not None:
#             self.images_list = list(images)
# 
#     def clean(self):
#         cleaned_data = super().clean()
# 
#         url_field = forms.URLField()
#         image_field = forms.ImageField()
# 
#         for link in self.links_list:
#             try:
#                 url_field.clean(link)
#             except forms.ValidationError:
#                 self.add_error(None, "Некоректний формат посилання")
# 
#         for image in self.images_list:
#             try:
#                 image_field.clean(image)
#             except forms.ValidationError:
#                 self.add_error(None, "Некоретний файл зображення")
# 
#         return cleaned_data
#     
#     def save(self, author, commit=True):
#         post = super().save(commit=False)
#         post.author = author
# 
#         if commit:
#             post.save()
#             post.tags.set(self.cleaned_data["tags"])
# 
#             for url in self.links_list:
#                 PostLink.objects.create(post=post, url=url)
# 
#             for image in self.images_list:
#                 PostImage.objects.create(
#                     post=post,
#                     original = image,
#                     compressed = self.compress_image(image)
#                 )
#         return post
#     
#     def compress_image(self, image):
#         
#         image.seek(0)
#         image_obj = Image.open(image)
# 
#         image_obj = image_obj.convert("RGB")
# 
#         quality = 85
#         width, height = image_obj.size
# 
#         MAX_COMPRESSED_IMAGE_SIZE = 5 * 1024 * 1024
# 
#         while True:
#             buffer = BytesIO()
#             image_obj.save(buffer, format="JPEG", quality = quality, optimize= True)
# 
#             if buffer.tell() <= MAX_COMPRESSED_IMAGE_SIZE:
#                 break
# 
#             if quality > 35:
#                 quality -= 10
#             else:
#                 if width <= 1 or height <= 1:
#                     break
# 
#                 width = int(width * 0.9)
#                 height = int(height * 0.9)
#                 image_obj = image_obj.resize((width, height), Image.Resampling.LANCZOS)
# 
#             # image.seek(0)
#         compressed_name = f"compressed_{image.name.rsplit('.', 1)[0]}.jpg"
#         return ContentFile(buffer.getvalue(), name=compressed_name)