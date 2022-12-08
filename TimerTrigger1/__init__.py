import logging
import datetime
import csv
import json
import sys
import time
import pandas as pd
import bs4
from bs4 import BeautifulSoup as BS

import azure.functions as func
import requests
from azure.data.tables import TableServiceClient
import KBO
sys.path.append('./')

def main(mytimer: func.TimerRequest, tablePath:func.Out[str]) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    tags1 = KBO.db() #한국시리즈
    #tags1 = KBO.sel() #정규시즌
    
    data1 = []

    for i,dt in enumerate(tags1) :
        data = { #원하는 정보만 들고오기 가능
            "선수명" : str(dt[1].replace(',','')),
            "AVG" : float(dt[3].replace(',','')),
            "H" : int(dt[7].replace(',','')),
            "HR" : int(dt[10].replace(',','')),
            "RBI" : int(dt[11].replace(',','')),
            "PartitionKey" : f"지역{i}",
            "RowKey": time.time()
        }
        data1.append(data)
    
    print(data1)
    tablePath.set(json.dumps(data1))

