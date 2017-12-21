from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from django.views.generic.base import TemplateView

app_name = 'webapp'
urlpatterns = [
    path('', views.index, {'message': ""}, name="index"),
    # ex: /polls/5/
    path('faq', views.faq, name='faq'),
    path('info', views.info, name='info'),
    path('contact', views.contact, name='contact'),
    path(r'^paytest', views.paytest, name='paytest'),
    path(r'^paypal_return', views.paypal_return, name='paypal_return'),
    path(r'^invoice_confirmation/(?P<group_id>[0-9]+)', views.invoice_confirmation,
         name='invoice_confirmation'),

    path(r'^register$', views.reg_user, name='reg'),
    path(r'^signup$', views.reg_user, name='reg_user'),
    path(r'^login/$', auth_views.login, {'template_name': 'webapp/login.html'}, name='login'),
    path(r'^account_activation_sent/$', views.account_activation_sent,
         name='account_activation_sent'),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
         views.activate, name='activate'),

    path('userhome', views.user_home, name='userhome'),
    path('logout', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('newgroup', views.new_group, name='newgroup'),
    path(r'^settings', views.settings, name='settings'),
    path(r'^grouphome/(?P<group_id>[0-9]+)', views.group_home, name='grouphome'),
    path(r'^grouphome/(?P<group_id>[0-9]+)/add', views.add, name='add'),
    path(r'^test', views.test, name='test')

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # urlpatterns += staticfiles(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
