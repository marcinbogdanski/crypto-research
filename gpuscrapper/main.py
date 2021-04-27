import os
from typing import List

from gpuscrapper.requestor import Requestor
from gpuscrapper.checker import Checker

class Scrapper:
    def __init__(self):
        self.requestor = Requestor()
        self.checker = Checker()

    def process_request(self, request_dict):
        supplier: str = request_dict['supplier']
        model: str = request_dict['model']

        listing_pages: List[str] = self.requestor.get_listing_pages(
            supplier=supplier, model=model)
        
        result = self.checker.check_listing_pages(request_dict, listing_pages)

        print('done')


if __name__ == '__main__':

    request = {
        'supplier': os.environ['SCRAPPER_SUPPLIER'],
        'model': os.environ['SCRAPPER_MODEL']
    }

    app = Scrapper()
    app.process_request(request)

