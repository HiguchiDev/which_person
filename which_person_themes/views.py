import json
import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views.generic.base import View
from django.core import serializers
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from which_person_themes.form import ThemeForm
from which_person_themes.models import Theme, Voting, Comment
from which_person_themes.serializers import CommnetSerializer


def themes_list(request):
    """書籍の一覧"""
    # return HttpResponse('書籍の一覧')
    themes = Theme.objects.all().order_by('id')
    return render(request,
                  'theme_list.html',  # 使用するテンプレート
                  {'themes': themes})  # テンプレートに渡すデータ


class ThemeCanceler(View):
    def get(self, request, *args, **kwargs):
        try:
            theme_id = kwargs['theme_id']
        except KeyError:
            theme_id = None

        if theme_id and request.user is not None and Theme.objects.filter(pk=theme_id,
                                                                          user_id=request.user.id).exists():
            Theme.objects.filter(pk=theme_id, user_id=request.user.id).delete()

        return redirect('which_person_themes:home')


class ThemeEditer(View):
    def get(self, request, *args, **kwargs):
        try:
            theme_id = kwargs['theme_id']
        except KeyError:
            theme_id = None

        if theme_id:
            theme = get_object_or_404(Theme, pk=theme_id)
        else:
            theme = Theme()

        form = ThemeForm(instance=theme)

        return render(request, 'theme_edit.html', dict(form=form, theme_id=theme_id))

    def post(self, request, *args, **kwargs):
        try:
            theme_id = kwargs['theme_id']
        except KeyError:
            theme_id = None

        if theme_id:
            theme = get_object_or_404(Theme, pk=theme_id)
        else:
            theme = Theme()

        form = ThemeForm(request.POST, instance=theme)  # POST された request データからフォームを作成

        user = request.user

        if form.is_valid() and user is not None:  # フォームのバリデーション
            theme = form.save(commit=False)
            theme.user = user
            theme.save()

            return redirect('which_person_themes:home')

        return render(request, 'theme_edit.html', dict(form=form, theme_id=theme_id))


class Vote(LoginRequiredMixin, View):

    # @login_required
    def get(self, request, *args, **kwargs):

        try:
            theme_id = kwargs['theme_id']
        except KeyError:
            theme_id = -1

        theme = get_object_or_404(Theme, pk=theme_id)

        param = {'theme': theme, 'user_id': request.user.id}

        return render(request, 'which.html', param)


class VoteQtyGetAPI(LoginRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):
        try:
            theme_id = kwargs['theme_id']
        except KeyError:
            result = {"get_success": False}
            return Response(result)

        choice1_qty = Voting.objects.filter(theme_id=theme_id, choice_num=1).count()
        choice2_qty = Voting.objects.filter(theme_id=theme_id, choice_num=2).count()

        result = {"get_success": True, "choice1_qty": choice1_qty, "choice2_qty": choice2_qty}
        return Response(result)


class VoteingAPI(LoginRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):

        try:
            theme_id = kwargs['theme_id']
            choice_num = kwargs['choice_num']
        except KeyError:
            result = {"processing_success": False}
            return Response(result)

        theme = get_object_or_404(Theme, pk=theme_id)
        user = request.user

        voted = False
        if not Voting.objects.filter(theme_id=theme_id, user_id=user.id).exists():
            voting = Voting()
            voting.theme = theme
            voting.user = user
            voting.choice_num = choice_num
            voting.save()
            voted = True

        result = {"processing_success": True, "voted": voted}
        return Response(result)


class CanVoteingAPI(LoginRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):
        try:
            theme_id = kwargs['theme_id']
        except KeyError:
            result = {"processing_success": False, "canVote": False}
            return Response(result)

        # ↓filterで取得しているが、実質1件となるはず。ひとつのお題に対して、1ユーザは1回までしか投票できないように制御済み
        if Voting.objects.filter(theme_id=theme_id, user_id=request.user.id).exists():
            vote = Voting.objects.filter(theme_id=theme_id, user_id=request.user.id)
            result = {"processing_success": True, "canVote": False, "choice_num": vote[0].choice_num}
            return Response(result)

        result = {"processing_success": True, "canVote": True}
        return Response(result)


class CancelVoteAPI(LoginRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):
        try:
            theme_id = kwargs['theme_id']
        except KeyError:
            result = {"processing_success": False, "isCanceled": False}
            return Response(result)

        # ↓filterで取得しているが、実質1件となるはず。ひとつのお題に対して、1ユーザは1回までしか投票できないように制御済み
        if Voting.objects.filter(theme_id=theme_id, user_id=request.user.id).exists():
            deletingVote = Voting.objects.filter(theme_id=theme_id, user_id=request.user.id)
            deletingChoiceNum = deletingVote[0].choice_num

            Voting.objects.filter(theme_id=theme_id, user_id=request.user.id).delete()

            result = {"processing_success": True, "isCanceled": True, "canceledChoiceNum": deletingChoiceNum}
            return Response(result)

        result = {"processing_success": True, "isCanceled": False}
        return Response(result)


class CommentPostAPI(LoginRequiredMixin, APIView):
    def post(self, request, *args, **kwargs):
        theme_id = request.POST.get("theme_id")
        input_text = request.POST.get("input_text")

        logging.debug("theme_id : " + theme_id)
        logging.debug("input_text : " + input_text)

        theme = get_object_or_404(Theme, pk=theme_id)
        vote = get_object_or_404(Voting, theme_id=theme_id, user_id=request.user.id)

        if input_text:
            comment = Comment()
            comment.theme = theme
            comment.choice_num = vote.choice_num
            comment.user_name = request.user.username
            comment.comment = input_text
            comment.user = request.user
            comment.save()

            serializer = CommnetSerializer(comment)
            return JsonResponse(serializer.data)


class CommentCancelAPI(LoginRequiredMixin, APIView):
    def post(self, request, *args, **kwargs):
        comment_id = request.POST.get("comment_id")

        isCanceled = False

        if Comment.objects.filter(pk=comment_id, user_id=request.user.id).exists():
            Comment.objects.filter(pk=comment_id, user_id=request.user.id).delete()
            isCanceled = True

        result = {"isCanceled": isCanceled, "comment_id": comment_id}
        return Response(result)


class CommentListGetAPI(LoginRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):
        try:
            theme_id = kwargs['theme_id']
        except KeyError:
            return JsonResponse({})

        dict = {}
        if Comment.objects.filter(theme_id=theme_id).exists():
            comments = Comment.objects.filter(theme_id=theme_id)

            for i, comment in enumerate(comments):
                dict[i] = CommnetSerializer(comment).data

        return JsonResponse(dict)
