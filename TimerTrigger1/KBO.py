import time
import pandas as pd
import bs4
import csv
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import time

def sel():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches",["enable-logging"])
    url = "https://www.koreabaseball.com/Record/Player/HitterBasic/Basic1.aspx?sort=HRA_RT"
    driver = webdriver.Chrome(executable_path='\chromderiver.exe') #크롬열기
    driver.get(url) #url접속
    driver.find_element("xpath",'//*[@id="cphContents_cphContents_cphContents_ddlSeries_ddlSeries"]/option[1]').click()
    time.sleep(1)
    driver.find_element("xpath",'').click()
    time.sleep(1)

    filename = "baseball.csv"
    f = open(filename,"w",encoding="utf_8_sig",newline="")
    w = csv.writer(f)

    p_data = []
    titel_data = driver.find_element("xpath",'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/thead/tr')
    base_data = driver.find_element("xpath",'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody')
    for i in titel_data:
        columns = i.find_element("xpath",'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/thead/tr/th[%d]'%(i))
        if len(columns)<=1:
            continue
        d_data = [column.get_text().strip() for column in columns]
        p_data.append(d_data)
        w.writerow(d_data)

    p_data = []    
    for j in base_data:
        columns = i.find_element("xpath",'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr/th[%d]'%j)
        if len(columns)<=1:
            continue
        d_data = [column.get_text().strip() for column in columns]
        p_data.append(d_data)
        w.writerow(d_data)
    driver.back()
    return p_data

def db():
    url = "https://www.koreabaseball.com/Record/Player/HitterBasic/BasicOld.aspx?sort=HRA_RT"
    res = requests.get(url)
    res.raise_for_status() #요청/응답 코드가 200이 아니면 예외 발생

    soup = BS(res.text,"lxml")
    
    filename = "base_ball.csv"
    f = open(filename, "w", encoding="utf_8_sig",newline= "")
    writer = csv.writer(f)
    
    bb_data = []
    try:
        ball_data = soup.find("table",attrs={"class" :"tData01 tt"}).find("tbody").find_all("tr")
        for data in ball_data:
            columns = data.find_all("td")
            if len(columns) <= 1 :
                    continue
            d_data = [column.get_text().strip() for column in columns]
            bb_data.append(d_data)
            writer.writerow(d_data)
    except IndexError : 
        pass
    return bb_data