from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.views.generic import RedirectView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('messages/', include('django_messages.urls')),
]

from test_django.core import views
app_name = "messages"

urlpatterns += [
    path('api/<int:pk>', views.MessageView.as_view()),
    path('api_un_read/<int:pk>', views.MessageUnreadView.as_view()),
    path('api_message/<int:pk>', views.MessageLastView.as_view()),
    path('api_create/', views.MessageCreateView.as_view()),
    path('api_del/<int:id_u>-<int:pk>', views.MessageDelView.as_view()),
]
