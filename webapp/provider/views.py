from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator

# to avoid 403 forbidden error
from django.views.decorators.csrf import csrf_exempt

from provider.models import *
from suburb.models import *
from occupation.models import *

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db import connection

import pandas as pd # to import pandas package
import numpy as np # to import numpy package
import re

from colour import Color
green = Color("#00802A")
colors = list(green.range_to(Color("#FF0000"), 10))
colors = [Color("#0D8000"), Color("#6FBF00"), Color("#FFFF00"), Color("#FFBB44"), Color("#FFAAAA")]
colors_font = ["white", "black", "black", "black", "black"]

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
    dict_filter = {}
    provider_filter = ""
    show_regional = 1

    try:
        if request.GET.get('q'):
            provider_filter = request.GET.get('q')
            dict_filter['name__icontains'] = provider_filter;
    except:
        print("")

    try:
        if request.GET.get('show-regional'):
            show_regional = request.GET.get('show-regional')
    except:
        print("show_regional exception", show_regional)

    category_filter = ""
    try:
        if request.GET.get('cf'):
            category_filter = request.GET.get('cf')
            dict_filter['suburb'] = category_filter
            dict_filter_contains['suburb'] = category_filter
    except:
        print("")

    print("show_regional value ", show_regional)
    show_regional = int(show_regional)
    has_data = True
    start_point = True
    pages = []
    page_count = 0

    if len(dict_filter) > 0:
        start_point = False
        # dict_filter['is_regional'] = int(show_regional);

        # if ('q' in request.GET) and request.GET['q'].strip():
        #     query_string = request.GET['q']
        #     entry_query = get_query(query_string, ['name', 'suburb', 'address_line_1',
        #     'address_line_2', 'postcode'])
        #     # entry_query = (entry_query) & Q(is_regional = int(show_regional))
        #     provider_list = VetProviders.objects.filter(entry_query).order_by('name')

        provider_list = VetProviders.objects.filter(**dict_filter).order_by("name")

        paginator = Paginator(provider_list, 10)

        page = request.GET.get('page')
        providers = paginator.get_page(page)
    else:
        providers = []
        has_data = False

    current_filter = "?"

    if provider_filter:
        current_filter += "q=" + provider_filter + "&"

    if category_filter:
        current_filter += "cf=" + category_filter + "&"

    return render(request, 'provider/templates/index.html',  {
        'providers': providers,
        'provider_filter': provider_filter,
        'category_filter': category_filter,
        'current_filter': current_filter,
        'show_regional': show_regional,
        'has_data': has_data,
        'start_point': start_point,
        'pages': pages,
        'page_count': page_count
    })

def normalize_query(query_string,
    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
    normspace=re.compile(r'\s{2,}').sub):

    return [normspace(' ',(t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def suburbs(request, provider_id):
    dict_debug = {}
    dict_data = {}
    dict_filter = {}
    provider_filter = ""
    show_regional = 1

    try:
        if request.GET.get('provider_filter'):
            provider_filter = request.GET.get('provider_filter')
            dict_filter['name__icontains'] = provider_filter;
    except:
        print("")

    # print("show_regional value ", show_regional)
    show_regional = int(show_regional)
    has_data = True
    start_point = True
    pages = []
    page_count = 0
    provider_info = []

    # just the provider info
    dict_filter['id'] = int(provider_id);
    provider_info = VetProviders.objects.filter(**dict_filter).order_by("name")[0]
    # print("provider_info", provider_info)

    nearest_suburbs = get_nearby_suburbs(provider_info)

    df_nearest_suburbs = pd.DataFrame(nearest_suburbs)

    df_nearest_suburbs = df_nearest_suburbs.sort_values(
    by = ['crime_star', 'connectivity_index', 'provider_count', 'distance_from_cbd',
    'school_count', 'hospital_count', 'population', 'distance_in_km'],
    ascending= [False, False, False, True,
    False, False, True, True])

    sorted_nearest_suburbs = df_nearest_suburbs.to_dict("records")

    # delete suburb with no info in it
    delete_suburbs = []

    for idx, xsuburb in enumerate(sorted_nearest_suburbs):

        # get rent ratings
        xs_rents = Rents.objects.filter(**{"suburb_id": xsuburb["suburb_id"]}).values()
        min_rent = 0
        for xsr in xs_rents:
            if min_rent == 0:
                min_rent = xsr["rent_value"]
                xsuburb["min_rent"] = xsr

            if min_rent > xsr["rent_value"]:
                min_rent = xsr["rent_value"]
                xsuburb["min_rent"] = xsr

        if "min_rent" in xsuburb:
            print(xsuburb["min_rent"])
        xsuburb["rents"] = xs_rents

        # get suburb schools
        xsuburb["schools"] = School.objects.filter(**{"suburb_id": xsuburb["suburb_id"]}).values()

        # get suburb Hospital
        xsuburb["hospitals"] = Hospital.objects.filter(**{"suburb_id": xsuburb["suburb_id"]}).values()

        # get suburb PtvStops
        xsuburb["stops"] = PtvStops.objects.filter(**{"suburb_id": xsuburb["suburb_id"]}).values()[0:9]

        # get suburb CrimeRate
        xsuburb["crime_rate"] = CrimeRate.objects.filter(**{"suburb_id": xsuburb["suburb_id"]}).values()

        # if len(xsuburb["rents"]) == 0 and len(xsuburb["schools"]) == 0 and len(xsuburb["hospitals"]) == 0 and len(xsuburb["stops"]) == 0:
        if len(xsuburb["schools"]) == 0:
            delete_suburbs.append(idx)


        # print(xsuburb)
    # print("nearest_suburbs", nearest_suburbs)
    for dindex in sorted(delete_suburbs, reverse=True):
        del sorted_nearest_suburbs[dindex]


    # just take the 5
    sorted_nearest_suburbs = sorted_nearest_suburbs[0:5]
    for idx, xsuburb in enumerate(sorted_nearest_suburbs):
        # recommended color
        xsuburb["fillColor"] = Color(colors[idx]).get_hex()
        xsuburb["fontColor"] = colors_font[idx]
        xsuburb["strokeColor"] = colors[idx].get_hex()

    if len(dict_filter) > 0:
        start_point = False
        # dict_filter['is_regional'] = int(show_regional);


        dict_filter['is_regional'] = int(show_regional);
        provider_list = VetProviders.objects.filter(**dict_filter).order_by("name")

        paginator = Paginator(provider_list, 10) # Show 25 contacts per page

        page = request.GET.get('page')
        providers = paginator.get_page(page)
    else:
        providers = []
        has_data = False

    return render(request, 'provider/templates/nearby_suburbs.html',  {
        'provider_info': provider_info,
        'providers': providers,
        'provider_filter': provider_filter,
        'show_regional': show_regional,
        'has_data': has_data,
        'start_point': start_point,
        'pages': pages,
        'nearest_suburbs': sorted_nearest_suburbs
    })


def get_nearby_suburbs(post_request):

    requested_data = []

    lat = post_request.latitude
    lng = post_request.longitude
    # (SELECT ms.mode FROM api_mode_stop_id as ms WHERE ms.stop_id = agg.stop_id LIMIT 1) as mode
    sql_str = f"""
SELECT
	s.id, s.region_name, s.lga, s.postcode,
    s.suburb, s.is_regional,
    111.111 *
    DEGREES(ACOS(COS(RADIANS(s.latitude))
 * COS(RADIANS({lat}))
 * COS(RADIANS(s.longitude - ({lng})))
 + SIN(RADIANS(s.latitude))
 * SIN(RADIANS({lat})))) AS distance_in_km,
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
ORDER BY distance_in_km ASC
LIMIT 10
    """

    cursor = connection.cursor();
    cursor.execute(sql_str)
    the_rs = cursor.fetchall()

    for var in the_rs:

        crime_rate = 0.4

        if var[12]:
            crime_rate = round(float(var[12]), 2)

        print("crime rate", crime_rate)

        crime_stars = [0] * 5
        if var[13]:
            the_high = int(var[13])
        else:
            the_high = 5

        if the_high > 5:
            the_high = 5
        for xindex in range(0, the_high):
            crime_stars[xindex] = 1

        if var[11]:
            population = int(var[11])
        else:
            population = 0

        if var[14]:
            area_sq_km = float(var[14])
        else:
            area_sq_km = 0

        if var[15]:
            stops_count = float(var[15])
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
            "distance_in_km": var[6],
            "geo_boundary": var[7],
            "latitude": var[8],
            "longitude": var[9],
            "no_of_incidents": var[10],
            "population": population,
            "crate": crime_rate,
            "crime_star": the_high,
            "crime_stars": crime_stars,
            "area_sq_km": area_sq_km,
            "stops_count": int(stops_count),
            "connectivity_index": connectivity_index,
            "provider_count": var[16],
            "school_count": var[17],
            "hospital_count": var[18],
            "distance_from_cbd": round(float(var[19]), 2)

        }
        requested_data.append(record)
    return requested_data


def distance(s_lat, s_lng, e_lat, e_lng):

    # radius of earth
    R = 6378.0

    s_lat = s_lat * np.pi / 180.0
    s_lng = np.deg2rad(s_lng)
    e_lat = np.deg2rad(e_lat)
    e_lng = np.deg2rad(e_lng)

    d = np.sin((e_lat - s_lat)/2)**2 + np.cos(s_lat)*np.cos(e_lat) * np.sin((e_lng - s_lng)/2)**2

    # modify to get metres
    return 2 * R * np.arcsin(np.sqrt(d)) * 1000

def nearest_suburbs(xrow, df_data):

    df_hospitals["distance_to_hospital"] = distance(xrow["lat"], xrow["lng"],
                                                   df_hospitals['lat'], df_hospitals['lng'])

    # sort distances in ascending order to get closest
    closest = df_hospitals.sort_values(by = 'distance_to_hospital')

    # fill null values with zeros and convert distances to int
    closest['distance_to_hospital'] = closest['distance_to_hospital'].fillna(0).astype(int)

    # get first row
    nearest = closest.head(1).iloc[0]

    return pd.Series({
        "hospital_id": nearest["id"], # return closeset shopping centre ID
        "distance_to_hospital": nearest["distance_to_hospital"] # return closeset shopping centre Distance
    })

def results(request):

    return render(request, 'provider/templates/results.html')

@csrf_exempt
def details(request, provider_id):
    dict_data = {
        "provider_id": provider_id
    }

    return render(request, 'provider/templates/details.html')

@csrf_exempt
def fetch(request):
    dict_data = {}

    search_query = request.POST.get('search', '')

    requested_data = []
    # querySet = VetProviders.objects.filter(name__icontains=search_institutes)
    querySet = VetProviders.objects.filter(name__icontains=search_query).values("name").annotate(n=models.Count("pk"))[0:9]
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
    search_regional = int(request.POST.get('show_regional', 0))

    requested_data = []
    # querySet = VetProviders.objects.filter(name__icontains=search_institutes)

    if search_query.isdigit():
        querySet = VetProviders.objects.filter(
            (Q(name__icontains = search_query) |
            Q(asqa_code__icontains = search_query) |
            Q(address_line_1__icontains = search_query) |
            Q(address_line_2__icontains = search_query) |
            Q(suburb__icontains = search_query) |
            Q(is_regional = search_regional) |
            Q(postcode = int(search_query)) |
            Q(site_name__icontains = search_query)) & Q(is_regional = search_regional)
        ).values()[0:9]
    else:
        querySet = VetProviders.objects.filter(
            (Q(name__icontains = search_query) |
            Q(asqa_code__icontains = search_query) |
            Q(address_line_1__icontains = search_query) |
            Q(address_line_2__icontains = search_query) |
            Q(suburb__icontains = search_query) |
            Q(site_name__icontains = search_query)) & Q(is_regional = search_regional)
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

@csrf_exempt
def fetch_data(request):
    dict_data = {}
    requested_data = []

    search_query = request.POST.get('search', '')

    sql_str = f"""
SELECT
DISTINCT vp.name
FROM vet_providers vp
WHERE
(name LIKE '{search_query}%')
LIMIT 50
    """

    cursor = connection.cursor();
    cursor.execute(sql_str)
    the_rs = cursor.fetchall()

    if len(the_rs) > 0:
        for qset in the_rs:
            # print(qset)
            # site_name =  qset[1].capitalize()
            # postcode =  qset[2]
            # suburb =  qset[3].capitalize()

            requested_data.append({
                'label': qset[0].strip(),
                'value': qset[0].strip(),
                # "site_name": site_name,
                # "postcode": postcode,
                # "suburb": suburb
            })
    else:
        filter_clause = Q(name__icontains = search_query) | Q(suburb__icontains = search_query)


        if search_query.isdigit():
            filter_clause = filter_clause | Q(postcode = int(search_query))

        querySet = VetProviders.objects.filter(
            filter_clause
        ).values().annotate(n=models.Count("pk"))[0:50]

        for qset in querySet:
            # print(qset)
            # site_name =  qset["site_name"].capitalize()
            # postcode =  qset["postcode"]
            # suburb =  qset["suburb"].capitalize()

            requested_data.append({
                # 'label': qset["name"].strip() + ", " + suburb + ", " + str(postcode),
                'label': qset["name"].strip(),
                'value': qset["name"].strip(),
                # "site_name": site_name,
                # "postcode": postcode,
                # "suburb": suburb
            })

    dict_data = {
        "results": requested_data,
        # "search": search_query
    }

    return JsonResponse(dict_data)

def compare(request, provider_id, suburb_id1, suburb_id2):
    dict_debug = {}
    dict_data = {}
    dict_filter = {}
    provider_filter = ""
    show_regional = 1

    suburbs = {}
    suburbs["s1"] = {}
    suburbs["s2"] = {}

    try:
        if request.GET.get('provider_filter'):
            provider_filter = request.GET.get('provider_filter')
            dict_filter['name__icontains'] = provider_filter;
    except:
        print("")

    # print("show_regional value ", show_regional)
    show_regional = int(show_regional)
    has_data = True
    start_point = True
    pages = []
    page_count = 0
    provider_info = []

    # just the provider info
    dict_filter['id'] = int(provider_id);
    provider_info = VetProviders.objects.filter(**dict_filter).order_by("name")[0]


    #### logic for first suburb
    better_connectivity = 1
    dict_filter['id'] = int(suburb_id1);
    suburbs["s1"]["ginfo"] = Suburb.objects.filter(**dict_filter).values()[0]
    suburbs["s1"]["ainfo"] = SuburbInfo.objects.filter(**dict_filter).values()[0]

    crime_rate = 0.4
    if suburbs["s1"]["ainfo"]["crate"]:
        crime_rate = round(float(suburbs["s1"]["ainfo"]["crate"]), 2)

    crime_stars = [0] * 5
    if suburbs["s1"]["ainfo"]["crime_star"]:
        the_high = int(suburbs["s1"]["ainfo"]["crime_star"])
    else:
        the_high = 5

    if the_high > 5:
        the_high = 5
    for xindex in range(0, the_high):
        crime_stars[xindex] = 1

    suburbs["s1"]["ainfo"]["crate"] = crime_rate
    suburbs["s1"]["ainfo"]["crime_stars"] = crime_stars

    suburbs["s1"]["boundary"] = SuburbBoundary.objects.filter(suburb_id = int(suburb_id1)).values()[0]

    if suburbs["s1"]["ainfo"]["area_sq_km"]:
        area_sq_km = float(suburbs["s1"]["ainfo"]["area_sq_km"])
    else:
        area_sq_km = 0

    if suburbs["s1"]["ainfo"]["stops_count"]:
        stops_count = float(suburbs["s1"]["ainfo"]["stops_count"])
    else:
        stops_count = 0

    connectivity_index = 0
    if stops_count:
        connectivity_index = int(stops_count/ area_sq_km)

    suburbs["s1"]["ainfo"]["connectivity_index"] = connectivity_index
    if suburbs["s1"]["ainfo"]["distance_from_cbd"] > 100:
        suburbs["s1"]["ainfo"]["distance_from_cbd"] = "100+"
    else:
        suburbs["s1"]["ainfo"]["distance_from_cbd"] = round(float(suburbs["s1"]["ainfo"]["distance_from_cbd"]), 2)

    # get rent ratings
    suburbs["s1"]["rentchart"] = {}
    suburbs["s1"]["rentchart"] = {
        "1 Bedroom Flat": 0,
        "2 Bedroom Flat": 0,
        "3 Bedroom Flat": 0,
        "2 Bedroom House": 0,
        "3 Bedroom House": 0,
        "4 Bedroom House": 0
    }

    xs_rents = Rents.objects.filter(**{"suburb_id": int(suburb_id1)}).values()
    min_rent = 0
    for xsr in xs_rents:
        if xsr["property_category"] in suburbs["s1"]["rentchart"]:
            suburbs["s1"]["rentchart"][xsr["property_category"]] = xsr["rent_value"]

        if min_rent == 0:
            min_rent = xsr["rent_value"]
            suburbs["s1"]["min_rent"] = xsr

        if min_rent > xsr["rent_value"]:
            min_rent = xsr["rent_value"]
            suburbs["s1"]["min_rent"] = xsr

    # if "min_rent" in xsuburb:
    #     print(xsuburb["min_rent"])
    suburbs["s1"]["rents"] = xs_rents
    suburbs["s1"]["rentchart"]["rates"] = list(suburbs["s1"]["rentchart"].values())


    #### for second sububr logic
    dict_filter['id'] = int(suburb_id2);
    suburbs["s2"]["ginfo"] = Suburb.objects.filter(**dict_filter).values()[0]
    suburbs["s2"]["ainfo"] = SuburbInfo.objects.filter(**dict_filter).values()[0]

    crime_rate = 0.4
    if suburbs["s2"]["ainfo"]["crate"]:
        crime_rate = round(float(suburbs["s2"]["ainfo"]["crate"]), 2)

    crime_stars = [0] * 5
    if suburbs["s2"]["ainfo"]["crime_star"]:
        the_high = int(suburbs["s2"]["ainfo"]["crime_star"])
    else:
        the_high = 5

    if the_high > 5:
        the_high = 5
    for xindex in range(0, the_high):
        crime_stars[xindex] = 1

    suburbs["s2"]["ainfo"]["crate"] = crime_rate
    suburbs["s2"]["ainfo"]["crime_stars"] = crime_stars

    suburbs["s2"]["boundary"] = SuburbBoundary.objects.filter(suburb_id = int(suburb_id2)).values()[0]

    # print(suburbs["s2"])
    if suburbs["s2"]["ainfo"]["area_sq_km"]:
        area_sq_km = float(suburbs["s2"]["ainfo"]["area_sq_km"])
    else:
        area_sq_km = 0

    if suburbs["s2"]["ainfo"]["stops_count"]:
        stops_count = float(suburbs["s2"]["ainfo"]["stops_count"])
    else:
        stops_count = 0

    connectivity_index_first = connectivity_index
    connectivity_index = 0
    if stops_count:
        connectivity_index = int(stops_count/ area_sq_km)

    if connectivity_index_first < connectivity_index:
        better_connectivity = 2

    suburbs["s2"]["ainfo"]["connectivity_index"] = connectivity_index
    if suburbs["s2"]["ainfo"]["distance_from_cbd"] > 100:
        suburbs["s2"]["ainfo"]["distance_from_cbd"] = "100+"
    else:
        suburbs["s2"]["ainfo"]["distance_from_cbd"] = round(float(suburbs["s2"]["ainfo"]["distance_from_cbd"]), 2)

    # get rent ratings
    suburbs["s2"]["rentchart"] = {}
    suburbs["s2"]["rentchart"] = {
        "1 Bedroom Flat": 0,
        "2 Bedroom Flat": 0,
        "3 Bedroom Flat": 0,
        "2 Bedroom House": 0,
        "3 Bedroom House": 0,
        "4 Bedroom House": 0
    }

    xs_rents = Rents.objects.filter(**{"suburb_id": int(suburb_id2)}).values()
    min_rent = 0
    for xsr in xs_rents:
        # print(xsr["property_category"], suburbs["s2"]["rentchart"])
        if xsr["property_category"] in suburbs["s2"]["rentchart"]:
            suburbs["s2"]["rentchart"][xsr["property_category"]] = xsr["rent_value"]

        if min_rent == 0:
            min_rent = xsr["rent_value"]
            suburbs["s2"]["min_rent"] = xsr

        if min_rent > xsr["rent_value"]:
            min_rent = xsr["rent_value"]
            suburbs["s2"]["min_rent"] = xsr

    # if "min_rent" in xsuburb:

    suburbs["s2"]["rents"] = xs_rents
    suburbs["s2"]["rentchart"]["rates"] = list(suburbs["s2"]["rentchart"].values())
    print("rents rents", suburbs["s2"]["rents"])


    #### common parameters
    suburbs["s1"]["ainfo"]["better_connectivity"] = better_connectivity
    suburbs["s2"]["ainfo"]["better_connectivity"] = better_connectivity


    nearest_suburbs = get_nearby_suburbs(provider_info)

    df_nearest_suburbs = pd.DataFrame(nearest_suburbs)

    df_nearest_suburbs = df_nearest_suburbs.sort_values(
    by = ['crime_star', 'connectivity_index', 'provider_count', 'distance_from_cbd',
    'school_count', 'hospital_count', 'population', 'distance_in_km'],
    ascending= [False, False, False, True,
    False, False, True, True])

    sorted_nearest_suburbs = df_nearest_suburbs.to_dict("records")

    # delete suburb with no info in it
    delete_suburbs = []

    for idx, xsuburb in enumerate(sorted_nearest_suburbs):

        # get rent ratings
        xs_rents = Rents.objects.filter(**{"suburb_id": xsuburb["suburb_id"]}).values()
        min_rent = 0
        for xsr in xs_rents:
            if min_rent == 0:
                min_rent = xsr["rent_value"]
                xsuburb["min_rent"] = xsr

            if min_rent > xsr["rent_value"]:
                min_rent = xsr["rent_value"]
                xsuburb["min_rent"] = xsr

        # if "min_rent" in xsuburb:
        #     print(xsuburb["min_rent"])
        xsuburb["rents"] = xs_rents

        # get suburb schools
        xsuburb["schools"] = School.objects.filter(**{"suburb_id": xsuburb["suburb_id"]}).values()

        # get suburb Hospital
        xsuburb["hospitals"] = Hospital.objects.filter(**{"suburb_id": xsuburb["suburb_id"]}).values()

        # get suburb PtvStops
        xsuburb["stops"] = PtvStops.objects.filter(**{"suburb_id": xsuburb["suburb_id"]}).values()[0:9]

        # get suburb CrimeRate
        xsuburb["crime_rate"] = CrimeRate.objects.filter(**{"suburb_id": xsuburb["suburb_id"]}).values()

        # if len(xsuburb["rents"]) == 0 and len(xsuburb["schools"]) == 0 and len(xsuburb["hospitals"]) == 0 and len(xsuburb["stops"]) == 0:
        if len(xsuburb["schools"]) == 0:
            delete_suburbs.append(idx)


        # print(xsuburb)
    # print("nearest_suburbs", nearest_suburbs)
    for dindex in sorted(delete_suburbs, reverse=True):
        del sorted_nearest_suburbs[dindex]


    # just take the 5
    sorted_nearest_suburbs = sorted_nearest_suburbs[0:5]
    for idx, xsuburb in enumerate(sorted_nearest_suburbs):
        # recommended color
        xsuburb["fillColor"] = Color(colors[idx]).get_hex()
        xsuburb["fontColor"] = colors_font[idx]
        xsuburb["strokeColor"] = colors[idx].get_hex()

    if len(dict_filter) > 0:
        start_point = False
        # dict_filter['is_regional'] = int(show_regional);


        dict_filter['is_regional'] = int(show_regional);
        provider_list = VetProviders.objects.filter(**dict_filter).order_by("name")

        paginator = Paginator(provider_list, 10) # Show 25 contacts per page

        page = request.GET.get('page')
        providers = paginator.get_page(page)
    else:
        providers = []
        has_data = False

    return render(request, 'provider/templates/compare_suburbs.html',  {
        'provider_info': provider_info,
        'providers': providers,
        'suburbs': suburbs,
        'provider_filter': provider_filter,
        'show_regional': show_regional,
        'has_data': has_data,
        'start_point': start_point,
        'pages': pages,
        'nearest_suburbs': sorted_nearest_suburbs
    })


def finder(request):
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
            # dict_filter['category_id'] = search_filter["category"]
            # dict_filter_contains['category_id'] = search_filter["category"]
    except:
        print("")

    try:
        if request.GET.get('location'):
            search_filter["location"] = request.GET.get('location')
    except:
        print("")

    location_chunks = search_filter["location"].split(",")
    dict_filter_2 = {}
    dict_filter_2["postcode"] = int(location_chunks[1])
    dict_filter_2["government_subsidised"] = 'Y'
    provider_list = VetProviders.objects.filter(**dict_filter_2).values()
    print("list of providers", len(provider_list))
    print(provider_list)
    totals["courses"] = len(provider_list)

    d1 = datetime.strptime('1/04/2020 1:30 PM', '%m/%d/%Y %I:%M %p')
    d2 = datetime.strptime('1/06/2020 4:50 AM', '%m/%d/%Y %I:%M %p')

    providers_from_list = []
    totals["pharmacy"] = 0
    totals["individuals"] = 0

    for xitem in provider_list:
        i = 0
        xitemtemp = xitem

        xitemtemp["title"] = xitemtemp["address_line_2"]

        if (xitemtemp["is_regional"] == 1):
            totals["pharmacy"] += 1
            qty_inHand = randrange(30, 100, 3)
            xitemtemp["availability"] = qty_inHand
            xitemtemp["desc"] = "Our store has " + str(qty_inHand) + " packs of mask, please check in store before pickup."
        else:
            totals["individuals"] += 1
            qty_inHand = randrange(10, 30, 2)
            xitemtemp["availability"] = qty_inHand
            xitemtemp["desc"] = "Hi, I'm " + xitemtemp["address_line_2"] + ", I have some extra masks to share."
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

    if search_filter["occupation"]:
        current_filter += "q=" + search_filter["occupation"] + "&"

    category_filter_name = ""
    # if search_filter["category"]:
    #     course_category_info = VetProfessionsCategory.objects.filter(id=search_filter["category"]).values()[0]
    #     print(course_category_info)
    #     category_filter_name = course_category_info["name"]
    #     current_filter += "cf=" + category_filter_name + "&"

    return render(request, 'provider/templates/product_finder.html',  {
        'occupations': occupations,
        'filters': search_filter,
        'occupation_filter': search_filter["occupation"],
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
