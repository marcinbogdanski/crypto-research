import os
from typing import Any, Dict, List

from gpuscrapper.requestor import Requestor
from gpuscrapper.checker import Checker
from gpuscrapper.database import Database

class Scrapper:
    def __init__(self, db_config: Dict[str, Any]):
        assert isinstance(db_config, dict)
        assert set(db_config.keys()) == {'hostname', 'username', 'password', 'database'}

        self.requestor = Requestor()
        self.checker = Checker()
        self.database = Database(
            hostname=db_config['hostname'],
            username=db_config['username'],
            password=db_config['password'],
            database=db_config['database']
        )

        print('bum')

    def process_request(self, request_dict):
        supplier: str = request_dict['supplier']
        model: str = request_dict['model']

        listing_pages: List[str] = self.requestor.get_listing_pages(
            supplier=supplier, model=model)
        
        result = self.checker.check_listing_pages(request_dict, listing_pages)

        print('done')


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
    app.process_request(request)

