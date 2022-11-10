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


        if request.GET.get('currency'):
            currency__ = request.GET.get('currency')
            print("featured_filter", currency__)
        #     listings = Currency.objects.filter(featured_choices=featured_filter)
        #     print("---------", featured_filter, listings)
        # else:
        #     listings = Currency.objects.all()

        # context_dict = {'listings': listings}

        # txt = request.POST.get('currency')
        # answer = request.GET['currency']
        # print("answer", answer)
        # print("TEXT", txt)
        # if request.method == 'POST':
        #     selected_value = request.POST.get('currency')
        #     print("selected_value", selected_value)
        currency = "AUDUSD"
        mydb.autocommit = True
        cursor = mydb.cursor()

        sql_query_buy = "SELECT buy from currency_buy_sell where currency = '" + currency + "' "
        cursor.execute(sql_query_buy)
        result = cursor.fetchall()
        sql_query_sell = "SELECT sell from currency_buy_sell where currency = '" + currency + "' "
        cursor.execute(sql_query_sell)
        result_sell = cursor.fetchall()
        print("result_sell", result_sell)

        if currency__ == '':
            sql_query_predicted_high_low = "select * from predicted_high_low"
        else:
            sql_query_predicted_high_low = "select * from predicted_high_low where currency = '" + currency__ + "'"

        cursor.execute(sql_query_predicted_high_low)
        result_high_low = cursor.fetchall()
        print("-----", result_high_low)


        sql_query_historical_data = "Select * from historical_data where currency = '" + currency + "' "
        cursor.execute(sql_query_historical_data)
        result_historical = cursor.fetchall()

        currency_ = Currency.objects.all()
        time_interval = Interval.objects.all()
        # sql_query_currency = "Select distinct currency from predicted_high_low"
        # cursor.execute(sql_query_currency)
        # currency_ = cursor.fetchall()
        # print("currency_", currency_)


        context = {
            "Buy": result,
            "Sell": result_sell,
            "high_low": result_high_low,
            "historical_data": result_historical,
            "Get_currency": currency_,
            "Get_interval": time_interval,
        }

        return render(request, 'chartjs/demo.html', context)
        # return render(request, context, template_name)

# def filter_data(request):
#     print("POST", request.POST)
#     print("Get", request.GET)


        # def leads_edit(request, id):
        #     leads = Currency.objects.get(id=id)
        #     context = {'leads': leads}
        #     template_name = 'file/edit.html'
        #     return render(request, template_name, context)
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