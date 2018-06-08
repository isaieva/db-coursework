from pymongo import MongoClient
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd
import pylab
from datetime import date, datetime
import numpy as np


class DataProcessing(object):

    def __init__(self):
        self.client = MongoClient('localhost', port=27017)
        self.db = self.client.test_db
        self.collection = self.db.accounts


#from data_processing import DataProcessing
#d = DataProcessing()
#d.top_entity(entity = 'likes..')

    def top_entity(self, entity='followers'):
        """
        Plot top entity
        :param entity: Chose one of entities (followers, engagement_rate, likes, comments). 'followers' by default.
        :type entity: str
        :return:
        """

        loc_df = pd.DataFrame(list(self.collection.aggregate(
            [
                {
                    '$sort': {'date': 1}
                },
                {
                    '$group':
                        {
                            '_id': '$username',
                            'date': {'$last': '$date'},
                            f'{entity}': {'$last': f'${entity}'}
                        }
                }
            ]
        )))
        loc_df.plot(x='_id', y=f'{entity}', kind='bar')
        pylab.show()


#from datetime import datetime
#d.entity_progress(['...', '...'], date_min = datetime(2018,6,5), date_max = datetime(2018,6,8))
    def entity_progress(self, usernames, date_min=datetime(2017, 1, 1),
                        date_max=datetime(2020, 1, 1),  entity='followers'):
        """
        Plot entity progress in time.
        :param date_min: Minimal date for data filtration
        :type date_min: date
        :param date_max: Maximal date for data filtration
        :param date_max: date
        :param usernames: Username of account to check progress.
        :type usernames: list of str
        :param entity: Chose one of entities (followers, engagement_rate, likes, comments). 'followers' by default.
        :type entity: str
        :return:
        """

        query = [{'username': name} for name in usernames]
        loc_df = pd.DataFrame(list(self.collection.find({'$and': [
            {
                'date': {
                    '$gte': date_min,
                    '$lte': date_max
                }
            },
            {
                '$or': query
            }
        ]})))
        print(loc_df)
        for username in usernames:
            plt.plot(loc_df[loc_df['username']==username]['date'], loc_df[loc_df['username']==username][entity]) 
        plt.show()


#d.compare_by_entity(['...', '...', '...'])
    def compare_by_entity(self, usernames):
        if isinstance(usernames, list):
            query = [{'username': name} for name in usernames]
            loc_df = pd.DataFrame(list(self.collection.aggregate(
                [
                    {
                        '$sort': {'date': 1}
                    },
                    {
                        '$match': {'$or': query}
                    },
                    {
                        '$group':
                            {
                                '_id': '$username',
                                'date': {'$last': '$date'},
                                'posts': {'$last': '$posts'},
                                'comments': {'$last': '$comments'},
                                'likes': {'$last': '$likes'}
                            }
                    },
                ]
            )))
            print(loc_df)
            plt.scatter(loc_df['posts'], loc_df['comments'], s=loc_df['likes'], c=np.random.rand(3, 3))
            for i in range(len(usernames)):
                plt.annotate(loc_df['_id'][i], xy=(loc_df['posts'][i], loc_df['comments'][i]))
            pylab.show()

        else:
            print('Usernames must be type of list')
