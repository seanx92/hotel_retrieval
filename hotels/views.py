from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import JsonResponse
from search import search

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

    print result[0][0]
    for k, v in result[0][1].iteritems():
        print k, v
    # if request.is_ajax():
    #     result = res    
    # else:
    #     result = "Not ajax"
    return JsonResponse(result, safe=False)
