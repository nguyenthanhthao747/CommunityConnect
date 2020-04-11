from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import Sum
from django.shortcuts import redirect
import pandas as pd
from provider.models import *

from django.contrib.auth.decorators import login_required
from datetime import datetime
from random import randrange
from datetime import timedelta

def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

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

def signup(request):
    dict_data = {}

    return render(request, 'vicview/templates/signup.html', {})

def login(request):
    dict_data = {}
    return render(request, 'vicview/templates/login.html', {})

def seek_support_search(request):
    dict_data = {}

    return render(request, 'vicview/templates/seek-support-search.html', {})

def volunteer_add(request):
    dict_data = {}
    dict_filter = {}
    dict_filter_contains = {}
    search_filter = {}
    high_demand = ""
    totals = {}
    totals["courses"] = 0

    try:
        if request.GET.get('q'):
            search_filter["occupation"] = request.GET.get('q')
            dict_filter['title__istartswith'] = search_filter["occupation"];
            dict_filter_contains['title__icontains'] = search_filter["occupation"];

        if request.GET.get('high_demand'):
            high_demand = int(request.GET.get('high_demand'))
        else:
            high_demand = 0

    except:
        print("")

    search_filter["category"] = ""
    try:
        if request.GET.get('category'):
            search_filter["category"] = request.GET.get('category')
            dict_filter['category_id'] = search_filter["category"]
            dict_filter_contains['category_id'] = search_filter["category"]
    except:
        print("")


    dict_filter_2 = {}
    dict_filter_2["postcode"] = int(3150)
    dict_filter_2["government_subsidised"] = 'N'
    provider_list = VetProviders.objects.filter(**dict_filter_2).values()
    print("list of providers", len(provider_list))
    print(provider_list)
    totals["courses"] = len(provider_list)

    d1 = datetime.strptime('1/04/2020 1:30 PM', '%m/%d/%Y %I:%M %p')
    d2 = datetime.strptime('1/06/2020 4:50 AM', '%m/%d/%Y %I:%M %p')

    providers_from_list = []
    for xitem in provider_list:
        i = 0
        xitemtemp = xitem
        xitemtemp["availability"] = random_date(d1, d2).strftime("%d-%m-%Y")
        if (i/2==0):
            xitemtemp["desc"] = "Hi, I'm " + xitemtemp["address_line_2"] + ", available for after hours age care support."
        else:
            xitemtemp["desc"] = "Hi, I'm " + xitemtemp["address_line_2"] + ", available on Fridays for help."
        i = i+1

        print("hello", xitemtemp["availability"], xitemtemp)
        providers_from_list.append(xitemtemp)

    has_data = True
    start_point = True
    pages = []
    page_count = 0

    if len(dict_filter) > 0:
        start_point = False

        # dict_filter['high_demand'] = high_demand;

        occupation_list = VetProfessions.objects.filter(**dict_filter).values()

        if len(occupation_list) <= 0:
            occupation_list = VetProfessions.objects.filter(**dict_filter_contains).values()

        for xitem in occupation_list:
            # get offered courses for xitem
            anzsco_filter = int(xitem["anzsco_id"])
            print(anzsco_filter)

            courses_from_occupation = VetCoursesToOccupation.objects.filter(anzsco=anzsco_filter).values().extra(
              select={
                'id': 'course_id'
              }
            ).values(
              'id'
            )
            print(courses_from_occupation)

            xitem["courses"] = VetCourses.objects.filter(id__in=courses_from_occupation).order_by("course_title")
            # totals["courses"] += len(xitem["courses"])

            if xitem["future_growth"] in future_growth_map:
                xitem["future_growth_info"] = future_growth_map[xitem["future_growth"]]

            if xitem["skill_level"] in skill_map:
                xitem["skill_level_info"] = skill_map[xitem["skill_level"]]

        totals["occupations"] = len(occupation_list)
        paginator = Paginator(occupation_list, 20)

        page = request.GET.get('page')
        occupations = paginator.get_page(page)
    else:
        occupations = []
        has_data = False

    current_filter = "?"


    category_filter_name = ""
    if search_filter["category"]:
        course_category_info = VetProfessionsCategory.objects.filter(id=search_filter["category"]).values()[0]
        print(course_category_info)
        category_filter_name = course_category_info["name"]
        current_filter += "cf=" + category_filter_name + "&"

    return render(request, 'vicview/templates/volunteer-landing.html',  {
        'occupations': occupations,
        'filters': search_filter,
        #'occupation_filter': search_filter["occupation"],
        'category_filter_name': category_filter_name,
        'current_filter': current_filter,
        'high_demand': high_demand,
        'has_data': has_data,
        'start_point': start_point,
        'pages': pages,
        'providers': providers_from_list,
        'page_count': page_count,
        'totals': totals
    })

def donate(request):
    dict_data = {}
    dict_filter = {}
    dict_filter_contains = {}
    search_filter = {}
    high_demand = ""
    totals = {}
    totals["courses"] = 0

    try:
        if request.GET.get('q'):
            search_filter["occupation"] = request.GET.get('q')
            dict_filter['title__istartswith'] = search_filter["occupation"];
            dict_filter_contains['title__icontains'] = search_filter["occupation"];

        if request.GET.get('high_demand'):
            high_demand = int(request.GET.get('high_demand'))
        else:
            high_demand = 0

    except:
        print("")

    search_filter["category"] = ""
    try:
        if request.GET.get('category'):
            search_filter["category"] = request.GET.get('category')
            dict_filter['category_id'] = search_filter["category"]
            dict_filter_contains['category_id'] = search_filter["category"]
    except:
        print("")


    dict_filter_2 = {}
    dict_filter_2["postcode"] = int(3150)
    dict_filter_2["government_subsidised"] = 'N'
    provider_list = VetProviders.objects.filter(**dict_filter_2).values()
    print("list of providers", len(provider_list))
    print(provider_list)
    totals["courses"] = len(provider_list)

    d1 = datetime.strptime('1/04/2020 1:30 PM', '%m/%d/%Y %I:%M %p')
    d2 = datetime.strptime('1/06/2020 4:50 AM', '%m/%d/%Y %I:%M %p')

    providers_from_list = []
    for xitem in provider_list:
        i = 0
        xitemtemp = xitem
        xitemtemp["availability"] = random_date(d1, d2).strftime("%d-%m-%Y")
        if (i/2==0):
            xitemtemp["desc"] = "Hi, I'm " + xitemtemp["address_line_2"] + ", available for after hours age care support."
        else:
            xitemtemp["desc"] = "Hi, I'm " + xitemtemp["address_line_2"] + ", available on Fridays for help."
        i = i+1

        print("hello", xitemtemp["availability"], xitemtemp)
        providers_from_list.append(xitemtemp)

    has_data = True
    start_point = True
    pages = []
    page_count = 0

    if len(dict_filter) > 0:
        start_point = False

        # dict_filter['high_demand'] = high_demand;

        occupation_list = VetProfessions.objects.filter(**dict_filter).values()

        if len(occupation_list) <= 0:
            occupation_list = VetProfessions.objects.filter(**dict_filter_contains).values()

        for xitem in occupation_list:
            # get offered courses for xitem
            anzsco_filter = int(xitem["anzsco_id"])
            print(anzsco_filter)

            courses_from_occupation = VetCoursesToOccupation.objects.filter(anzsco=anzsco_filter).values().extra(
              select={
                'id': 'course_id'
              }
            ).values(
              'id'
            )
            print(courses_from_occupation)

            xitem["courses"] = VetCourses.objects.filter(id__in=courses_from_occupation).order_by("course_title")
            # totals["courses"] += len(xitem["courses"])

            if xitem["future_growth"] in future_growth_map:
                xitem["future_growth_info"] = future_growth_map[xitem["future_growth"]]

            if xitem["skill_level"] in skill_map:
                xitem["skill_level_info"] = skill_map[xitem["skill_level"]]

        totals["occupations"] = len(occupation_list)
        paginator = Paginator(occupation_list, 20)

        page = request.GET.get('page')
        occupations = paginator.get_page(page)
    else:
        occupations = []
        has_data = False

    current_filter = "?"


    category_filter_name = ""
    if search_filter["category"]:
        course_category_info = VetProfessionsCategory.objects.filter(id=search_filter["category"]).values()[0]
        print(course_category_info)
        category_filter_name = course_category_info["name"]
        current_filter += "cf=" + category_filter_name + "&"

    return render(request, 'vicview/templates/donate.html',  {
        'occupations': occupations,
        'filters': search_filter,
        #'occupation_filter': search_filter["occupation"],
        'category_filter_name': category_filter_name,
        'current_filter': current_filter,
        'high_demand': high_demand,
        'has_data': has_data,
        'start_point': start_point,
        'pages': pages,
        'providers': providers_from_list,
        'page_count': page_count,
        'totals': totals
    })


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
