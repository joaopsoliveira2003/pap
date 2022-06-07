from django.urls import path, include
from website.views import *
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/<str:username>/', profile, name='profile'),
    path('ticket-list/', ticketlist, name='ticketlist'),
    path('ticket-archive/', ticketarchive, name='ticketarchive'),
    path('files/', files, name='files'),
    path('contact-list/', contactlist, name='contactlist'),
    path('contact-archive/', contactarchive, name='contactarchive'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('admin/', admin, name="admin"),
    path('extension/', extension, name='extension'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', register, name='register')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)