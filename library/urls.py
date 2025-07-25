from django.urls import path  
from .import views  
from django.views.generic import TemplateView 

urlpatterns = [  
    path('', views.Home, name='Home'),  
    path('home1/', TemplateView.as_view(template_name='library/home1.html'), name='home1'),
    path('Home/', TemplateView.as_view(template_name='library/Home.html'), name='Home'),
    path('submit/', views.submit_page, name='submit_data'),
    path('books/search/', TemplateView.as_view(template_name='library/searchbook.html'), name='searchbook'),
    path('books/view/', TemplateView.as_view(template_name='library/viewbooks.html'), name='viewbooks'),
    path('books/issue/', TemplateView.as_view(template_name='library/issuebook.html'), name='issuebook'),
    path('books/return/', views.returnbook, name='returnbook'),
    path('auth/login/', TemplateView.as_view(template_name='library/login.html'), name='login'),
    path('auth/register/', TemplateView.as_view(template_name='library/registeration.html'), name='registeration'),
]