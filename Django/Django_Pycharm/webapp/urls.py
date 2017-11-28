from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views

urlpatterns = [
                  url(r'^$', views.index, name="index"),
                  # ex: /polls/5/
                  url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
                  # ex: /polls/5/results/
                  url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
                  # ex: /polls/5/vote/
                  url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
                  url(r'^$', views.reg_user, name='reg'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
