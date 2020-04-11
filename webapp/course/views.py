from django.shortcuts import render
from django.core.paginator import Paginator

from django.http import HttpResponse, JsonResponse

# to avoid 403 forbidden error
from django.views.decorators.csrf import csrf_exempt
from course.models import *
from provider.models import *
from occupation.models import *

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db import connection

from datetime import datetime
from random import randrange
from datetime import timedelta


def index(request):
    dict_data = {}
    dict_filter = {}
    course_filter = ""
    course_subsidized = ""
    course_apprenticeship = ""
    course_traineeship = ""

    try:
        if request.GET.get('q'):
            course_filter = request.GET.get('q')
            dict_filter['course_title__icontains'] = course_filter;

        if request.GET.get('subsidized'):
            course_subsidized = int(request.GET.get('subsidized'))
            dict_filter['government_subsidised'] = course_subsidized;

        if request.GET.get('apprenticeship'):
            course_apprenticeship = int(request.GET.get('apprenticeship'))
            dict_filter['apprenticeship'] = course_apprenticeship;

        if request.GET.get('traineeship'):
            course_traineeship = int(request.GET.get('traineeship'))
            dict_filter['traineeship'] = course_traineeship;
    except:
        print("")

    category_filter = ""
    try:
        if request.GET.get('cf'):
            category_filter = request.GET.get('cf')


            if category_filter == "certificates":
                dict_filter['qualification_level__in'] = ["Certificate I", "Certificate II", "Certificate III", "Certificate IV"]

            if category_filter == "diploma":
                dict_filter['qualification_level__in'] = ["Advanced Diploma", "Diploma"]

            if category_filter == "graduate":
                dict_filter['qualification_level__in'] = ["Graduate Diploma", "Graduate Certificate"]

            if "qualification_level__in" not in dict_filter:
                dict_filter['qualification_level'] = category_filter

    except:
        print("")

    has_data = True
    start_point = True
    pages = []
    page_count = 0

    if len(dict_filter) > 0:
        start_point = False
        course_list = VetCourses.objects.filter(**dict_filter)

        paginator = Paginator(course_list, 10) # Show 25 contacts per page

        page = request.GET.get('page')
        courses = paginator.get_page(page)
        pages = list(paginator.page_range)
        page_count = len(pages)
    else:
        courses = []
        has_data = False

    current_filter = "?"

    if course_filter:
        current_filter += "q=" + course_filter + "&"

    if category_filter:
        current_filter += "cf=" + category_filter + "&"

    return render(request, 'course/templates/index.html',  {
        'courses': courses,
        'course_filter': course_filter,
        'category_filter': category_filter,
        'current_filter': current_filter,
        'subsidized': course_subsidized,
        'apprenticeship': course_apprenticeship,
        'traineeship': course_traineeship,
        'has_data': has_data,
        'start_point': start_point,
        'pages': pages,
        'page_count': page_count
    })


def results(request):

    return render(request, 'course/templates/results.html')

def providers(request, course_id):
    dict_data = {
        "course_id": int(course_id)
    }

    dict_filter = {}
    course_filter = ""

    has_data = True
    start_point = True

    course_details = VetCourses.objects.filter(id=dict_data["course_id"]).all()[0]
    print(course_details)

    provider_from_courses = VetCoursesToProvider.objects.filter(course_id=dict_data["course_id"]).extra(
      select={
        'id': 'campus_id'
      }
    ).values(
      'id'
    )
    # print(provider_from_courses)

    provider_list = VetProviders.objects.filter(id__in=provider_from_courses).order_by("name")

    if len(provider_list)>0:
        has_data = True
    else:
        has_data = False

    paginator = Paginator(provider_list, 10) # Show 25 contacts per page

    page = request.GET.get('page')
    providers = paginator.get_page(page)

    return render(request, 'provider/templates/course_providers.html',  {
        'providers': providers,
        'course_details': course_details,
        'has_data': has_data,
    })


@csrf_exempt
def details(request, course_id):
    dict_data = {
        "course_id": course_id
    }

    return JsonResponse(dict_data)


@csrf_exempt
def fetch(request):
    dict_data = {}

    search_query = request.POST.get('search', '')

    requested_data = []
    # querySet = VetProviders.objects.filter(name__icontains=search_institutes)
    querySet = VetCourses.objects.filter(course_title__icontains=search_query).values("course_title").annotate(n=models.Count("pk"))[0:9]
    for qset in querySet:
        requested_data.append(qset["course_title"]);

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
    querySet = VetCourses.objects.filter(
        Q(course_title__icontains = search_query) |
        Q(course_code__icontains = search_query) |
        Q(course_code__icontains = search_query)
    ).values()[0:9]

    # print(len(querySet))

    # set user query back in the result
    if search_query:
        requested_data.append({
            "id": search_query,
            "text": search_query
        });

    for qset in querySet:
        # print(qset)
        requested_data.append({
        "id": qset["id"],
        "text": qset["course_title"]
        });

    dict_data = {
        "results": requested_data,
        # "search": search_query
    }

    return JsonResponse(dict_data)

@csrf_exempt
def fetch_data(request):
    dict_data = {}

    search_query = request.POST.get('search', '')

    requested_data = []
    # querySet = VetProviders.objects.filter(name__icontains=search_institutes)
    querySet = VetCourses.objects.filter(
        Q(course_title__icontains = search_query) |
        Q(course_code__icontains = search_query) |
        Q(course_code__icontains = search_query)
    ).values()[0:9]

    # print(len(querySet))

    # set user query back in the result
    # if search_query:
    #     requested_data.append({
    #         "id": search_query,
    #         "text": search_query
    #     });

    for qset in querySet:
        # print(qset)
        requested_data.append(qset["course_title"])

    dict_data = {
        "results": requested_data,
        # "search": search_query
    }

    return JsonResponse(dict_data)


future_growth_map = {}
future_growth_map["Decline"] = { "class": "danger", "icon": '<i class="fa fa-caret-down"></i>' }
future_growth_map["Moderate"] = { "class": "warning", "icon": '<i class="fa fa-minus"></i>' }
future_growth_map["Stable"] = { "class": "info", "icon": '<i class="fa fa-caret-right"></i>' }
future_growth_map["Strong"] = { "class": "success", "icon": '<i class="fa fa-caret-up"></i>' }
future_growth_map["Very strong"] = { "class": "success", "icon": '<i class="fa fa-fighter-jet"></i>' }


skill_map = {}
skill_map["Entry level"] = { "class": "success", "icon": '<i class="fa fa-caret-down"></i>' }
skill_map["Lower skill"] = { "class": "success", "icon": '<i class="fa fa-minus"></i>' }
skill_map["Medium skill"] = { "class": "warning", "icon": '<i class="fa fa-caret-right"></i>' }
skill_map["High skill"] = { "class": "danger", "icon": '<i class="fa fa-caret-up"></i>' }
skill_map["Very high skill"] = { "class": "danger", "icon": '<i class="fa fa-fighter-jet"></i>' }

def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


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
            dict_filter['category_id'] = search_filter["category"]
            dict_filter_contains['category_id'] = search_filter["category"]
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

    if search_filter["occupation"]:
        current_filter += "q=" + search_filter["occupation"] + "&"

    category_filter_name = ""
    if search_filter["category"]:
        course_category_info = VetProfessionsCategory.objects.filter(id=search_filter["category"]).values()[0]
        print(course_category_info)
        category_filter_name = course_category_info["name"]
        current_filter += "cf=" + category_filter_name + "&"

    return render(request, 'course/templates/course_finder.html',  {
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
