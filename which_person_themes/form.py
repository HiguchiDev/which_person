from django.forms import ModelForm

from which_person_themes.models import Theme


class ThemeForm(ModelForm):

    class Meta:
        model = Theme
        fields = ('name', 'major_class', 'medium_class', 'choice1', 'choice2',)