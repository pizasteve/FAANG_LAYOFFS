# importing all the necessary libaries
import os
#import csv
import time
import re
#import string
#import keyboard
import pandas as pd
from re import search
#from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains



profile_names=[]
profile_headlines=[]
profile_location=[]
company_name=[]
company_worktime=[]
work_months=[]
work_months_total=[]

# define your school name right here:
Company_name = "meta"

# defining the webdriver and config btw this code will be almost the same in all of your selenium scripts
options = Options()

# !!! blocking browser notifications !!!
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)

# starting in maximized window
options.add_argument("start-maximized")
options.add_argument("--disable-default-apps")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


driver.get("https://www.linkedin.com/login/")


username = "salmasamira2001@gmail.com"
password = "-7kx:gnJcSEkPQX"

username_field = driver.find_element(By.ID,"username")
username_field.send_keys(username)

password_field = driver.find_element(By.ID,"password")
password_field.send_keys(password)

password_field.submit()


count1 = 0
driver.get("https://www.linkedin.com/search/results/content/?authorJobTitle=%22Meta%22&keywords=%23metalayoffs&origin=FACETED_SEARCH&sid=D8.&sortBy=%22relevance%22")
time.sleep(3) 
items_urls = []
testing = []
while count1 < 10:
    try:
        profiles_links = driver.find_elements(By.XPATH, "//body/div[4]/div[3]/div[2]/div[1]/div[1]/main[1]/div[1]/div[1]/div[1]/div[1]/ul[1]/li/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/span[1]/span[1]/a[1]")

        #print(len(profiles_links))
        #print(profiles_links)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/.3);")
        time.sleep(3)
        for link in profiles_links: 
            print("hih")
            items_urls.append(link.get_attribute("href"))
            count1+=1
            if count1 ==10:
                break
    except Exception as e:
        print(e)            
print(items_urls)   


def scrap(url):
    
    # go to emloyee profile
    driver.get(url)

    # waiting for the profile to load
    time.sleep(1)


    # scraping the name of the layoff profile
    try:
        name = driver.find_element(By.XPATH, "/html[1]/body[1]/div[4]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/main[1]/section[1]/div[2]/div[2]/div[1]/div[1]/h1[1]").text
    except:              
        name = "none"
        print("makhdamch hadchi!")
    profile_names.append(name)
    time.sleep(1)
    # scraping the headline
    try:
        headline = driver.find_element(By.CLASS_NAME, "text-body-medium").text
    except:
        headline = "none"
    profile_headlines.append(headline)
    time.sleep(1)
    # scraping the location
    try:                                                                                              
        location = driver.find_element(By.XPATH, "//span[@class='text-body-small inline t-black--light break-words']").text
    except:
        location = "none"
    profile_location.append(location)
    time.sleep(1)
    # scraping the company
    try:    
        company = driver.find_element(By.XPATH, "//body/div[4]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/main[1]/section[5]/div[3]/ul[1]/li[1]/div[1]/div[2]/div[1]/div[1]/span[1]/span[1]").text
    except:
        try:
            company = driver.find_element(By.XPATH, "//body/div[4]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/main[1]/section[4]/div[3]/ul[1]/li[1]/div[1]/div[2]/div[1]/div[1]/span[1]/span[1]").text
        except:
            company = driver.find_element(By.XPATH, "//body/div[4]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/main[1]/section[3]/div[3]/ul[1]/li[1]/div[1]/div[2]/div[1]/div[1]/span[1]/span[1]").text
    company_name.append(company)
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/.1);")
    # scraping the company_worktime
    try:
        worktime = driver.find_element(By.XPATH, "/html[1]/body[1]/div[4]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/main[1]/section[3]/div[3]/ul[1]/li[1]/div[1]/div[2]/div[1]/div[1]/span[2]/span[1]").text                          
    except:
        try:
            worktime = driver.find_element(By.XPATH, "/html[1]/body[1]/div[4]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/main[1]/section[4]/div[3]/ul[1]/li[1]/div[1]/div[2]/div[1]/div[1]/span[2]/span[1]").text
        except:
            worktime = driver.find_element(By.XPATH, "/html[1]/body[1]/div[4]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/main[1]/section[5]/div[3]/ul[1]/li[1]/div[1]/div[2]/div[1]/div[1]/span[2]/span[1]").text
    str1='y'
    str2='m'
    worktime_nospaces=re.sub(r"\s+", "", worktime)
    if str1 in worktime_nospaces and isinstance(int(re.findall(r"(\d+)y", worktime_nospaces)[0]), int) and str2 in worktime_nospaces and isinstance(int(re.findall(r"(\d+)m", worktime_nospaces)[0]), int) :
        worktime_years=re.findall(r"(\d+)y", worktime_nospaces)
        worktime_monthsy=int(worktime_years[0])*12
        worktime_months=int(re.findall(r"(\d+)m", worktime_nospaces)[0])
        worktime_months_total=worktime_monthsy+worktime_months
        company_worktime.append(worktime_months_total)
    elif str2 in worktime_nospaces and isinstance(int(re.findall(r"(\d+)m", worktime_nospaces)[0]), int):
        worktime_months=int(re.findall(r"(\d+)m", worktime_nospaces)[0])
        company_worktime.append(worktime_months)
    elif str1 in worktime_nospaces and isinstance(int(re.findall(r"(\d+)y", worktime_nospaces)[0]), int):
        worktime_years=re.findall(r"(\d+)y", worktime_nospaces)
        worktime_monthsy=int(worktime_years[0])*12
        company_worktime.append(worktime_monthsy)
    time.sleep(1)
    # scraping the years of experience
    try:    
        experiences = driver.find_elements(By.XPATH, "//body/div[4]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/main[1]/section[4]/div[3]/ul[1]/li/div[1]/div[2]/div[1]/div[1]/span[2]/span[1]")
        print(experiences[0])
    except:
        try:
            experiences = driver.find_elements(By.XPATH, "//body/div[4]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/main[1]/section[3]/div[3]/ul[1]/li/div[1]/div[2]/div[1]/div[1]/span[2]/span[1]")
            print(experiences[0])
        except:
            experiences = driver.find_elements(By.XPATH, "//body/div[4]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/main[1]/section[5]/div[3]/ul[1]/li/div[1]/div[2]/div[1]/div[1]/span[2]/span[1]")
            print(experiences[0])

    for experience in experiences:
        print("this is experience: ", experience)
        if experience.text == "":
            pass
        else:
            years=experience.text
        str1='y'
        str2='m'
        experience_nospaces=re.sub(r"\s+", "", years)
        print(experience_nospaces)
        try:
            if str1 in experience_nospaces and isinstance(int(re.findall(r"(\d+)y", experience_nospaces)[0]), int) and str2 in experience_nospaces and isinstance(int(re.findall(r"(\d+)m", experience_nospaces)[0]), int) :
                experience_years=re.findall(r"(\d+)y", experience_nospaces)
                experience_monthsy=int(experience_years[0])*12
                experience_months=int(re.findall(r"(\d+)m", experience_nospaces)[0])
                experience_months_total=experience_monthsy+experience_months
                work_months.append(experience_months_total)
            elif str2 in experience_nospaces and isinstance(int(re.findall(r"(\d+)m", experience_nospaces)[0]), int):
                experience_months=int(re.findall(r"(\d+)m", experience_nospaces)[0])
                work_months.append(experience_months)
            elif str1 in experience_nospaces and isinstance(int(re.findall(r"(\d+)y", experience_nospaces)[0]), int):
                experience_years=re.findall(r"(\d+)y", experience_nospaces)
                experience_monthsy=int(experience_years[0])*12
                work_months.append(experience_monthsy)
        except:
            pass
    work_months_total.append(sum(work_months))
    
    time.sleep(1)

count_profiles=0
for item in items_urls:
    scrap(item)
    count_profiles=count_profiles+1
    if count_profiles==5:
        break


ids = [i for i in range(len(items_urls))]
df = pd.DataFrame(list(zip(profile_names, profile_headlines, profile_location, company_name, company_worktime,work_months_total)), columns =['Name', 'Headline', 'Location', 'Company', 'Company_Months', 'Work_Months'])

print(df) 
df.to_csv("FAANG.csv")