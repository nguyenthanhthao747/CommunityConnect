from django.shortcuts import render
from django.core.paginator import Paginator

from django.http import HttpResponse, JsonResponse

# to avoid 403 forbidden error
from django.views.decorators.csrf import csrf_exempt
from occupation.models import *
from course.models import *

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db import connection

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


def index(request):
    dict_data = {}
    dict_filter = {}
    occupation_filter = ""
    high_demand = ""
    try:
        if request.GET.get('occupation_filter'):
            occupation_filter = request.GET.get('occupation_filter')
            dict_filter['title__icontains'] = occupation_filter;

        if request.GET.get('high_demand'):
            high_demand = int(request.GET.get('high_demand'))
        else:
            high_demand = 0

    except:
        print("")

    has_data = True
    start_point = True
    pages = []
    page_count = 0

    if len(dict_filter) > 0:
        start_point = False

        dict_filter['high_demand'] = high_demand;

        occupation_list = VetOccupations.objects.filter(**dict_filter)

        paginator = Paginator(occupation_list, 20)

        page = request.GET.get('page')
        occupations = paginator.get_page(page)
    else:
        occupations = []
        has_data = False

    # occupation = occupations.values()[0]

    return render(request, 'occupation/templates/index.html',  {
        # 'occupation': occupation,
        'occupations': occupations,
        'occupation_filter': occupation_filter,
        'high_demand': high_demand,
        'has_data': has_data,
        'start_point': start_point,
        'pages': pages,
        'page_count': page_count
    })

def results(request):

    return render(request, 'occupation/templates/results.html')

def courses(request, occupation_id):
    dict_data = {
        "occupation_id": int(occupation_id)
    }

    dict_filter = {}
    occupation_filter = ""

    occupation_details = VetOccupations.objects.filter(id=dict_data["occupation_id"]).all().values()[0]
    print(occupation_details)
    anzsco_filter = int(occupation_details["anzsco_id"])
    print(anzsco_filter)

    courses_from_occupation = VetCoursesToOccupation.objects.filter(anzsco=anzsco_filter).values().extra(
      select={
        'id': 'course_id'
      }
    ).values(
      'id'
    )
    print(courses_from_occupation)

    course_list = VetCourses.objects.filter(id__in=courses_from_occupation).order_by("course_title")

    paginator = Paginator(course_list, 10) # Show 25 contacts per page

    page = request.GET.get('page')
    courses = paginator.get_page(page)

    return render(request, 'course/templates/course_occupations.html',  {
        'courses': courses,
        'occupation_details': occupation_details,
    })

@csrf_exempt
def details(request, occupation_id):
    dict_data = {}
    dict_filter = {}
    dict_filter_contains = {}
    occupation_filter = ""
    high_demand = ""
    totals = {}
    occupation = {}
    totals["courses"] = 0

    try:
        dict_filter['id'] = int(occupation_id)
    except:
        print("")

    has_data = True
    start_point = True
    pages = []
    page_count = 0

    if len(dict_filter) > 0:
        start_point = False

        # dict_filter['high_demand'] = high_demand;

        occupation_list = VetOccupations.objects.filter(**dict_filter).values()

        if len(occupation_list) <= 0:
            occupation_list = VetOccupations.objects.filter(**dict_filter_contains).values()

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
            totals["courses"] += len(xitem["courses"])

            if xitem["future_growth"] in future_growth_map:
                xitem["future_growth_info"] = future_growth_map[xitem["future_growth"]]

            if xitem["skill_level"] in skill_map:
                xitem["skill_level_info"] = skill_map[xitem["skill_level"]]

        occupation = occupation_list.values()[0]

        totals["occupations"] = len(occupation_list)
        paginator = Paginator(occupation_list, 20)

        page = request.GET.get('page')
        occupations = paginator.get_page(page)


    else:
        occupations = []
        has_data = False

    return render(request, 'occupation/templates/occupation_details.html',  {
        'occupation': occupation,
        'occupations': occupations,
        'occupation_filter': occupation_filter,
        'high_demand': high_demand,
        'has_data': has_data,
        'start_point': start_point,
        'pages': pages,
        'page_count': page_count,
        'totals': totals
    })


@csrf_exempt
def fetch(request):
    dict_data = {}

    search_query = request.POST.get('search', '')

    requested_data = []
    # querySet = VetProviders.objects.filter(name__icontains=search_institutes)
    querySet = VetOccupations.objects.filter(title__icontains=search_query).order_by("title").values("title").annotate(n=models.Count("pk"))[0:9]
    for qset in querySet:
        requested_data.append(qset["title"]);

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
    querySet = VetOccupations.objects.filter(
        Q(title__icontains = search_query) |
        Q(anzsco_id__icontains = search_query) |
        Q(description__icontains = search_query)
    ).order_by("title").values().annotate(n=models.Count("pk"))[0:9]

    # print(len(querySet))

    for qset in querySet:
        # print(qset)
        requested_data.append({
            "id": qset["id"],
            "text": qset["title"]
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
vp.title,
(SELECT vpc.name from vet_professions_category vpc WHERE vpc.id = vp.category_id) as category_name
FROM vet_professions vp
WHERE
(title LIKE '{search_query}%')
LIMIT 50
    """

    cursor = connection.cursor();
    cursor.execute(sql_str)
    the_rs = cursor.fetchall()

    if len(the_rs) == 0:
        # if no results found in case of starts with
        the_rs = VetProfessions.objects.filter(title__icontains=search_query).values().annotate(n=models.Count("pk"))[0:50]

        for qset in the_rs:
            category_info = VetProfessionsCategory.objects.filter(id=qset["category_id"]).values()[0]
            print(category_info)

            requested_data.append({
                'label': qset["title"].strip(),
                'category': category_info["name"]
            })

    # display starts with results
    else:
        for qset in the_rs:
            # print(qset)
            requested_data.append({
                'label': qset[0].strip(),
                'category': qset[1]
            })

    dict_data = {
        "results": requested_data,
        "search": search_query
    }

    return JsonResponse(dict_data)
