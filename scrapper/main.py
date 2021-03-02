# Python Imports
import os
import time
import urllib
import traceback
import datetime as dt

# Relative Imports
from .s3 import S3Wrapper







def get_website_as_string(url: str) -> str:
    
    # Header is required so we don't get 403 error
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    req = urllib.request.Request(url, headers=hdr)
    response = urllib.request.urlopen(req)
    content_bytes = response.read()
    content_str = content_bytes.decode()
    return content_str


def main():
    website_url = os.environ['WEBSITE_URL']  # http://vendor.com/link
    s3_url = os.environ['S3_URL']            # s3://bucket_name/folder_prefix
    
    s3_raw = s3_url.replace('s3://', '')
    s3_bucket = s3_raw.split('/')[0]
    s3_prefix = '/'.join(s3_raw.split('/')[1:])

    s3 = S3Wrapper()

    utcnow = dt.datetime.utcnow()
    previous_minute = utcnow.minute
    items_buffer = []

    while True:
        utcnow = dt.datetime.utcnow()
        
        item_dict = {
            'content': None,
            'datetime': utcnow.isoformat,
            'traceback': None,
        }
        try:
            item_dict['content'] = get_website_as_string(website_url)
        except:
            item_dict['traceback'] = traceback.format_exc()
        items_buffer.append(item_dict)
        
        # check if we crossed minute boundry
        if previous_minute != utcnow.minute:
            previous_minute = utcnow.minute

            s3_key = os.path.join(s3_prefix, utcnow.strftime('%Y-%m-%d_%H-%M-%S.pkl.gzip'))
            s3.put_object_pickled_gzip(
                s3_bucket=s3_bucket,
                s3_key=s3_key,
                obj=items_buffer
            )
            items_buffer = []
            print('Saved:', os.path.join('s3://', s3_bucket, s3_key))        

        time.sleep(1)
            


if __name__ == '__main__':
    main()
