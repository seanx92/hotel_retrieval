import json
import shelve
from tokenization import tokenize
import time

def buildInvertedIndex(hotel_data):
    '''This function is used for building the index of address to hotel.

       Index for the whole address include: region, street, city, tostal-code, locality. 
    '''
    name_result = {}
    address_result = {}
    score_result = {}
    for hotel_id in range(13000):#hotel_data:
        hotel_id = str(hotel_id)
        #for name to hotel index
        if hotel_id in hotel_data:
            print hotel_id#, hotel_data[hotel_id]
            l_name = tokenize(hotel_data[hotel_id]["name"])
            for term in l_name:
                if term not in name_result.keys():
                    name_result[term] = []
                if hotel_id not in name_result[term]:
                    name_result[term].append(hotel_id)
            #for address to hotel index
            l_address = []
            address_dic = hotel_data[hotel_id]["address"]
            for sub_address in address_dic:#handle each sub-address of the address: region, locality, street, postal-code
                l_address.extend(tokenize(address_dic[sub_address]))
            for term in l_address:
                if term not in address_result.keys():
                    address_result[term] = []
                if hotel_id not in address_result[term]:
                    address_result[term].append(hotel_id)
            #for scores
            average_scores = {}        
            for review_id in hotel_data[hotel_id]["reviews"]:
                for aspect in hotel_data[hotel_id]["reviews"][review_id]["ratings"]:
                    if aspect not in average_scores:
                        average_scores[aspect] = 0
                    if hotel_data[hotel_id]["reviews"][review_id]["ratings"][aspect] != "":
#                    print type(result[id]["reviews"][review_id]["ratings"][aspect])
                        average_scores[aspect] += float(hotel_data[hotel_id]["reviews"][review_id]["ratings"][aspect])
            for average_score in average_scores:
                average_scores[average_score] /= len(hotel_data[hotel_id]["reviews"])
            score_result[hotel_id] = average_scores
    return (name_result, address_result, score_result)

def nameToHotel(hotel_data):
    '''This function is used for building the index of hotel name to hotel id.

       Index for build from the name part.
    '''
    result = {}
    for id in hotel_data:
#        print tokenize(hotel_data[id]["name"])
        l = tokenize(hotel_data[id]["name"])
        for term in l:
            if term not in result.keys():
                result[term] = []
            if id not in result[term]:
                result[term].append(id)
#    print result
    return result

def getAverageScores(hotel_data):
    '''This function is used for calculate the average scores of overall scores and other aspect scores.

    '''
    result = {}
    for id in hotel_data:
        result[id] = hotel_data[id]
        average_scores = {}
#        if id == "994":
#            print id, hotel_data[id]
        for review_id in result[id]["reviews"]:
            for aspect in result[id]["reviews"][review_id]["ratings"]:
                if aspect not in average_scores:
                    average_scores[aspect] = 0
                if result[id]["reviews"][review_id]["ratings"][aspect] != "":
#                    print type(result[id]["reviews"][review_id]["ratings"][aspect])
                    average_scores[aspect] += float(result[id]["reviews"][review_id]["ratings"][aspect])
        for average_score in average_scores:
            average_scores[average_score] /= len(hotel_data[id]["reviews"])
#        print average_scores
        result[id]["average_scores"] = average_scores
 #   print result
    return result

def buildIndex(): 
    '''This function is used for writing the index data to database.


    '''
    address_Hotel = shelve.open('hotels/static/data/index_addressToHotel.db')
    name_Hotel = shelve.open('hotels/static/data/index_nameHotel.db')
    hotels = shelve.open('hotels/static/data/hotel_score.db')
    with open('hotels/static/data/hotel_data.json') as f:
        hotel_data = json.load(f)
    n_t_data, a_t_data, h_data = buildInvertedIndex(hotel_data)
#    print n_t_data
    try:
        for term in a_t_data:
            address_Hotel[term] = a_t_data[term]
        for term in n_t_data:
            name_Hotel[term] = n_t_data[term]
        for id in h_data:
            hotels[str(id)] = h_data[id]
    finally:
        address_Hotel.close()
        name_Hotel.close()
        hotels.close()

start = time.time()
buildIndex()
print "building time is", time.time() - start
#with open('toy_data.json') as f:
#    hotel_data = json.load(f)
#getAverageScores(hotel_data)
