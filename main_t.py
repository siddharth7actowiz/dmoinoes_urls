from config import *
from utils import read_html
from html_parser import parse_urls, data_from_html
from db import *
import time
from concurrent.futures import ThreadPoolExecutor

def main():
    st = time.time()
   
    #DB Connetions
    con = make_connection()
    cursor = con.cursor()

    #  #urls table
    create_Tables(cursor, TABLE_NAME, DATA_TAB)

   #extracting urls and storing to db
    extracted_urls = parse_urls()
    insert_into_db(extracted_urls, cursor, con, TABLE_NAME)
    con.commit()

    # ectrating data from req 
    with ThreadPoolExecutor(max_workers=8) as tpe:
        future = tpe.submit(data_from_html)
        parsed_data = future.result()   

    insert_into_db(parsed_data, cursor, con, DATA_TAB)

    con.commit()
    cursor.close()
    con.close()
    print(f"Done in {time.time() - st:.2f}s — {len(parsed_data)} stores inserted")

if __name__ == "__main__":
    main()