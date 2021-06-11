from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, WebDriverException
from urllib.request import urlretrieve
from urllib import parse
from urllib.parse import urlparse
from urllib.parse import parse_qs
from tqdm import tqdm
import time
import os
import zipfile
import numpy as np
from time import sleep    

from save_result import *
from install_driver import *
import random

from bs4 import BeautifulSoup
import requests
import requests.exceptions
import glob
import ast

count, a_count = 0, 0
result, a_result = [], []
max_scholar_count, max_author_count = 10000, 1000

def driver_setup():
    
    global driver

    driveManager, options = install_driver()
    driver = webdriver.Chrome(driveManager, options=options)
    wait = WebDriverWait(driver, 10)
    print('driver setup done')

def crawling_authors(gf, file_path, max_count):

    global driver, result, count

    if file_path.endswith('.csv'):
        file_list = [file_path]
    else:
        file_list = list(glob.glob(file_path +  "/*.csv"))
        file_list = sorted(file_list, key=lambda x: int(x.split('/')[-1].split('_')[0]))
    
    for path in file_list:
        df = pd.read_csv(path)
        for url in df['url']:

            while True:
                try:
                    response = requests.get(url)
                    soup = BeautifulSoup(response.text, 'html.parser')

                    info = {}
                    name = soup.select_one('#gsc_prf_in')
                    info['name'] = name.get_text()
                    job = soup.select_one('#gsc_prf_i > div:nth-child(2)')
                    info['job'] = job.get_text()

                    keywords = soup.select('#gsc_prf_int > a')
                    keyword = []
                    for kw in keywords:
                        keyword.append(kw.get_text())        
                    info['keywords'] = ','.join(keyword)

                    rows = soup.select('#gsc_rsb_cit > div > div.gsc_md_hist_w > div > span')
                    values = soup.select('#gsc_rsb_cit > div > div.gsc_md_hist_w > div > a > span')
                    for row, value in zip(rows, values):
                        info[row.get_text()] = value.get_text()

                    cols = soup.select('#gsc_rsb_st > tbody > tr > td.gsc_rsb_sc1')
                    values = soup.select('#gsc_rsb_st > tbody > tr > td:nth-child(2)')
                    for col, value in zip(cols, values):
                        info[col.get_text()] = value.get_text()

                    result.append(info)
                    count += 1
                    print(info['name'], count)

                    if count > max_count:
                        raise MaxCrawlingError("The maximum number of authors that can be crawled has been reached.")
                    elif count % gf.interval == 0:
                        save_authors(gf, result)
                        result = []
                    break
                except:
                    driver.delete_all_cookies()

            sleep(random.random() + 1)

def crawling_author_links(gf, url, max_count):

    global driver, result, count

    driver_setup()

    print('접속중 >>> {}'.format(url))
    driver.get(url)
    driver.implicitly_wait(3)

    while True:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            wait = WebDriverWait(driver, 20)
            xpath_authors = "//div[@class='gs_ai gs_scl gs_ai_chpr']"
            
            authors = driver.find_elements_by_xpath(xpath_authors)
            
            for author in authors:        
                xpath_detail = "./div[@class='gs_ai_t']/h3[@class='gs_ai_name']/a"
                author_detail = author.find_element_by_xpath(xpath_detail)
                author_url = author_detail.get_attribute('href')
                author_name = author_detail.text
            
                info = {'name' : author_name, 'url' : author_url}
                result.append(info)
                count += 1
                if count > max_count:
                    raise MaxCrawlingError("The maximum number of authors that can be crawled has been reached.")
                elif count % gf.interval == 0:
                    save_author_links(gf, result)
                    result = []
            
            xpath_next = '//*[@id="gsc_authors_bottom_pag"]/div/button[2]'
            elem_next = driver.find_element_by_xpath(xpath_next)  
            elem_next.click()
            
        except (TimeoutException, WebDriverException) as e:
            print("Last page reached. Error: {}".format(e))
            break
        except MaxCrawlingError as e:
            print(e)
            break

    if len(result) > 0:
        save_author_links(gf, result)

    driver.quit()

def crawling_scholar_links(gf, url, max_count):

    global driver, result, count

    driver_setup()

    print('접속중 >>> {}'.format(url))
    driver.get(url)
    driver.implicitly_wait(3)

    while True:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") 
            
            wait = WebDriverWait(driver, 20)
            xpath_authors = "//div[@class='gs_ai gs_scl gs_ai_chpr']"
            
            authors = driver.find_elements_by_xpath(xpath_authors)
            
            # 현재 페이지를 main 으로 등록
            main_window = driver.current_window_handle
            for author in authors:
                    
                xpath_detail = "./div[@class='gs_ai_t']/h3[@class='gs_ai_name']/a"
                author_detail = author.find_element_by_xpath(xpath_detail)
                author_url = author_detail.get_attribute('href')
                author_name = author_detail.text
                
                # 새로운 tab 에 새로운 페이지 open
                driver.execute_script(f'window.open("{author_url}","_blank");')
                driver.implicitly_wait(3)
                # 새로운 페이지로 이동
                driver.switch_to.window(driver.window_handles[1])
                
                # 논문 정보 
                _crawling_scholar_links_detail(gf, max_count)
                
                # 새로운 페이지 close
                driver.close() 
                # 다시 main 으로 이동
                driver.switch_to.window(main_window)
                
            xpath_next = '//*[@id="gsc_authors_bottom_pag"]/div/button[2]'
            elem_next = driver.find_element_by_xpath(xpath_next)  
            elem_next.click()
        except (TimeoutException, WebDriverException) as e:
            print("Last page reached. Error: {}".format(e))
            break
        except MaxCrawlingError as e:
            print(e)
            break
    driver.quit()

def _crawling_scholar_links_detail(gf, max_count):

    global driver, result, count

    base_url = driver.current_url

    # 모든 논문 리스트 불러오기
    xpath_show_more = '//*[@id="gsc_bpf_more"]'
    while True:
        try:
            show_more = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath_show_more)))
            show_more.click()
        except:
            print('Last page reached')
            break
    
    # 논문 선택
    xpath_scholars = "//tr[@class='gsc_a_tr']"
    scholars = driver.find_elements_by_xpath(xpath_scholars)
    
    # 각 논문마다 정보 들고오기
    for scholar in scholars:
        xpath_detail = "./td[@class='gsc_a_t']/a"
        scholar_click = scholar.find_element_by_xpath(xpath_detail)

        info = {}
        title = scholar_click.text
        link = base_url + '#d=gs_md_cita-d&u=' + parse.quote(scholar_click.get_attribute('data-href')) \
                + '%26tzom%3D-540'
        info = {'title': title, 'link': link}

        result.append(info)
        count += 1

        if count > max_count:
            raise MaxCrawlingError("The maximum number of authors that can be crawled has been reached.")
        elif count % gf.interval == 0:
            save_scholar_links(gf, result)
            result = []

def check_scholars_count(gf, file_path):
    global driver, result, count

    driver_setup()

    author_count = 0

    file_list = list(glob.glob(file_path +  "/*.csv"))
    file_list = sorted(file_list, key=lambda x: int(x.split('/')[-1].split('_')[0]))

    total = 0

    for path in file_list:
        print(path)

        df = pd.read_csv(path)
        for url in df['url']:
            author_count += 1

            print('접속중 >>> {}'.format(url))
            driver.get(url)
            driver.implicitly_wait(3)
            
            # 모든 논문 리스트 불러오기
            xpath_show_more = '//*[@id="gsc_bpf_more"]'
            while True:
                try:
                    show_more = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath_show_more)))
                    show_more.click()
                except:
                    print('Last page reached')
                    break
            
            # 논문 선택
            xpath_scholars = "//tr[@class='gsc_a_tr']"
            scholars = driver.find_elements_by_xpath(xpath_scholars)

            if len(scholars) < 1:
                print('delete all cookies')
                driver.delete_all_cookies()
                continue
        
            total += len(scholars)
            print(total)
            sleep(random.randint(2, 12))

    print('all scholars : ', total)

def crawling_scholars_by_author(gf, file_path, start, max_author_count):

    global driver, result, count

    driver_setup()

    author_count = 0

    if file_path.endswith('.csv'):
        file_list = [file_path]
    else:
        file_list = list(glob.glob(file_path +  "/*.csv"))
        file_list = sorted(file_list, key=lambda x: int(x.split('/')[-1].split('_')[0]))

    asd = author_scholar_dict()

    for path in file_list:
        print(path)

        df = pd.read_csv(path)
        for name, url in zip(df['name'], df['url']):
            author_count += 1

            if name in asd:
                if gf.start + asd[name] < start:
                    gf.start += asd[name]
                    print(f'{author_count}-th author, total scholars : {gf.start}')
                    continue

            print('접속중 >>> {}'.format(url))
            driver.get(url)
            driver.implicitly_wait(3)
            
            # 모든 논문 리스트 불러오기
            xpath_show_more = '//*[@id="gsc_bpf_more"]'
            while True:
                try:
                    show_more = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath_show_more)))
                    show_more.click()
                except:
                    print('Last page reached')
                    break
            
            # 논문 선택
            xpath_scholars = "//tr[@class='gsc_a_tr']"
            scholars = driver.find_elements_by_xpath(xpath_scholars)

            if len(scholars) < 1:
                print('There is Some Problem, Please Retry')
                return

            asd[name] = len(scholars)
            save_author_scholar_dict(asd)


            # 각 논문마다 정보 들고오기
            xpath_popup_close = '/html/body/div/div[8]/div/div[1]/a'
            for scholar in scholars:

                if gf.start < start:
                    gf.start += 1
                    continue

                while True:
                    try:
                        xpath_detail = "./td[@class='gsc_a_t']/a"
                        scholar_click = scholar.find_element_by_xpath(xpath_detail)

                        info = {}
                        title = scholar_click.text
                        info['제목'] = title

                        scholar_click.click()

                        xpath_popup_view = "/html/body/div/div[8]/div/div[2]/div/div/div[2]/form"
                        popup_view = driver.find_element_by_xpath(xpath_popup_view)

                        popup_table = popup_view.find_elements_by_xpath("./div[@id='gsc_vcd_table']/div[@class='gs_scl']")
                        for row in popup_table:
                            row_title = row.find_element_by_xpath("./div[@class='gsc_vcd_field']").text
                            if row_title == '전체 인용횟수':
                                citation_count = row.find_element_by_xpath("./div[@class='gsc_vcd_value']/div[1]/a").text
                                info[title] = citation_count
                                graph_x = row.find_elements_by_xpath('//*[@id="gsc_vcd_graph_bars"]/span')
                                graph_y = row.find_elements_by_xpath('//*[@id="gsc_vcd_graph_bars"]/a/span')
                                for x, y in zip(graph_x, graph_y):
                                    info[x.text] = y.get_attribute('textContent')
                            else:
                                row_value = row.find_element_by_xpath("./div[@class='gsc_vcd_value']").text
                                info[row_title] = row_value

                        result.append(info)
                        count += 1
                        # print(count)
                        if count % gf.interval == 0:
                            save_scholars(gf, result)
                            result = []

                        popup_close = driver.find_element_by_xpath(xpath_popup_close)
                        popup_close.click()
                        
                        print(title, count)

                        # 초당 request 제한이 10개이기 때문에 sleep
                        sleep(random.random() + 1)
                        break
                    except Exception as e:
                        print(f'some exception found when crawling {count}')
                        print(e)
                        driver.delete_all_cookies()
                        popup_close = driver.find_element_by_xpath(xpath_popup_close)
                        popup_close.click()
            
            print(f'{author_count}-th author, total scholars : {gf.start}')

            if author_count > max_author_count:
                raise MaxCrawlingError("The maximum number of scholars that can be crawled has been reached.")


def author_scholar_dict():

    if not os.path.exists('./author_scholar_dict.txt'):
        return dict()

    with open('./author_scholar_dict.txt', 'r') as f:
        asd = f.readline()
        asd = ast.literal_eval(asd)

    asd = dict() if asd is None else asd
    return asd

def save_author_scholar_dict(asd):
    with open('./author_scholar_dict.txt', 'w') as f:
        f.write(str(asd))


class MaxCrawlingError(Exception):
    def __init__(self, msg):
        super().__init__(msg)