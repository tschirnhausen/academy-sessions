from django.urls import path

from core.views import TestView, FlushView

urlpatterns = [
    path('', TestView.as_view(), name='index'),
    path('flush/', FlushView.as_view(), name='flush')
]