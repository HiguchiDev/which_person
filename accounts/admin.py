from django.contrib import admin

# admin.site.register(Book)
# admin.site.register(Impression)
from django.contrib.auth.models import User


"""
#django標準で用意されているので、下記はいらない
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password1', 'password2',)
    list_display_links = ('username', 'password1',)  # 修正リンクでクリックできる項目

admin.site.register(User, UserAdmin)
"""