"""forex_charts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from forex_chartjs import views
# from forex_charts.views import *
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view()),
    path('v1/', include('forex_chartjs.urls')),
    # path('test-api', views.get_data),
    # path('api', views.ChartData.as_view()),
]
