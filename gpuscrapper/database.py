import pymongo

class Database:
    def __init__(self, hostname: str, username: str, password: str, database: str, port: int = 27017):
        assert isinstance(hostname, str)
        assert isinstance(username, str)
        assert isinstance(password, str)
        assert isinstance(database, str)
        assert isinstance(port, int) and port > 0

        import pdb; pdb.set_trace()
        
        url = f'mongodb://{username}:{password}@{hostname}:{port}/'
        self._client = pymongo.MongoClient(url, serverSelectionTimeoutMS = 2000)

        print('Testing MongoDB connection...')
        print('Server Info:', self._client.server_info())
        print('Databases:', self._client.list_database_names())
        self._db = self._client[database]
        print('Collections:', self._db.list_collection_names())
        collection = self._db['my-collection']
        print('First Document:', collection.find_one())


        print('hop')