from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.template.context_processors import csrf
from django.views.generic import DetailView, ListView, TemplateView
from .models import Content, Comments, Reviews
import json
# Create your views here.

class ListingContent(ListView):
    template_name='index.html'
    queryset = Content.objects.all()

    def get(self, request, *args, **kwargs):
        filter_condition = self.kwargs.get('q', None)
        if filter_condition:
            self.queryset = self.queryset.filter(content_type=filter_condition)
        return super(ListingContent, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ListingContent, self).get_context_data(*args, **kwargs)
        qs = self.get_queryset()
        context['news_count'] = qs.filter(content_type=1).count()
        context['articles_count'] = qs.filter(content_type=0).count()
        return context

class CurrentArticle(DetailView):
    template_name = 'article.html'
    model = Content
    context_object_name = 'article'

    def post(self, request, *args, **kwargs):
        txt = request.POST.get('text_comment', None)
        if txt:
            content_id = self.kwargs.get('pk', None)
            if content_id:
                content = Content.objects.filter(pk=content_id).only('id').first()
                user = request.session.get('user', None)
                author = user if not user else User.objects.filter(pk=user.get('id')).only('id').first()
                new_comment = Comments(author=author, content=content, text=txt)
                new_comment.save()
            else:
                return Http404
        return super(CurrentArticle, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(CurrentArticle, self).get_context_data(*args, **kwargs)
        context['comment_list'] = Comments.objects.filter(content=self.object)
        context.update(csrf(self.request))
        return context

    def ajax_response(self, context, **response_kwargs):
        active_user = self.request.session.get('user', None)
        if not active_user:
            return HttpResponse('')
        else:
            user_id = active_user.get('id', None)
            if self.request.GET.get('t_content', 'article') == 'article':
                content_id = self.object.pk
                content_type = 0
            else:
                content_id = self.request.GET.get('comment_id', None)
                content_type = 1
            reviews = Reviews.objects.filter(content_type=content_type, user_id=user_id,
                                              content_id=content_id).first()
            like = True if self.request.GET.get('t_like') == 'positive' else False
            if not reviews:
                reviews = Reviews(user_id=user_id, content_id=content_id,
                                content_type=content_type)
            state_likes = reviews.add_like(like)
            return HttpResponse(json.dumps(state_likes))

    def render_to_response(self, context, **response_kwargs):
        if not self.request.is_ajax():
            response = super(CurrentArticle, self).render_to_response(context, **response_kwargs)
        else:
            response = self.ajax_response(context, **response_kwargs)
        return response

class ChangeUser(TemplateView):
    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id', None)
        if user_id:
            self.request.session['user'] = User.objects.filter(pk=user_id).values('id','username').first()
        return redirect ('/')

class TestView(TemplateView):
    test_var=None
    def get(self, request, *args, **kwargs):
        import ipdb; ipdb.set_trace()
        return super(TestView, self).get(self, request, *args, **kwargs)
