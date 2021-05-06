import datetime as dt
import pymongo

class DatabaseMongoDB:
    def __init__(self, hostname: str, username: str, password: str, database: str, collection: str, port: int = 27017):
        assert isinstance(hostname, str)
        assert isinstance(username, str)
        assert isinstance(password, str)
        assert isinstance(database, str)
        assert isinstance(collection, str)
        assert isinstance(port, int) and port > 0

        print('MongoDB: Creating client')
        url = f'mongodb://{username}:{password}@{hostname}:{port}/'
        self._client = pymongo.MongoClient(url, serverSelectionTimeoutMS = 2000)

        print('MongoDB: Server info:', self._client.server_info())
        print('MongoDB: Databases:', self._client.list_database_names())
        self._db = self._client[database]
        print('MongoDB: Collections:', self._db.list_collection_names())
        self._collection = self._db[collection]
        print('MongoDB: Example document:',
              str(self._collection.find_one())[:100])

    
    def insert_one(self, request_dt, request_dict, result_dict, listing_pages, error_report):
        assert isinstance(request_dt, dt.datetime)
        assert isinstance(request_dict, dict)
        assert result_dict is None or isinstance(result_dict, dict)
        assert listing_pages is None or isinstance(listing_pages, list)
        assert error_report is None or isinstance(error_report, dict)

        document = {
            'metadata': {
                'request_datetime_utc': request_dt,
                'listing_pages': listing_pages,
                'error_report': error_report
            },
            'request': request_dict,
            'result': result_dict
        }

        print(f'MongoDB: Inserting doc: {str(document)[:100]}')
        insertion_result = self._collection.insert_one(document)
        print(f'MongoDB: Insertion ok: {insertion_result.inserted_id}')
        return insertion_result.inserted_id  # str
