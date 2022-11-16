from django.http import JsonResponse
from django.shortcuts import render

from django.shortcuts import render
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
import psycopg2
from .serializers import *
from .models import *
from rest_framework import viewsets


def get_data(request):
    mydb = psycopg2.connect(
        database="postgres", user='postgres', password='admin', host='127.0.0.1', port='5432')

    currency__ = ""
    interval__ = ""

    if request.GET.get('currency'):
        currency__ = request.GET.get('currency')

    if request.GET.get('interval'):
        interval__ = request.GET.get('interval')
        interval__ = interval__ + "Min"

    currency = "AUDUSD"
    time_interval = "15Min"
    mydb.autocommit = True
    cursor = mydb.cursor()

    if currency__ == '':
        sql_current_price = "SELECT current_price from currency_buy_sell where currency = '" + currency + "' "
    else:
        sql_current_price = "SELECT current_price from currency_buy_sell where currency = '" + currency__ + "' "
    cursor.execute(sql_current_price)
    result_current_price = cursor.fetchall()[0][0]

    if currency__ == '':
        sql_query_buy = "SELECT buy from currency_buy_sell where currency = '" + currency + "' "
    else:
        sql_query_buy = "SELECT buy from currency_buy_sell where currency = '" + currency__ + "' "
    cursor.execute(sql_query_buy)
    result_buy = cursor.fetchall()[0][0]

    if currency__ == '':
        sql_query_sell = "SELECT sell from currency_buy_sell where currency = '" + currency + "' "
    else:
        sql_query_sell = "SELECT sell from currency_buy_sell where currency = '" + currency__ + "' "
    cursor.execute(sql_query_sell)
    result_sell = cursor.fetchall()[0][0]

    if currency__ == '':
        sql_query_predicted_high_low = "select * from predicted_high_low"
    else:
        sql_query_predicted_high_low = "select * from predicted_high_low where currency = '" + currency__ + "'"

    cursor.execute(sql_query_predicted_high_low)
    result_high_low = cursor.fetchall()

    if currency__ != '' and interval__ == '':
        sql_query_historical_data = "Select * from historical_data where currency = '" + currency__ + "'"
    elif currency__ != '' and interval__ != '':
        sql_query_historical_data = "Select * from historical_data where currency = '" + currency__ + "' and time_interval = '" + interval__ + "'"
    else:
        sql_query_historical_data = "Select * from historical_data"

    cursor.execute(sql_query_historical_data)
    result_historical = cursor.fetchall()

    currency_ = Currency.objects.all()
    time_interval = Interval.objects.all()

    context = {
        "Buy": result_buy,
        "Sell": result_sell,
        "high_low": result_high_low,
        "historical_data": result_historical,
        "Get_currency": currency_,
        "Get_interval": time_interval,
        "currency": currency__,
        "current_price": result_current_price,
    }

    return render(request, 'chartjs/demo_v1.html', context)
    # return render(request, context, template_name)

def get_currency(request):
    mydb = psycopg2.connect(
        database="postgres", user='postgres', password='admin', host='127.0.0.1', port='5432')

    mydb.autocommit = True
    cursor = mydb.cursor()

    currency = "AUDUSD"
    currency__ = ""
    interval__ = ""


    if request.GET.get('currency'):
        currency__ = request.GET.get('currency')

    if request.GET.get('interval'):
        interval__ = request.GET.get('interval')
        interval__ = interval__ + "Min"

    # print(currency__)
    # print(request.GET)
    # print("CURRENCY--------------------------", currency__)

    if currency__ == '':
        sql_current_price = "SELECT current_price from currency_buy_sell where currency = '" + currency + "' "
    else:
        sql_current_price = "SELECT current_price from currency_buy_sell where currency = '" + currency__ + "' "
    cursor.execute(sql_current_price)
    result_current_price = cursor.fetchall()[0][0]
    cursor = None
    cursor = mydb.cursor()

    if currency__ == '':
        sql_query_buy = "SELECT buy from currency_buy_sell where currency = '" + currency + "' "
    else:
        sql_query_buy = "SELECT buy from currency_buy_sell where currency = '" + currency__ + "' "
    cursor.execute(sql_query_buy)
    result_buy = cursor.fetchall()[0][0]

    if currency__ == '':
        sql_query_sell = "SELECT sell from currency_buy_sell where currency = '" + currency + "' "
    else:
        sql_query_sell = "SELECT sell from currency_buy_sell where currency = '" + currency__ + "' "
    cursor.execute(sql_query_sell)
    result_sell = cursor.fetchall()[0][0]

    if currency__ == '':
        sql_query_high_low = "select * from predicted_high_low "
    else:
        sql_query_high_low = "select * from predicted_high_low where currency = '" + currency__ + "' "
    cursor.execute(sql_query_high_low)
    result_high_low = cursor.fetchall()
    # print("result_high_low", result_high_low)
    # print(type(result_high_low))

    if currency__ != '' and interval__ == '':
        sql_query_historical_data = "Select * from historical_data where currency = '" + currency__ + "'"
    elif currency__ != '' and interval__ != '':
        sql_query_historical_data = "Select * from historical_data where currency = '" + currency__ + "' and time_interval = '" + interval__ + "'"
    else:
        sql_query_historical_data = "Select * from historical_data"

    cursor.execute(sql_query_historical_data)
    result_historical = cursor.fetchall()
    print("result_historical", result_historical)
    print("result_historical", len(result_historical))

    response = {
        'current_price': result_current_price,
        'result_buy': str(result_buy),
        'result_sell': str(result_sell),
        'result_high_low': result_high_low,
        'result_historical': result_historical
    }
    return JsonResponse(response)

def get_current_price(request):
    mydb = psycopg2.connect(
        database="postgres", user='postgres', password='admin', host='127.0.0.1', port='5432')

    mydb.autocommit = True
    cursor = mydb.cursor()

    currency = "AUDUSD"
    currency__ = ""
    if request.GET.get('currency'):
        currency__ = request.GET.get('currency')
    print("CURRENCY--------------------------", currency__)

    if currency__ == '':
        sql_current_price = "SELECT current_price from currency_buy_sell where currency = '" + currency__ + "' "
    else:
        sql_current_price = "SELECT current_price from currency_buy_sell where currency = '" + currency + "' "
    cursor.execute(sql_current_price)
    result_current_price = cursor.fetchall()[0][0]

    response = {
        'current_price': result_current_price
    }
    return JsonResponse(response)

def get_buy_sell_gauge(request):
    mydb = psycopg2.connect(
        database="postgres", user='postgres', password='admin', host='127.0.0.1', port='5432')

    mydb.autocommit = True
    cursor = mydb.cursor()

    currency__ = ""
    currency = "AUDUSD"

    if request.GET.get('currency'):
        currency__ = request.GET.get('currency')


    if currency__ == '':
        sql_query_buy = "SELECT buy from currency_buy_sell where currency = '" + currency + "' "
    else:
        sql_query_buy = "SELECT buy from currency_buy_sell where currency = '" + currency__ + "' "
    cursor.execute(sql_query_buy)
    result_buy = cursor.fetchall()[0][0]

    if currency__ == '':
        sql_query_sell = "SELECT sell from currency_buy_sell where currency = '" + currency + "' "
    else:
        sql_query_sell = "SELECT sell from currency_buy_sell where currency = '" + currency__ + "' "
    cursor.execute(sql_query_sell)
    result_sell = cursor.fetchall()[0][0]

    currency_params = request.GET.get('currency', None)
    print("currency_params", currency_params)

    response = {
        'result_buy': str(result_buy),
        'result_sell': str(result_sell)
    }

    return JsonResponse(response)

def get_prediction_tbl(request):
    mydb = psycopg2.connect(
        database="postgres", user='postgres', password='admin', host='127.0.0.1', port='5432')

    mydb.autocommit = True
    cursor = mydb.cursor()

    currency = ""
    # currency = "AUDUSD"

    if request.GET.get('currency'):
        currency = request.GET.get('currency')


    # currency = "AUDUSD"
    sql_query_current_price = "select * from predicted_high_low where currency = '" + currency + "' "
    cursor.execute(sql_query_current_price)
    result_high_low = cursor.fetchall()

    currency_params = request.GET.get('currency', None)

    response = {
        'result_high_low': result_high_low
    }

    return JsonResponse(response)

def get_historical_tbl(request):
    mydb = psycopg2.connect(
        database="postgres", user='postgres', password='admin', host='127.0.0.1', port='5432')

    mydb.autocommit = True
    cursor = mydb.cursor()

    currency__ = "AUDUSD"
    interval__ = ""

    if request.GET.get('currency'):
        currency__ = request.GET.get('currency')

    if request.GET.get('interval'):
        interval__ = request.GET.get('interval')
        interval__ = interval__ + "Min"


    if currency__ != '' and interval__ == '':
        sql_query_historical_data = "Select * from historical_data where currency = '" + currency__ + "'"
    elif currency__ != '' and interval__ != '':
        sql_query_historical_data = "Select * from historical_data where currency = '" + currency__ + "' and time_interval = '" + interval__ + "'"
    else:
        sql_query_historical_data = "Select * from historical_data"

    cursor.execute(sql_query_historical_data)
    result_historical = cursor.fetchall()

    currency_params = request.GET.get('currency', None)

    response = {
        'result_historical': result_historical
    }

    return JsonResponse(response)




class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class IntervalViewSet(viewsets.ModelViewSet):
    queryset = Interval.objects.all()
    serializer_class = IntervalSerializer
