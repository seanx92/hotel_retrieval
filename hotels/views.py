from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import JsonResponse
from search import search
import shelve
from result import myResult
from search_reviews import searchThroughSearchBar, searchThroughTags

r = myResult()
# Create your views here.
def home(request):
    # return render(request, 'hotels/hotel.html', {})
    return render(request, 'hotels/home.html', {})

def search_query(request):
    title = request.POST.get("title")
    location = request.POST.get("location")
    tags = request.POST.get("tags")

    tags = ["service", "sleep_quality","cleanliness", "location"]

    result = search(title, location, True, tags)
    r.put(result)

    return JsonResponse(result, safe=False)

def hotel(request, hotel_id = '100000'):
    # details = r.get(hotel_id)
    # detail = details[1]
    # detail["reviews_total"] = details[0]

    # if request.method == 'POST':
    #     hotel_id = request.POST.get("hotel_id")
    #     query = request.POST.get("query")
    #     print hotel_id, query
    #     # detail = searchThroughSearchBar(hotel_id, query)
    #     detail["reviews"] = searchThroughTags("11544", False, ["cleanliness", "service"])
        # if search_result is not None:
        #     request.session.review = search_result


    return render(request, 'hotels/hotel.html', {})

def hotel_detail(request, index_id = 0):
    search_result = []
    detail = r.get(index_id)


    if request.method == 'POST':
        hotel_id = request.POST.get("hotel_id")
        query = request.POST.get("query")
        print hotel_id, query, type(hotel_id)
        search_result = searchThroughTags(str(hotel_id), False, ["cleanliness", "service"])

    elif request.method == 'GET':
        print("get")

    if len(search_result) > 0:
        # print(search_result)
        detail[1]["good_reviews"] = search_result[0]
        detail[1]["bad_reviews"] = search_result[1]
        print(detail[1]["reviews"])
    
    detail[1]["reviews_total"] = len(detail[1]["reviews"])

    return JsonResponse(detail, safe=False)


    # result = searchThroughSearchBar(2514711, "apple")

    # return JsonResponse(result, safe=False)
