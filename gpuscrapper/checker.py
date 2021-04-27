import datetime as dt
from typing import Any, Dict, List, Optional, Tuple

from gpuscrapper.subcheckers.subchecker_ebuyer import SubcheckerEBuyer

class Checker:
    def __init__(self):
        pass

    def check_listing_pages(self,
        request_dict: Dict[str, Optional[str]],
        listing_pages: List[str]) -> Dict[str, Any]:

        assert isinstance(request_dict, dict)
        assert request_dict.keys() == {'model', 'supplier'}
        assert all(isinstance(k, str) for k in request_dict.keys())
        assert all(isinstance(v, str) for v in request_dict.values())

        model = request_dict['model']
        assert model in {'nvidia', '3060ti', '3070'}
        
        supplier = request_dict['supplier']
        assert supplier in {'ebuyer'}
        

        plp_summaries: List[List[Dict[str, Any]]] = []
        for plp in listing_pages:
            if supplier == 'ebuyer':
                plp_summary = \
                    SubcheckerEBuyer.check_product_listing_page(plp)
                plp_summaries.append(plp_summary)
        
        print('hop')

        total_products_found_all_pages = \
            sum(s['num_products_found_on_page'] for s in plp_summaries)
        total_products_available_all_pages = \
            sum(s['num_products_available_on_page'] for s in plp_summaries)
        
        return {
            '_type': 'request_result',
            'products_found': total_products_found_all_pages,
            'products_available': total_products_available_all_pages,
            'product_listing_page_sumaries': plp_summaries
        }