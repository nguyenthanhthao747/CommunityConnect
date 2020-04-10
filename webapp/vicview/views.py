from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import Sum
from django.shortcuts import redirect
import pandas as pd

from django.contrib.auth.decorators import login_required

def index(request):
    dict_data = {}

    print(request.is_secure())
    # earlier model used date_mode_hour_card_type
    # query = year_month_mode.objects.filter(
    #     year=2018
    # ).values('mode').annotate(total=Sum('scan_count'))
    #
    # df = to_df(query)
    #
    # bus = df[df["mode"] == 1]["total"]
    # train = df[df["mode"] == 2]["total"]
    # tram = df[df["mode"] == 3]["total"]
    #
    pie_info = {}
    #
    # pie_info["labels"] = ["Bus", "Train", "Tram"]
    # pie_info["data"] = [sum(bus), sum(train), sum(tram)]
    # pie_info["backgroundColor"] = ["#ff8201", "#0073d0", "#78be1f"]


    return render(request, 'vicview/templates/index.html', {
        'sample_0': dict_data,
        # 'stop_rows': stop_rows_sub,
        "pie_info": pie_info,
        # 'stops': stops
    })

def seek_support_search(request):
    dict_data = {}

    return render(request, 'vicview/templates/seek-support-search.html', {})

def search_integrated(request):
    dict_data = {}

    return render(request, 'vicview/templates/index_search.html')

def about(request):
    dict_data = {}

    return render(request, 'vicview/templates/about.html')


def geolocation(request):
    dict_data = {}

    return render(request, 'vicview/templates/geolocation.html')

#perfom the raw query
def execute_raw_sql(query):
    cursor = connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return data

#function to query
def to_df(queryset):
    try:
        query, params = queryset.query.sql_with_params()
    except EmptyResultSet:
        # Occurs when Django tries to create an expression for a
        # query which will certainly be empty
        # e.g. Book.objects.filter(author__in=[])
        return pd.DataFrame()
    return pd.io.sql.read_sql_query(query, connection, params=params)

def code1(request):

    return HttpResponse("AZADY6r0unRjhV2NRazkgH8MdP2n9VQthyb8sQPGc6I.OHtyEX9a6NSfZ-gfbSBUwtTqVc2gWsDuxSdlxnrG96o")

def code2(request):

    return HttpResponse("jZERTMXD3HgoMnKRfM74JowjSrugN6KsmW5N9nulB7U.OHtyEX9a6NSfZ-gfbSBUwtTqVc2gWsDuxSdlxnrG96o")

def page_not_found_view(request, exception, template_name='404.html'):
	dict_data = {}
	dict_data["str_page_title"] = "PAGE NOT FOUND"
	dict_data["str_page_message"] = "Requested page could not be found."
	return render(request, 'vicview/templates/404.html', dict_data)

def error_view(request, template_name='500.html'):
	dict_data = {}
	dict_data["str_page_title"] = "UNABLE TO PROCESS"
	dict_data["str_page_message"] = "Requested page could not be found."
	return render(request, 'vicview/templates/404.html', dict_data)

def permission_denied_view(request, exception, template_name='403.html'):
	dict_data = {}
	dict_data["str_page_title"] = "PERMISSION DENIED"
	dict_data["str_page_message"] = "Requested page could not be found."
	return render(request, 'vicview/templates/404.html', dict_data)

def bad_request_view(request, exception, template_name='403.html'):
	dict_data = {}
	dict_data["str_page_title"] = "BAD REQUEST"
	dict_data["str_page_message"] = "Requested page could not be found."
	return render(request, 'vicview/templates/404.html', dict_data)
