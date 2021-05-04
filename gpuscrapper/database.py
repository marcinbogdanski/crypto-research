import datetime as dt
import pymongo

class Database:
    def __init__(self, hostname: str, username: str, password: str, database: str, port: int = 27017):
        assert isinstance(hostname, str)
        assert isinstance(username, str)
        assert isinstance(password, str)
        assert isinstance(database, str)
        assert isinstance(port, int) and port > 0

        url = f'mongodb://{username}:{password}@{hostname}:{port}/'
        self._client = pymongo.MongoClient(url, serverSelectionTimeoutMS = 2000)

        print('Testing MongoDB connection...')
        print('Server Info:', self._client.server_info())
        print('Databases:', self._client.list_database_names())
        self._db = self._client[database]
        print('Collections:', self._db.list_collection_names())
        self._collection = self._db['gpu-scrapper']
        print('First Document:', self._collection.find_one())


        print('hop')
    
    def insert_one(self, request_dt, request_dict, result_dict):
        assert isinstance(request_dt, dt.datetime)
        assert isinstance(request_dict, dict)
        assert isinstance(result_dict, dict)

        document = {
            'metadata': {
                'request_datetime_utc': request_dt
            },
            'request': request_dict,
            'result': result_dict
        }
        inserted_id = self._collection.insert_one(document)
        return inserted_id
