from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
                  url(r'^$', views.index, name="index"),
                  # ex: /polls/5/
                  url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
                  # ex: /polls/5/results/
                  url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
                  # ex: /polls/5/vote/
                  url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
                  url(r'^faq$', views.faq, name='faq'),
                  url(r'^info', views.info, name='info'),
                  url(r'^contact', views.contact, name='contact'),
                  url(r'^paytest', views.paytest, name='paytest'),
                  url(r'^submitToInvoice/(?P<groupID>[0-9]+)', views.submitToInvoice, name='submitToInvoice'),
                  url(r'^register$', views.reg_user, name='reg'),
                  url(r'^signup$', views.reg_user, name='reg_user'),
                  url(r'^login/$', auth_views.login, {'template_name': 'webapp/login.html'}, name='login'),
                  url(r'^account_activation_sent/$', views.account_activation_sent,
                      name='account_activation_sent'),
                  url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                      views.activate, name='activate'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
