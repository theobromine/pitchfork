from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^$', views.index, {'message': ""}, name="index"),
    # ex: /polls/5/
    url(r'^faq$', views.faq, name='faq'),
    url(r'^info', views.info, name='info'),
    url(r'^contact', views.contact, name='contact'),
    url(r'^paytest', views.paytest, name='paytest'),
    url(r'^paypal_return', views.paypal_return, name='paypal_return'),
    url(r'^invoice_confirmation/(?P<group_id>[0-9]+)', views.invoice_confirmation,
        name='invoice_confirmation'),

    url(r'^register$', views.reg_user, name='reg'),
    url(r'^signup$', views.reg_user, name='reg_user'),
    url(r'^login/$', auth_views.login, {'template_name': 'webapp/login.html'}, name='login'),
    url(r'^account_activation_sent/$', views.account_activation_sent,
        name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

    url(r'^userhome', views.user_home, name='userhome'),
    url(r'^logout/$', auth_views.logout,{'next_page': '/'}, name='logout'),
    url(r'^newgroup', views.new_group, name='newgroup'),
    url(r'^settings', views.settings, name='settings'),
    url(r'^grouphome/(?P<group_id>[0-9]+)', views.group_home, name='grouphome'),
    url(r'^grouphome/(?P<group_id>[0-9]+)/add', views.add, name='add'),
    url(r'^test', views.test, name='test')

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # urlpatterns += staticfiles(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
