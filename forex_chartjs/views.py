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
    def get(self, request, *args, **kwargs):
        mydb = psycopg2.connect(
            database="postgres", user='postgres', password='admin', host='127.0.0.1', port='5432'
        )
        currency = "AUDUSD"
        mydb.autocommit = True
        cursor = mydb.cursor()

        sql_query_buy = "SELECT buy from currency_buy_sell where currency = '" + currency + "' "
        cursor.execute(sql_query_buy)
        result = cursor.fetchall()[0][0]
        sql_query_sell = "SELECT sell from currency_buy_sell where currency = '" + currency + "' "
        cursor.execute(sql_query_sell)
        result_sell = cursor.fetchall()[0][0]

        sql_query_predicted_high_low = "select * from predicted_high_low where currency = '" + currency + "' "
        cursor.execute(sql_query_predicted_high_low)
        result_high_low = cursor.fetchall()

        sql_query_historical_data = "Select * from historical_data where currency = '" + currency + "' "
        cursor.execute(sql_query_historical_data)
        result_historical = cursor.fetchall()

        currency_ = Currency.objects.all()

        context = {
            "Buy": result,
            "Sell": result_sell,
            "high_low": result_high_low,
            "historical_data": result_historical,
            "Get_currency": currency_
        }

        return render(request, 'chartjs/index2.html', context)
        # return Response(result)
        # return render(request, 'chartjs/index2.html')

    # def get_data(self,request, format = None):
    #
    #     currency = "AUDUSD"
    #     mydb = psycopg2.connect(
    #         database="postgres", user='postgres', password='admin', host='127.0.0.1', port='5432'
    #     )
    #     print(mydb)
    #     mydb.autocommit = True
    #     cursor = mydb.cursor()
    #     sql_query = "SELECT buy from currency_buy_sell where currency = '"+currency+"' "
    #     print(sql_query)
    #     cursor.execute(sql_query)
    #     result = cursor.fetchall()
    #     print("RESULT", result)
    #     return Response(result)

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class IntervalViewSet(viewsets.ModelViewSet):
    queryset = Interval.objects.all()
    serializer_class = IntervalSerializer