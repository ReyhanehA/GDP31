from django.conf.urls import patterns, url
from omblog.feeds import PostFeed


urlpatterns = patterns(
    '',
    url(r'^feed\.rss$', PostFeed(), name='feed'),

    url(r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'omblog/login.html'},
        name='login'),

    url(r'^attach/delete/$',
        'omblog.views.attach_delete',
        name='attach_delete'),

    url(r'^attach/$',
        'omblog.views.attach',
        name='attach'),

    url(r'^create/$',
        'omblog.views.create',
        name='create'),

    url(r'^edit/(?P<pk>\d+)/$',
        'omblog.views.edit',
        name='edit'),

    url(r'^tags/(?P<slug>[\w\-]+)/$',
        'omblog.views.tag',
        name='tag'),

    url(r'^(?P<slug>[\w\-]+)/edit/$',
        'omblog.views.redirect_edit',
        name='edit_redirect'),

    url(r'^(?P<slug>[\w\-]+)/$',
        'omblog.views.post',
        name='post'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        'omblog.views.month',
        name='month'),

    url(r'^$',
        'omblog.views.index',
        name='index'),
)
