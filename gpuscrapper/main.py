import os
import time
import datetime as dt
from typing import Any, Dict, List

from gpuscrapper.requestor import Requestor
from gpuscrapper.checker import Checker
from gpuscrapper.database import DatabaseMongoDB

class Scrapper:
    def __init__(self, db_config: Dict[str, Any]):
        assert isinstance(db_config, dict)
        assert set(db_config.keys()) == {'hostname', 'username', 'password', 'database'}

        print('Scrapper: Initializing Requestor')
        self.requestor = Requestor()
        print('Scrapper: Initializing Checker')
        self.checker = Checker()
        print('Scrapper: Initializing Database')
        self.database = DatabaseMongoDB(
            hostname=db_config['hostname'],
            username=db_config['username'],
            password=db_config['password'],
            database=db_config['database']
        )
        print('Scrapper: Initialization completed')


    def process_request(self, request_dict):
        
        print(f'Scrapper: Processing request: {str(request_dict)[:100]}')

        # Record request timestamp
        request_dt = dt.datetime.utcnow()

        # Perform the request
        listing_pages: List[str] = self.requestor.get_listing_pages(
            supplier=request_dict['supplier'],
            model=request_dict['model'])
        print(f'Scrapper: Request completed: {str(listing_pages)[:100]}')
        
        # Process the result
        result_dict = self.checker.check_listing_pages(request_dict, listing_pages)
        print(f'Scrapper: Processing completed: {str(result_dict)[:100]}')

        inserted_id = self.database.insert_one(
            request_dt=request_dt,
            request_dict=request_dict,
            result_dict=result_dict
        )
        print(f'Scrapper: Insertion completed: {inserted_id}')


if __name__ == '__main__':

    db_config = {
        'hostname': os.environ['MONGODB_HOSTNAME'],
        'username': os.environ['MONGODB_USERNAME'],
        'password': os.environ['MONGODB_PASSWORD'],   
        'database': os.environ['MONGODB_DATABASE'],
    }

    request = {
        'supplier': os.environ['SCRAPPER_SUPPLIER'],
        'model': os.environ['SCRAPPER_MODEL']
    }

    app = Scrapper(db_config=db_config)
    while True:
        app.process_request(request)
        time.sleep(5)
    

