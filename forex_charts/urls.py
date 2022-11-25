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
    path('home/', views.get_data, name= "get_data"),
    path('get_currency', views.get_currency, name= "get_currency"), 
    # path('get_current_price', views.get_current_price, name= "get_current_price"),
    # path('get_prediction_tbl', views.get_prediction_tbl, name= "get_prediction_tbl"),
    # path('get_buy_sell_gauge', views.get_buy_sell_gauge, name= "get_buy_sell_gauge"),
    # path('get_historical_tbl', views.get_historical_tbl, name= "get_historical_tbl"),
    # # path('v1/', include('forex_chartjs.urls')),

    # path('test-api', views.get_data),
    # path('api', views.ChartData.as_view()),
]
