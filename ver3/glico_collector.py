from selenium import webdriver
from bs4 import BeautifulSoup

import requests
import datetime


def team_id_collector():

    team_ids=[]
    driver=webdriver.Chrome()
    driver.get('https://www.datdota.com/teams/performances?default=true')

    all_pages_buttons = driver.find_element_by_id('DataTables_Table_0_paginate').find_elements_by_tag_name(
        'li')
    pages = int(all_pages_buttons[-2].get_attribute('innerText'))

    for table_page in range(pages):

        rows=driver.find_element_by_id('DataTables_Table_0').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
        for row in rows:
            team_ids.append(row.find_element_by_tag_name('a').get_attribute('href').split('/')[-1])


        all_pages_buttons = driver.find_element_by_id('DataTables_Table_0_paginate').find_elements_by_tag_name(
        'li')
        if table_page != pages:
            all_pages_buttons[-1].find_element_by_tag_name('a').click()
    return team_ids

def glico_collctor(team_id_list):
    glico_dict={}
    base_url='https://www.datdota.com/teams/'

    for id in team_id_list:

        html = requests.get(base_url+id).text
        soup = BeautifulSoup(html, 'lxml')

        glico2_row=soup.find('table',id='current-ratings').find_all('tr')[-1]
        rating=glico2_row.find_all('td')[2].text

        glico_dict[id]=rating
    return glico_dict
def create_glico_log(glico_dictinary):
    with open('glico_logs/'+str(datetime.date.today())+'.txt','w') as glico_log:
        for team_id in glico_dictinary:
            glico_log.write(team_id+':'+glico_dictinary[team_id]+'\n')

print('Collecting team ids')
team_id_list=team_id_collector()
print('collecting team\'s glico')
glico_dict=glico_collctor(team_id_list)
print('Creating glico log')
create_glico_log(glico_dict)


