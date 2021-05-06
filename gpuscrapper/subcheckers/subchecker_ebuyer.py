from typing import Any, Dict, List, Optional, Tuple

import bs4
from bs4 import BeautifulSoup

class SubcheckerEBuyer:
    
    @staticmethod
    def _check_title_and_link(product_tag: bs4.element.Tag) -> Tuple[str, str]:
        assert isinstance(product_tag, bs4.element.Tag)
        link_a = product_tag.select_one('h3.grid-item__title > a')
        # print(link_a)

        title = link_a.text.strip()
        # print(title)

        link_a_href = link_a['href']
        full_link = 'https://www.ebuyer.com' + link_a_href
        # print(full_link)
        return title, full_link
    
    @staticmethod
    def _check_available(product_tag: bs4.element.Tag) -> bool:
        assert isinstance(product_tag, bs4.element.Tag)

        button_basket = product_tag.select_one('div.grid-item__buttons > button.button--mini-basket')

        if button_basket is not None:
            button_text = button_basket.text.strip().lower()
            if button_text == 'add to basket':
                return True   # check succeded, product is available
            else:
                return False
        else:
            return False  # check failed
    
    @staticmethod
    def _check_not_available(product_tag: bs4.element.Tag) -> bool:
        assert isinstance(product_tag, bs4.element.Tag)

        p_coming_soon = product_tag.select_one('p.grid-item__coming-soon')
        if p_coming_soon is not None:
            assert p_coming_soon.text.strip().lower() in {'coming soon'}
            return True   # check succeded, product IS NOT available!
        else:
            return False  # check failed

    @staticmethod
    def _check_product(product_tag: bs4.element.Tag) -> List[Dict[str, str]]:
        assert isinstance(product_tag, bs4.element.Tag)
        
        title, link = SubcheckerEBuyer._check_title_and_link(product_tag)
        is_available = SubcheckerEBuyer._check_available(product_tag)
        is_not_available = SubcheckerEBuyer._check_not_available(product_tag)

        is_valid = (is_available or is_not_available) and \
                     not (is_available and is_not_available)
        
        if not is_valid:
            is_available = None
        
        return {
            'title': title,
            'link': link,
            'is_valid': is_valid,
            'available': is_available,
        }
    
    @staticmethod
    def check_product_listing_page(content_html: str) -> List[Dict[str, Any]]:
        assert isinstance(content_html, str)
        
        soup = bs4.BeautifulSoup(content_html)
        product_list = soup.select('div.grid-item')
        
        products_list = []
        for product_tag in product_list:
            product_dict = SubcheckerEBuyer._check_product(product_tag)
            products_list.append(product_dict)
        
        num_found = len(products_list)
        num_valid = sum(p['is_valid'] == True for p in products_list)
        num_invalid = sum(p['is_valid'] == False for p in products_list)
        num_available = sum(p['available'] == True for p in products_list)
        
        # Product Listing Page Summary
        plp_summary = {
            'num_products_found_on_page': num_found,
            'num_products_available_on_page': num_available,
            'num_products_valid_on_page': num_valid,
            'num_products_invalid_on_page': num_invalid,
            'product_summaries': products_list
        }
        
        return plp_summary
