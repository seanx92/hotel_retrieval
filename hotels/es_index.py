from elasticsearch import Elasticsearch, helpers
import json
import time
import sys

def build_review_index():
    '''This function is used for building elasticsearch index for reviews.

    '''
    es = Elasticsearch()
    schema = createSetting()
    indexName = "reviews_es_index"
    es.indices.delete(index=indexName, ignore=[400,404])
    es.indices.create(index=indexName,body=schema)
    doc_type = "review"
    hotel_data = json.loads(open("reviews.json").read())
    #hotel_data = json.loads(open("reviews.json").read())
    actions = []
    for key, value in hotel_data.iteritems():
        formatted_result = {"_index": indexName, "_type": doc_type, "_id": int(key), "_source":value}
        actions.append(formatted_result)
        print key
    helpers.bulk(es, actions, stats_only=True, refresh=True)

def createSetting():
    '''This function created a setting schema for building index.


    '''
    settings = {}
    settings["mapping"] = {}
    settings["mapping"]["review"] = {"_all": {"enabled": "true", "store": "yes"}}
    settings["mapping"]["properties"] = {"hotel_id": {"type": "string", "index":"not_analyzed"}, "review_id": {"type": "string", "index": "no", "include_in_all":"false"}, "content":{"type": "string", "store": "yes", "analyzer": "snowball_analyzer"}, "ratings":{"type": "object", "properties": {"service":{"type":"double"}, "cleanliness":{"type":"double"}, "overall":{"type":"double"}, "location":{"type":"double"}, "sleep_quality":{"type":"double"}, "rooms":{"type":"double"}}}, "title":{"type": "string", "store": "yes", "analyzer": "snowball_analyzer"}, "date":{"type": "string", "index": "no", "include_in_all":"false"}, "author_location":{"type": "string", "index": "no", "include_in_all":"false"}}
    settings["settings"] = {"index": {"analysis": {"analyzer": {"analyzer_lower": {"lowercase": "true", "type": "standard"}, "snowball_analyzer": {"type": "snowball", "language": "English"}}}}}
    return settings

start = time.time()
build_review_index()
print time.time() - start
