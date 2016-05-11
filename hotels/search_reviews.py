from elasticsearch import Elasticsearch

def searchThroughSearchBar(hotel_id, query):
    '''This function is used for search reviews of a hotel by query.

       hotel_id is the hotel_id in hotels.db
       query is input query from review search bar. 

    '''
    es = Elasticsearch()
    indexName = "reviews_es_index"
    doc_type = "review"
    query_body = {
                   "query": {
                        "bool": {
                            "must": [],
                            "should":[]
                         }
                    },
                   "highlight":{
                        "pre_tags":['<em style="background-color:yellow">'],
                        "post_tags":["</em>"],
                        "fields":{"content":{"fragment_size": 500}}
                 }}
    query_body["query"]["bool"]["must"].append({"match":{"hotel_id":hotel_id}})
    query_body["query"]["bool"]["should"].append({"match":{"content":query}})
    query_body["query"]["bool"]["should"].append({"match":{"title":query}})
    res = es.search(indexName, body=query_body)
    res = res["hits"]["hits"]
    for i in range(len(res)):
        res[i] = res[i]["_source"]
    return res

def searchThroughTags(hotel_id, only_overall=True, tags=["cleanliness", "service", "value", "location", "sleep_quality", "rooms"]):
    '''This function is used for search reviews by clicking tags. It will return two class of reviews, one is high score reviews and the other is low score reviews.

       If the only_overall flag set to True, the function will return high over score reviews and low overall score reviews.
       If the flag set to false, the function will return two classes of result based on the scores of each field in the tags.
    '''
    es = Elasticsearch()
    indexName = "reviews_es_index"
    doc_type = "review"
    query_body1 = getQueryTemplate(hotel_id)
    query_body2 = getQueryTemplate(hotel_id)        
    if only_overall:
        query_body1["query"]["bool"]["must"].append({"range":{"ratings.overall":{"gt":3.0}}})
        query_body2["query"]["bool"]["must"].append({"range":{"ratings.overall":{"lt":3.0}}})
    else:
        query_body1["query"]["bool"]["must_not"] = {}
        query_body2["query"]["bool"]["must_not"] = {}
        query_body1["query"]["bool"]["must_not"]["range"] = {}
        query_body2["query"]["bool"]["must_not"]["range"] = {}
        for tag in tags:
            query_body1["query"]["bool"]["should"].append({"range":{"ratings."+tag:{"gt":3.0}}})
            query_body1["query"]["bool"]["must_not"]["range"]["ratings."+tag] = {"lt":3.0}
            query_body2["query"]["bool"]["should"].append({"range":{"ratings."+tag:{"lt":3.0}}})
            query_body2["query"]["bool"]["must_not"]["range"]["ratings."+tag] = {"gt":3.0}
    res1 = es.search(indexName, body=query_body1)["hits"]["hits"]
    res2 = es.search(indexName, body=query_body2)["hits"]["hits"]
    for i in range(len(res1)):
        res1[i] = res1[i]["_source"]
    for i in range(len(res2)):
        res2[i] = res2[i]["_source"]
    return (res1, res2)

def getQueryTemplate(hotel_id):
    query_body = {
                   "query": {
                        "bool": {
                            "must": [{"match":{"hotel_id":hotel_id}}],
                            "should":[]
                         }
                    },
                   "highlight":{
                        "pre_tags":['<em style="background-color:yellow">'],
                        "post_tags":["</em>"],
                        "fields":{"content":{"fragment_size": 500}}
                 }}
    return query_body

#print searchReviews("11544", "credit card company") 
#res = searchThroughTags("11544")
#res = searchThroughTags("11544", False, ["cleanliness", "service"])
#print res[0]
#print "-----------------------------------------------"
#print res[1] 
