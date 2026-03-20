from lxml import html ,etree
from validation import Store
from pydantic import ValidationError
from utils import read_json
import re
from pprint import pprint
from config import JSON_FILE_PATH
from db import make_connection
import requests
import sys
sys.stdout.reconfigure(encoding='utf-8')



headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://www.dominos.co.in/store-location/pune',
    'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
    # 'cookie': '_gcl_au=1.1.1121010527.1773899531; _gid=GA1.2.362445554.1773899533; _ga=GA1.1.1502612679.1773408617; _fbp=fb.1.1773899532647.25529123894767585; moe_uuid=005a9800-88e6-414a-9244-ee3bf6b15efa; _ga_51NSXH673Q=GS2.1.s1773899532$o1$g0$t1773899534$j58$l0$h0; _ga_CRJBK2R8LM=GS2.1.s1773899532$o1$g0$t1773899534$j58$l0$h0; _ga_KQE6QVSPD1=GS2.1.s1773899540$o2$g1$t1773899821$j34$l0$h0',
}


def parse_urls():

    urls = []
    res=requests.get("https://www.dominos.co.in/store-location/",headers=headers)

    tree = html.fromstring(res.text)

    base = "https://www.dominos.co.in"

    store_url = tree.xpath("//li//a[@class='citylink']")

    for url in store_url:

        city_name = url.xpath('string(./text())').split("(")[0].strip()
        city_name_clean = url.xpath('string(./@href)')

        dominos_restaurants = {}
        dominos_restaurants["Citiy_Name"] = city_name
        dominos_restaurants["City_URL"] = base + city_name_clean

        urls.append(dominos_restaurants)

    return urls


def fetch_urls():
    conn = make_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT City_URL FROM Dominos_Urls;")

    for row in cursor:
        yield row[0]   # one URL at a time

    cursor.close()
    conn.close()


#Helper to extract text safely
def clean_xpath(element, xp):
    res = element.xpath(xp)
    if isinstance(res, list):
        return " ".join([r.strip() for r in res if str(r).strip()])
    return str(res).strip()



def data_from_html():
  
    
    urls = fetch_urls()
    
    parsed_data = []
    xpaths = read_json(JSON_FILE_PATH)

    for url in urls:
        try:
            print(url)
            res = requests.get(url,headers=headers)
            tree = html.fromstring(res.text)
            city=url.rstrip('/').split('/')[-1]
            with open(f'D:\Siddharth\DOMINOS_URLS\html_pages\{city}.html.gz', "w", encoding="utf-8") as f:
                 f.write(res.text)
        except Exception as e:
            print("Request failed:", url, e)
            continue

        stores = tree.xpath(xpaths.get("stores"))

        for store in stores:
            temp_data = {}

            temp_data["Store_Name"] = clean_xpath(store, xpaths["Store_Name"])
            address = clean_xpath(store, xpaths["Address"])
            address = re.sub(r'\s+', ' ', address)
            temp_data["Address"] = address
            pincode = re.search(r'\b\d{6}\b', address)
            temp_data["Pincode"] = int(pincode.group()) if pincode else 0
            temp_data["Region"] = clean_xpath(store, xpaths["Region"])
            city_match = re.search(r'([A-Z]+)\s+\d{6}', address)
          
            temp_data["City"] = city_match.group(1).strip() if city_match else ""
          
            temp_data["ETA"] = clean_xpath(store, xpaths["ETA"])
            temp_data["Timing"] = clean_xpath(store, xpaths["Timing"])
            temp_data["Phone_Number"] = clean_xpath(store, xpaths["Phone_Number"])
            temp_data["Cost"] = clean_xpath(store, xpaths["Cost"])
            temp_data["Good_for"] = clean_xpath(store, xpaths["Good_for"])
            store_url = clean_xpath(store, xpaths["Store_Url"])
            temp_data["Store_Url"] = "https://www.dominos.co.in" + store_url if store_url else ""
            menu_url = store.xpath(xpaths["Menu_Url"])
            temp_data["Menu_Url"] = menu_url[0] if menu_url else ""

            parsed_data.append(temp_data)

            
            clean_data = []

            for i in parsed_data:
                try:
                    validated = Store(**i)
                    clean_data.append(validated.model_dump())
                except ValidationError as e:
                    print("Validation Error:", data_from_html.__name__, e)

    return parsed_data




