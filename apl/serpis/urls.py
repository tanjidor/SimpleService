from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView



app_name 		= 'serpis'
urlpatterns 	= [
	path('', views.masuk, name='masuk'),
	path('logout/', LogoutView.as_view(next_page='serpis:masuk'), name="logout"),
	path('beranda/', views.beranda, name='beranda'),
	path('order/', views.orderan, name='orderan'),
	path('order/<int:pk>/edit/', views.orderan, name='orderan_edit'),

	#path('order/<int:pk>/detail/', views.OrderDetail.as_view(), name='orderan_detail'),
	path('order/<int:pk>/detail', views.orderan_detail, name='orderan_detail'),
]