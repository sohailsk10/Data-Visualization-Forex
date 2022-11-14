from django.shortcuts import render

from django.shortcuts import render
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
import psycopg2
from .serializers import *
from .models import *
from rest_framework import viewsets


class HomeView(View):
    def get(self, request, template_name = "index2.html",  *args, **kwargs):
        mydb = psycopg2.connect(
            database="postgres", user='postgres', password='admin', host='127.0.0.1', port='5432'
        )

        currency__ = ""
        interval__ = ""

        if request.GET.get('currency'):
            currency__ = request.GET.get('currency')
            print("Currency List", currency__)

        if request.GET.get('interval'):
            interval__ = request.GET.get('interval')
            interval__ = interval__+"Min"
            print("Time Interval", interval__)

        currency = "AUDUSD"
        time_interval = "15Min"
        mydb.autocommit = True
        cursor = mydb.cursor()

        if currency__ == '':
            sql_query_buy = "SELECT buy from currency_buy_sell where currency = '" + currency + "' "
        else:
            sql_query_buy = "SELECT buy from currency_buy_sell where currency = '" + currency__ + "' "
        cursor.execute(sql_query_buy)
        result_buy = cursor.fetchall()[0][0]
        print("result_buy", result_buy)

        if currency__ == '':
            sql_current_price = "SELECT current_price from currency_buy_sell where currency = '" + currency + "' "
        else:
            sql_current_price= "SELECT current_price from currency_buy_sell where currency = '" + currency__ + "' "
        cursor.execute(sql_current_price)
        result_current_price = cursor.fetchall()[0][0]
        print(result_current_price)

        if currency__ == '':
            sql_query_sell = "SELECT sell from currency_buy_sell where currency = '" + currency + "' "
        else:
            sql_query_sell = "SELECT sell from currency_buy_sell where currency = '" + currency__ + "' "
        cursor.execute(sql_query_sell)
        result_sell = cursor.fetchall()[0][0]
        print("result_sell", result_sell)

        if currency__ == '':
            sql_query_predicted_high_low = "select * from predicted_high_low"
        else:
            sql_query_predicted_high_low = "select * from predicted_high_low where currency = '" + currency__ + "'"



        cursor.execute(sql_query_predicted_high_low)
        result_high_low = cursor.fetchall()

        if currency__!='' and interval__=='':
            sql_query_historical_data = "Select * from historical_data where currency = '" + currency__ + "'"
        elif currency__!='' and interval__!='' :
            sql_query_historical_data = "Select * from historical_data where currency = '" + currency__ + "' and time_interval = '" + interval__ + "'"
        else:
            sql_query_historical_data = "Select * from historical_data"

        print("sql_query_historical_data", sql_query_historical_data)
        cursor.execute(sql_query_historical_data)
        result_historical = cursor.fetchall()

        currency_ = Currency.objects.all()
        time_interval = Interval.objects.all()
        print("Time Interval", time_interval)


        context = {
            "Buy": result_buy,
            "Sell": result_sell,
            "high_low": result_high_low,
            "historical_data": result_historical,
            "Get_currency": currency_,
            "Get_interval": time_interval,
            "currency":currency__,
            "current_price": result_current_price,
        }

        return render(request, 'chartjs/demo_v1.html', context)
        # return render(request, context, template_name)

# def filter_data(request):

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class IntervalViewSet(viewsets.ModelViewSet):
    queryset = Interval.objects.all()
    serializer_class = IntervalSerializer