from django.conf.urls.defaults import *
import views
#Blog related url patters

urlpatterns = patterns('blog.views',
	(r'^$',                                  'blog_default'),
	(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'month_view'),
	(r'^blog_id/(?P<blog_id>\d+)/$',         'blog_single'),
)