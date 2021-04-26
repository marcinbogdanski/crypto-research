import os
from gpuscrapper.requestor import Requestor


class Scrapper:
    def __init__(self):

        
        
        self.requestor = Requestor()

    def process_request(self, request_description):
        supplier: str = request_description['supplier']
        model: str = request_description['model']
        content_list = self.requestor.get_websites(supplier=supplier, model=model)

        print('done')


if __name__ == '__main__':

    request_description = {
        'supplier': os.environ['SCRAPPER_SUPPLIER'],
        'model': os.environ['SCRAPPER_MODEL']
    }

    app = Scrapper()
    app.process_request(request_description)

