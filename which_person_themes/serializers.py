from rest_framework import serializers

from which_person_themes.models import Voting, Comment


class CommnetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'user_name', 'choice_num', 'comment', 'user_id')