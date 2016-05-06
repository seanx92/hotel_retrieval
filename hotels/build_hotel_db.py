import shelve
import json

def buildHotelsDB():
    '''This function is used for building hotel database.
    '''
    hotels = shelve.open('hotels/static/data/hotels.db')
    with open('hotels/static/data/hotel_data.json') as f:
        hotel_data = json.load(f)

    try:
        for hotel_id in hotel_data:
            print hotel_id
            hotels[str(hotel_id)] = hotel_data[hotel_id]
    finally:
        hotels.close()

buildHotelsDB()
