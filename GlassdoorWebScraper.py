import time
import pandas as pd
import numpy as np
from selenium import webdriver
import csv

unsuccessful_links = [] 
companies = {} 

roles = ['Data Scientist','Data Engineer','Business Analyst','Data Analyst','Business Intelligence Engineer']

driver = webdriver.Chrome(executable_path='C:/software/Drivers/chromedriver_win32/chromedriver.exe')

def get_link_attributes(links):
    return [link.get_attribute("href") for link in links]


def scraping_pages(num_pages, role):
    #Creating 'n' urls with url_roots to scrape
    url_root = f'https://www.glassdoor.com/Explore/browse-companies.htm?overall_rating_low=3&occ={role}&page='.replace(" ", "%20")
    nums = [x+1 for x in range(num_pages)]
    url_mains = list(map(lambda n: url_root + str(n), nums)) #adding 'n' number to call url_root 
    companies_list = []
    for url in url_mains:
        try:
            driver.get(url)
            time.sleep(5) #give page plenty of time to load (page 1 loads first, then specified 'n' page)
            
            elems = driver.find_elements('xpath','//div[@data-test = \'employer-card-single\']') #find links on an individual search page tagged with the 'a' tag
            reviews_href = get_link_attributes(driver.find_elements('xpath','//a[@data-test = \'cell-Reviews-url\']'))
            salaries_href = get_link_attributes(driver.find_elements('xpath','//a[@data-test = \'cell-Salaries-url\']'))
            jobs_href = get_link_attributes(driver.find_elements('xpath','//a[@data-test = \'cell-Jobs-url\']'))
            counter = 0
            for elem in elems:
                lst = elem.text.splitlines()
                # only include needed text
                companies_list.append([role] + [lst[i] for i in [0,1,3,5,7,10,12,14]] + [reviews_href[counter], salaries_href[counter], jobs_href[counter]])
                counter += 1


        except: #fail safe for inevitable errors
            unsuccessful_links.append(url) #adding unsuccessful urls to a list
            print('ERROR: ', url) #optional code to see list of urls that don't scrape properly
            time.sleep(5) #extra time here to let your internet catch up after an error
                
        print(f'Finished scraping {len(companies_list)} companies')                 
    return companies_list                            

for role in roles:
    num_p = 3
    companies[role] = scraping_pages(num_p,role)

# send to excel 
  
# field names 
fields = ['Role','Company', 'Ratings', 'Reviews', 'Salaries','Jobs', 'Office Locations','Global Company Size','Industry','Reviews Link','Salaries Link','Jobs Link'] 

with open('company_database.csv', 'w', newline='') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(fields)
    for role in roles:
        write.writerows(companies[role])
    f.close()