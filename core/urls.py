from django.conf.urls import url
from .views import ListingContent, CurrentArticle, ChangeUser, TestView

urlpatterns = [
	url(r'^$', ListingContent.as_view(), name='index_page'),
	url(r'^article/(?P<pk>\d+)/$', CurrentArticle.as_view(), name='current_article'),
	url(r'^change_user/(?P<user_id>\d+)/$', ChangeUser.as_view(), name='change_user'),
	url(r'^filter/(?P<q>\d+)/$', ListingContent.as_view(), name='filter_page'),
]
