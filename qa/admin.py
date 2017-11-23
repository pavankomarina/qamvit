from django.contrib import admin


# Register your models here.
from .models import Userdetails,Questions,Tags,Answers,Blog,Like


admin.site.register(Userdetails)
admin.site.register(Questions)
admin.site.register(Tags)
admin.site.register(Answers)
admin.site.register(Blog)
admin.site.register(Like)

