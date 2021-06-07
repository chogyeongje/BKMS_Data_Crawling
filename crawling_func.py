from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, WebDriverException
from urllib.request import urlretrieve
from tqdm import tqdm
import time
import os
import zipfile
import numpy as np
from time import sleep    

from save_result import *
from install_driver import *
import random

count, a_count = 0, 0
result, a_result = [], []
max_scholar_count, max_author_count = 10000, 1000

def crawling_scholars(gf, author_name, author=True, scholar=True):

    global driver, result, count, a_result, a_count, max_scholar_count, max_author_count

    # print(author_name)

    if author:
        
        a_info = {}
        author_job = driver.find_element_by_xpath('//*[@id="gsc_prf_i"]/div[2]').text
        
        a_info['name'] = author_name
        a_info['job'] = author_job
        
        # xpath_citation_show_more = '/html/body/div/div[13]/div[2]/div/div[1]/div[1]/h3/button'
        # citation_show_more = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath_citation_show_more)))
        # citation_show_more.click()

        xpath_citation_chart = '/html/body/div/div[13]/div[2]/div/div[1]/div/div/div[3]/div' # '/html/body/div/div[4]/div/div[2]/div/div/div[3]/div'
        citation_chart = driver.find_element_by_xpath(xpath_citation_chart)
        years = citation_chart.find_elements_by_xpath("./span")
        numbers = citation_chart.find_elements_by_xpath('./a[@class="gsc_g_a"]')
        for year, num in zip(years, numbers):
            a_info[year.text] = num.find_element_by_xpath('./span').get_attribute("textContent")
    
        # xpath_close_chart = '/html/body/div/div[4]/div/div[1]/a'
        # close_chart = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath_close_chart)))
        # close_chart.click()

        # 초당 request 제한이 10개이기 때문에 sleep
        sleep(0.2)
        
        xpath_summary = '/html/body/div/div[13]/div[2]/div/div[1]/div[1]/table/tbody/tr'
        summary = driver.find_elements_by_xpath(xpath_summary)
        for s in summary:
            key = s.find_element_by_xpath('./td[@class="gsc_rsb_sc1"]/a').text
            value = s.find_elements_by_xpath('./td[@class="gsc_rsb_std"]')[0].text
            a_info[key] = value
        
        a_result.append(a_info)
        a_count += 1
        print(a_count)
        if a_count > max_author_count:
            raise MaxCrawlingError("The maximum number of authors that can be crawled has been reached.")
        elif a_count % gf.interval == 0:
            save_author(gf, a_result)
            a_result = []
    
    if scholar:
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
        xpath_popup_close = '/html/body/div/div[8]/div/div[1]/a'
        for scholar in scholars:
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
                row_value = row.find_element_by_xpath("./div[@class='gsc_vcd_value']").text
                if row_title == '전체 인용횟수':
                    row_value = row_value.split()[0]
                info[row_title] = row_value

            result.append(info)
            count += 1
            if count > max_scholar_count:
                raise MaxCrawlingError("The maximum number of scholars that can be crawled has been reached.")
            elif count % gf.interval == 0:
                save_result(gf, result)
                result = []

            popup_close = driver.find_element_by_xpath(xpath_popup_close)
            popup_close.click()
            
            # 초당 request 제한이 10개이기 때문에 sleep
            sleep(ramdon.random() + 1)

def driver_setup():
    
    global driver

    driveManager, options = install_driver()
    driver = webdriver.Chrome(driveManager, options=options)
    wait = WebDriverWait(driver, 10)
    print('driver setup done')

def crawling(gf, url, max_scholar = 10000, max_author = 1000, author=True, scholar=True):

    global driver, result, a_result, max_scholar_count, max_author_count
    max_scholar_count = max_scholar
    max_author_count = max_author

    driver_setup()

    print('접속중 >>> {}'.format(url))
    driver.get(url)
    driver.implicitly_wait(3)

    current_url = url
    page_count = 0

    global a_result, a_count

    while True:
        try:
            # if page_count % 10 == 0:
            #     current_url = driver.current_url
            #     driver.quit()
            #     print('접속중 >>> {}'.format(current_url))
            #     driver.get(url)
            #     driver.implicitly_wait(3)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") 
            
            wait = WebDriverWait(driver, 20)
            xpath_authors = "//div[@class='gs_ai gs_scl gs_ai_chpr']"
            
            authors = driver.find_elements_by_xpath(xpath_authors)
            print(current_url)
            
            # 현재 페이지를 main 으로 등록
            main_window = driver.current_window_handle
            for author in authors:
                    
                xpath_detail = "./div[@class='gs_ai_t']/h3[@class='gs_ai_name']/a"
                author_detail = author.find_element_by_xpath(xpath_detail)
                author_url = author_detail.get_attribute('href')
                author_name = author_detail.text
                
                # 확인
                a_info = {'name' : author_name, 'url' : author_url}
                a_result.append(a_info)
                a_count += 1
                if a_count > max_author_count:
                    raise MaxCrawlingError("The maximum number of authors that can be crawled has been reached.")
                elif a_count % gf.interval == 0:
                    save_author(gf, a_result)
                    a_result = []
                
                # # 새로운 tab 에 새로운 페이지 open
                # driver.execute_script(f'window.open("{author_url}","_blank");')
                # driver.implicitly_wait(3)
                # # 새로운 페이지로 이동
                # driver.switch_to.window(driver.window_handles[1])
                
                # # 논문 정보 
                # crawling_scholars(gf, author_name, author, scholar)
                
                # # 새로운 페이지 close
                # driver.close() 
                # # 다시 main 으로 이동
                # driver.switch_to.window(main_window)
                
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
        save_result(gf, result)
    if len(a_result) > 0:
        save_author(gf, a_result)

    print(author_name)

    driver.quit()

class MaxCrawlingError(Exception):
    def __init__(self, msg):
        super().__init__(msg)