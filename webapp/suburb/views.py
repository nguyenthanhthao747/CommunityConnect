from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator

# to avoid 403 forbidden error
from django.views.decorators.csrf import csrf_exempt

from provider.models import *
from suburb.models import *

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db import connection



def index(request):
    dict_data = {}
    dict_filter = {}
    suburb_filter = ""
    show_regional = 1
    start_point = True

    try:
        if request.GET.get('q'):
            suburb_filter = request.GET.get('q')
            start_point = False
            dict_filter['suburb__icontains'] = suburb_filter;

        if request.GET.get('show-regional'):
            show_regional = request.GET.get('show-regional')
    except:
        print("")

    has_data = True

    pages = []
    page_count = 0
    providers_list =[]

    # if len(dict_filter) > 0:

    # dict_filter['is_regional'] = int(show_regional);

    providers_list = VetProviders.objects.filter(**dict_filter).order_by("name")
    # providers_list_full = VetProviders.objects.filter(**dict_filter).order_by("name")

    paginator = Paginator(providers_list, 100) # Show 25 contacts per page

    page = request.GET.get('page')
    suburbs = paginator.get_page(page)
    # else:
    #     suburbs = []
    #     has_data = False

    return render(request, 'suburb/templates/index.html',  {
        'providers': suburbs,
        # 'providers_all': providers_list,
        'suburb_filter': suburb_filter,
        'show_regional': show_regional,
        'has_data': has_data,
        'start_point': start_point,
        'pages': pages,
        'page_count': page_count
    })


def institutes(request):
    dict_data = {}
    dict_filter = {}
    suburb_filter = ""
    show_regional = 1
    start_point = True

    try:
        if request.GET.get('q'):
            suburb_filter = request.GET.get('q')
            start_point = False
            dict_filter['suburb__icontains'] = suburb_filter;

        if request.GET.get('show-regional'):
            show_regional = request.GET.get('show-regional')
    except:
        print("")

    has_data = True

    pages = []
    page_count = 0
    providers_list =[]

    # if len(dict_filter) > 0:

    # dict_filter['is_regional'] = int(show_regional);

    providers_list = VetProviders.objects.filter(**dict_filter).order_by("name")
    # providers_list_full = VetProviders.objects.filter(**dict_filter).order_by("name")

    paginator = Paginator(providers_list, 100) # Show 25 contacts per page

    page = request.GET.get('page')
    suburbs = paginator.get_page(page)
    # else:
    #     suburbs = []
    #     has_data = False

    return render(request, 'suburb/templates/index_institutes.html',  {
        'providers': suburbs,
        # 'providers_all': providers_list,
        'suburb_filter': suburb_filter,
        'show_regional': show_regional,
        'has_data': has_data,
        'start_point': start_point,
        'pages': pages,
        'page_count': page_count
    })

def index_ajax(request):
    dict_data = {}
    dict_filter = {}
    suburb_filter = ""
    show_regional = 1

    has_data = True
    start_point = True
    pages = []
    page_count = 0
    providers_list =[]

    # if len(dict_filter) > 0:
    start_point = False
    # dict_filter['is_regional'] = int(show_regional);

    providers_list = VetProviders.objects.filter(**dict_filter).order_by("name")
    # providers_list_full = VetProviders.objects.filter(**dict_filter).order_by("name")

    paginator = Paginator(providers_list, 100) # Show 25 contacts per page

    page = int(request.GET.get('page'))
    if paginator.num_pages < page:
        suburbs = []
    else:
        suburbs = paginator.get_page(page)
    # else:
    #     suburbs = []
    #     has_data = False

    return render(request, 'suburb/templates/institute_row.html',  {
        'providers': suburbs,
    })

def boundary_ajax(request):
    dict_data = {}
    dict_filter = {}
    suburb_filter = ""
    show_regional = 1

    has_data = True
    start_point = True
    pages = []
    page_count = 0
    providers_list =[]

    # if len(dict_filter) > 0:
    start_point = False
    dict_filter['is_regional'] = int(show_regional);

    sububs = get_suburbs(request)

    dict_data["sububs"] = sububs

    return JsonResponse(dict_data)

def get_suburbs(post_request):

    requested_data = []

    page = 1
    if post_request.GET.get('page'):
        page = int(post_request.GET.get('page'))
        print("####################### fetch page = " + str(page))

    page_size = 300
    start_limit = page_size * (page - 1)

    sql_str = f"""
SELECT
	s.id, s.region_name, s.lga, s.postcode,
    s.suburb, s.is_regional,
sb.geo_boundary, s.latitude, s.longitude,
cr.no_of_incidents, cr.population,
cr.crime_rate as crate, cr.crime_star,
s.area_sq_km,
si.stops_count,
si.provider_count,
si.school_count,
si.hospital_count,
si.distance_from_cbd
FROM
    suburb as s
INNER JOIN suburb_boundary sb ON sb.suburb_id = s.id
LEFT JOIN crime_rate cr ON cr.suburb_id = s.id
LEFT JOIN suburb_info si ON si.id = s.id
WHERE s.is_regional = 1 AND si.provider_count > 0
LIMIT {start_limit}, {page_size}
    """

    cursor = connection.cursor();
    cursor.execute(sql_str)
    the_rs = cursor.fetchall()

    for var in the_rs:

        crime_rate = 0.4

        if var[11]:
            crime_rate = round(float(var[11]), 2)

        # print("crime rate", crime_rate)

        crime_stars = [0] * 5
        if var[12]:
            the_high = int(var[12])
        else:
            the_high = 5

        if the_high > 5:
            the_high = 5
        for xindex in range(0, the_high):
            crime_stars[xindex] = 1

        if var[10]:
            population = int(var[10])
        else:
            population = 0

        if var[13]:
            area_sq_km = float(var[13])
        else:
            area_sq_km = 0

        if var[14]:
            stops_count = float(var[14])
        else:
            stops_count = 0

        connectivity_index = 0
        if stops_count:
            connectivity_index = int(stops_count/ area_sq_km)

        record = {
            "suburb_id": var[0],
            "region_name": var[1],
            "lga": var[2],
            "postcode":var[3],
            "name": var[4],
            "is_regional": var[5],
            "geo_boundary": var[6],
            "latitude": var[7],
            "longitude": var[8],
            "no_of_incidents": var[9],
            "population": population,
            "crate": crime_rate,
            "crime_star": the_high,
            "crime_stars": crime_stars,
            "area_sq_km": area_sq_km,
            "stops_count": int(stops_count),
            "connectivity_index": connectivity_index,
            "provider_count": var[15],
            "school_count": var[16],
            "hospital_count": var[17],
            "distance_from_cbd": round(float(var[18]), 2)

        }
        requested_data.append(record)
    return requested_data

def suburb_info(request, suburb_id):
    dict_data = {}
    dict_filter = {}
    suburb_filter = ""

    has_data = True
    start_point = True
    pages = []
    page_count = 0
    providers_list =[]

    if len(dict_filter) > 0:
        start_point = False
        # dict_filter['is_regional'] = int(show_regional);

        providers_list = VetProviders.objects.filter(**dict_filter).order_by("name")
        providers_list_full = VetProviders.objects.filter(**dict_filter).order_by("name")

        paginator = Paginator(providers_list, 10) # Show 25 contacts per page

        page = request.GET.get('page')
        suburbs = paginator.get_page(page)
    else:
        suburbs = []
        has_data = False

    return render(request, 'suburb/templates/index.html',  {
        'providers': providers_list,
        'suburb_filter': suburb_filter,
        'show_regional': show_regional,
        'has_data': has_data,
        'start_point': start_point,
        'pages': pages,
        'page_count': page_count
    })

def results(request):


    return render(request, 'suburb/templates/results.html')

@csrf_exempt
def details(request, suburb_id):
    dict_data = {
        "suburb_id": suburb_id
    }

    return render(request, 'suburb/templates/details.html')

@csrf_exempt
def fetch(request):
    dict_data = {}

    search_query = request.POST.get('search', '')

    requested_data = []
    # querySet = VetProviders.objects.filter(name__icontains=search_institutes)
    querySet = VetProviders.objects.filter(suburb__icontains=search_query).values("name").annotate(n=models.Count("pk"))[0:9]
    for qset in querySet:
        requested_data.append(qset["name"]);

    dict_data = {
        "data": requested_data,
        # "search": search_query
    }

    return JsonResponse(dict_data)


@csrf_exempt
def fetch_details(request):
    dict_data = {}

    search_query = request.POST.get('search', '')

    requested_data = []
    # querySet = VetProviders.objects.filter(name__icontains=search_institutes)

    if search_query.isdigit():
        querySet = VetProviders.objects.filter(
            Q(name__icontains = search_query) |
            Q(asqa_code__icontains = search_query) |
            Q(address_line_1__icontains = search_query) |
            Q(address_line_2__icontains = search_query) |
            Q(suburb__icontains = search_query) |
            Q(postcode = int(search_query)) |
            Q(site_name__icontains = search_query)
        ).values()[0:9]
    else:
        querySet = VetProviders.objects.filter(
            Q(name__icontains = search_query) |
            Q(asqa_code__icontains = search_query) |
            Q(address_line_1__icontains = search_query) |
            Q(address_line_2__icontains = search_query) |
            Q(suburb__icontains = search_query) |
            Q(site_name__icontains = search_query)
        ).values()[0:9]



    # print(len(querySet))

    for qset in querySet:

        address_field = ""
        if qset["address_line_1"] != "0":
            address_field += qset["address_line_1"] + ", "

        if qset["address_line_2"] != "0":
            address_field += qset["address_line_2"] + ", "

        if qset["suburb"] != "0":
            address_field += qset["suburb"].title() + ", "

        if qset["postcode"] != 0:
            address_field += str(qset["postcode"])

        # print(qset)
        requested_data.append({
            "id": qset["id"],
            "text": qset["name"],
            "address": address_field,
            "asqa_code": qset["asqa_code"],
            "site_name": qset["site_name"],
        });

    dict_data = {
        "results": requested_data,
        # "search": search_query
    }

    return JsonResponse(dict_data)

def fetch_data(request):
    dict_data = {}
    requested_data = []

    search_query = request.POST.get('search', '')

    sql_str = f"""
SELECT
DISTINCT vp.suburb
FROM vet_providers vp
WHERE
(suburb LIKE '{search_query}%')
LIMIT 50
    """

    cursor = connection.cursor();
    cursor.execute(sql_str)
    the_rs = cursor.fetchall()

    if len(the_rs) > 0:
        for qset in the_rs:
            requested_data.append({
                'label': qset[0].strip().capitalize() ,
                'value': qset[0].strip().capitalize() ,
            })
    else:
        filter_clause = Q(suburb__icontains = search_query)


        if search_query.isdigit():
            filter_clause = filter_clause | Q(postcode = int(search_query))

        querySet = VetProviders.objects.filter(
            filter_clause
        ).values().annotate(n=models.Count("pk"))[0:50]

        for qset in querySet:

            requested_data.append({
                'label': qset["suburb"].strip().capitalize() ,
                'value': qset["suburb"].strip().capitalize() ,
            })

    dict_data = {
        "results": requested_data,
        # "search": search_query
    }

    return JsonResponse(dict_data)
