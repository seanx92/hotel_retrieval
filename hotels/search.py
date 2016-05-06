import shelve
import time
import heapq
from tokenization import tokenize

def search(name, address, onlyOverall=True, tags=["cleanliness", "service", "value", "location", "sleep_quality", "rooms"]):
    ''' This function is used for finding the conjunctive result by searching by "address" and "name".

    '''
    address_search_result = searchByAddress(address)
    name_search_result = searchByName(name)
    if len(address_search_result) == 0 and len(name_search_result) == 0:
        return getDefaultData()
    elif len(address_search_result) == 0:#if no search resuls for address search return, final result is the result of name search
        result = name_search_result
    elif len(name_search_result) == 0:#if no search result for name search retuan, final result is the result of address search
        result = address_search_result
    else:#if both of the address and name search have results, intersect the result
        if len(address_search_result) > len(name_search_result):
            result = intersect_two(name_search_result, address_search_result)
        else:
            result = intersect_two(address_search_result, name_search_result)
#        if len(result) == 0:#if no result after intersection, use the result of address search as final result
#            print "I'm in the no intersected result part"
#            result = address_search_result
#    print "time before ranking is:", time.time() - start
#    print result
    return rankResult(result, onlyOverall, tags)

def rankResult(result_ids, onlyOverall=True, tags=["cleanliness", "service", "value", "location", "sleep_quality", "rooms"]):
    '''This function is used for rank the results by overall rating or tags.

    '''
    hotel_score = shelve.open('hotels/static/data/hotel_score.db')
    result = []
    for id in result_ids:
        result.append((id, hotel_score[str(id)]))
    if onlyOverall:
        result = rankByOverall(result)
    else:
        result = rankByTags(result, tags)
    hotel_score.close()
    mid3 = time.time()
    hotels = shelve.open('hotels/static/data/hotels.db')
    for i in range(len(result)):
        result[i] = (str(result[i]),hotels[str(result[i])])
    hotels.close()
    print "read hotel data from db time is:", time.time() - mid3
    return result

def rankByOverall(hotel_list):
    '''This function rank the input hotel_list with the average overall rating.

    '''
    temp = []
    for hotel_tuple in hotel_list:
        temp.append((float(hotel_tuple[1]["overall"]), hotel_tuple[0]))
    result = getTopResults(temp)
    return result#sorted(hotel_list, key=lambda x: x[1]["average_scores"]["overall"], reverse=True)


def rankByTags(hotel_list, tags):
    '''This function rank the input hotel_list with the weighted averaged rating for the given tag list.

    '''
    length = len(tags)
    temp = []
    result = []
    for hotel_tuple in hotel_list:
        score = 0
        for tag in tags:
            score += hotel_tuple[1][tag]
        score /= length
        temp.append((score, hotel_tuple[0]))
    result = getTopResults(temp)
    return result

def getTopResults(hotel_scores):
    h = []
    result = []
    count = 30#how many results need to be return
    for h_s in hotel_scores:
        if count > 0:
            heapq.heappush(h, h_s)
            count = count - 1
        elif h_s[0] > h[0]:
            heap.heappushpop(h, h_s)
    h.sort(key=lambda x: x[0], reverse=True)
    for hotel_scores in h:
        result.append(hotel_scores[1])
    return result

def searchByName(name):
    '''This function is used for searching by name.

    '''
    name_hotel = shelve.open('hotels/static/data/index_nameHotel.db')
    query_list = tokenize(name)
    keys = name_hotel.keys()
    result = []
    for term in query_list:
        if term in keys:
            result.append(name_hotel[term])
    if len(result) > 1:
        result = intersect(result)
    elif len(result) == 1:
        result = result[0]
    name_hotel.close()
    return result

def searchByAddress(address):
    '''This function is used for searching by address.

    '''
    address_hotel = shelve.open('hotels/static/data/index_addressToHotel.db')
    query_list = tokenize(address)
    result = []
    keys = address_hotel.keys()
    for term in query_list:
        if term in keys:
            result.append(address_hotel[term])
    if len(result) > 1:
        result = intersect(result)
    elif len(result) == 1:
        result = result[0]
    address_hotel.close()
    return result

def intersect(resultLists):
    '''This function is used for intersecting given lists.

    '''
    resultLists.sort(key=lambda x: len(x))
    result = resultLists[0]
    i = 1
    while i < len(resultLists):
        result = intersect_two(result, resultLists[i])
        i += 1
    return result

def intersect_two(resultList1, resultList2):
    '''This function is used for intersecting two given lists.

        It is useful for intersect() function and when intersect the search result getting from name searching and address searching. 
    '''
    result = []
    i = 0
    j = 0
    while i < len(resultList1) and j < len(resultList2):
        if int(resultList1[i]) == int(resultList2[j]):
            result.append(resultList1[i])
            i = i + 1
            j = j + 1
        elif int(resultList1[i]) < int(resultList2[j]):
            i = i + 1
        else:
            j = j + 1
    return result

def getDefaultData():
    hotels = shelve.open('hotels/static/data/hotels.db')
    result = []
    i = 30
    j = 0
    while i > 0:
        if str(j) in hotels:
            result.append((str(j), hotels[str(j)]))
            i = i - 1
        j = j + 1
    hotels.close()
    return result

# start = time.time()
# result = search('hilton', 'new york', False, ["service", "sleep_quality","cleanliness", "location"])
# # result = search('continental','')
# print "uses time:", time.time() - start
# print "there are", len(result), "hits"
# #print result
# for item in result:
#     #print item["name"]
#     print item[0], item[1]["name"], item[1]["hotel_id"]#, item["address"]
# #print search('', 'hotel', False, ["cleanliness"])'''
