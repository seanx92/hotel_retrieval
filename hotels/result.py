class myResult(object):

    def __init__(self):
        self.hotel_info = []

    def put(self, hotel_list):
        self.hotel_info = hotel_list

    def get(self, hotel_id):
        for i in self.hotel_info:
            if i[0] == hotel_id:
                return i
            