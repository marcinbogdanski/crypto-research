import urllib.request
from typing import Any, Dict, List, Optional

_default_config = {
    'ebuyer': {
        'nvidia': [
            'https://www.ebuyer.com/store/Components/cat/Graphics-Cards-Nvidia'
        ],
        '3080': [
            'https://www.ebuyer.com/store/Components/cat/Graphics-Cards-Nvidia/subcat/GeForce-RTX-3080'
        ]
    }
}


class Requestor:
    def __init__(self, config: Optional[Dict[str,Any]] = None):
        assert config is None or isinstance(config, dict)
        
        self.config = config if config is not None else _default_config

    def get_listing_pages(self, supplier: str, model: str) -> List[str]:
        """Return one or more websites as strings"""
        url_list = self.config[supplier][model]

        contents_list = []
        for url in url_list:
            website_content = self._get_website_as_string(url)
            contents_list.append(website_content)
        
        return contents_list

    def _get_website_as_string(self, url: str) -> str:
        """Fetch URL and decode into Python string"""
        
        # Header is required so we don't get 403 error
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
        req = urllib.request.Request(url, headers=hdr)
        response = urllib.request.urlopen(req)
        content_raw = response.read()
        content = content_raw.decode()
        
        return content   # HTML with embedded script source code
