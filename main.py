from config import *
# from utils import read_html
from html_parser import parse_urls,data_from_html
   
from pprint import pprint
from db import *
import time
def main():
    st=time.time()
    # data=read_html(FILE_PATH)
    
    extracted_urls=parse_urls()
    con=make_connection()
    cursor=con.cursor()
    create_Tables(cursor,TABLE_NAME,DATA_TAB)
    insert_into_db(extracted_urls,cursor,con,TABLE_NAME)
   
    parsed_data=data_from_html()
    insert_into_db(parsed_data,cursor,con,DATA_TAB)
   
    con.commit()
    cursor.close()
    con.close()
    print(time.time()-st)
if __name__=="__main__":
    main()    


