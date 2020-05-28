from django.contrib import admin

# Register your models here.
from which_person_themes.models import Theme, Voting


class ThemeAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'major_class', 'medium_class', 'choice1', 'choice2',)  # 一覧に出したい項目

admin.site.register(Theme, ThemeAdmin)

class VotingAdmin(admin.ModelAdmin):

    list_display = ('id', 'user_id',  'theme_id', 'choice_num',)  # 一覧に出したい項目

admin.site.register(Voting, VotingAdmin)