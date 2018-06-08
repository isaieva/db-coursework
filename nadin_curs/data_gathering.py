from datetime import datetime
from instagram_web_api import Client
from pymongo import MongoClient
from threading import Timer
import time


class WebAPIExportManager(object):

    def __init__(self, connection_url='localhost', port=27017):
        self.web_api = Client(auto_patch=True, drop_incompat_keys=False)
        self.mongo_client = MongoClient(connection_url, port=port)

    def write_to_mongo(self, collection, record):
        db = self.mongo_client.test_db
        collection = db[collection]
        collection.insert(record)

#from data_gathering import WebAPIExportManager
#api = WebAPIExportManager
#api.get_account('...')
    def get_account(self, account_name='nadine__is'):
        try:
            full_data = self.web_api.user_info2(account_name)
            clear_data = {
                'id': full_data.get('id'),
                'date': datetime.utcnow(),
                'name': full_data.get('full_name'),
                'username': full_data.get('username'),
                'followers': full_data.get('counts').get('followed_by'),
                'posts': full_data.get('edge_owner_to_timeline_media').get('count'),
            }
            likes = comments = count = 0
            for post in full_data.get('edge_owner_to_timeline_media').get('edges'):
                likes += post['node']['edge_liked_by']['count']
                comments += post['node']['edge_media_to_comment']['count']
                count += 1
            clear_data['likes'] = likes
            clear_data['comments'] = comments
            clear_data['engagement_rate'] = (likes+comments)*100/(clear_data['followers']*count)
            self.write_to_mongo('accounts', clear_data)
            return 'Account seccesfuly scraped'
        except Exception as ex:
            print(str(ex))
            return 'Something went wrong'


#api.day_account_scrap('...')
    def day_account_scrap(self, account_name):
        while True:
            self.get_account(account_name=account_name)
            today = datetime.today()
            tomorrow = today.replace(day=today.day + 1, hour=0, minute=0, second=0)
            delta_time = tomorrow - today
            seconds = delta_time.seconds + 1
            print(f'Next scrap will be {tomorrow}')
            time.sleep(seconds)
