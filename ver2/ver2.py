from selenium import webdriver
from selenium.webdriver.common.by import By

class GrafMaker:
    def __init__(self,team_url):
        self.driver=webdriver.Chrome()
        self.team_url=team_url
        self.heroes_dic=self.set_heroes_dic()
        self.heroes_rels=self.set_heroes_rels()
        self.graf_site_url='https://graphonline.ru/'

    def fill_heroes_rel_with_data(self):
        self.driver.get(self.team_url)
        all_pages_buttons=self.driver.find_element(By.ID ,'DataTables_Table_0_paginate').find_elements(By.TAG_NAME ,'li')
        pages=int(all_pages_buttons[-2].get_attribute('innerText'))

        for table_page in range(pages):
            rows = self.driver.find_element(By.ID ,
                    'DataTables_Table_0').find_element(By.TAG_NAME ,'tbody').find_elements(By.TAG_NAME ,'tr')
            for row in rows:
                columns=row.find_elements(By.TAG_NAME ,'td')
                match_number=columns[0]
                match_result='Win' if columns[-1].get_attribute("innerText")=='Team A' else 'Lose'
                picked_heroes=columns[7].find_elements(By.TAG_NAME ,'img')

                for hero in picked_heroes:
                    for other_hero in picked_heroes:
                        if other_hero == hero:
                            continue
                        hero_index = self.heroes_dic[hero.get_attribute('title')][0]
                        other_hero_index = self.heroes_dic[other_hero.get_attribute('title')][0]
                        self.heroes_rels[hero_index][other_hero_index][match_result != 'Win'] += 1
                    self.heroes_dic[hero.get_attribute('title')][1][match_result != 'Win'] += 1
            all_pages_buttons = self.driver.find_element(By.ID ,'DataTables_Table_0_paginate').find_elements(By.TAG_NAME,
                'li')
            if table_page!=pages:
                all_pages_buttons[-1].find_element(By.TAG_NAME, 'a').click()

    def set_heroes_dic(self):
        dic={}
        id=0
        with open('all_heroes.txt', 'r') as heroes:
            for hero in heroes.readlines():
                dic[hero.strip()] = (id, [0, 0])
                id += 1
            return dic

    def set_heroes_rels(self):
        hero_rels=[]
        for i in range(len(self.heroes_dic)):
            blank = [[0, 0] for x in range(len(self.heroes_dic))]
            hero_rels.append(blank)
        return hero_rels

    def graf_create_new(self,driver):
        driver.find_element(By.CSS_SELECTOR ,'.btn.btn-default.btn-sm.dropdown-toggle').click()
        driver.find_element(By.ID, 'NewGraph').click()

    def graf_save(self,driver):
        driver.find_element(By.CSS_SELECTOR ,'.btn.btn-default.btn-sm.dropdown-toggle').click()
        driver.find_element(By.ID ,'SaveGraph').click()
        graf_url=driver.find_element(By.ID,'GraphName').get_attribute('value')
        print(graf_url)

    def heroes_rel_to_str(self):
        heroes_rel_str=''
        print('hero_rel_to_str_start')
        for i in self.heroes_rels:
            for j in i:
                heroes_rel_str+=(str(j[0]) + '.' + str(j[1])+',')
            heroes_rel_str+='\n'
        print('done')
        return heroes_rel_str

    def graf_input_heroes_rels(self,driver):
        driver.find_element(By.CSS_SELECTOR, '.btn.btn-default.btn-sm.dropdown-toggle').click()
        driver.find_element(By.ID,'ShowAdjacencyMatrix').click()
        #matrix_input_box=driver.find_element_by_css_selector('ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-front.EdgeDialog.ui-dialog-buttons.ui-draggable')
        print('found box')
        driver.find_element(By.NAME , 'adjacencyMatrixField').send_keys(self.heroes_rel_to_str())
        print('input_done')

    def heroes_dic_to_str(self):
        heroes_dic_str=''
        for i in self.heroes_dic:
            win, lose = self.heroes_dic[i][1][0], self.heroes_dic[i][1][1]
            times_played = win + lose
            if times_played == 0:
                win_rate = 'None'
            elif win == 0:
                win_rate = 0
            else:
                win_rate = round(win / times_played, 4)
            heroes_dic_str+=('{} {}({}%)\n'.format(i, times_played, win_rate * 100 if win_rate != 'None' else 'None'))
        return heroes_dic_str


    def graf_change_names(self, driver):
        driver.find_element(By.CSS_SELECTOR, '.btn.btn-default.btn-sm.dropdown-toggle').click()
        driver.find_element(By.ID, 'GroupRename').click()
        driver.find_element(By.ID,'VertextTitleList').send_keys(self.heroes_dic_to_str())
        save_and_cancel_butt=driver.find_element(By.CLASS_NAME, 'ui-dialog-buttonset').find_element(By.TAG_NAME, 'button')
        save_and_cancel_butt[0].click()

    def graf_make(self):
        self.driver.get(self.graf_site_url)
        '''
        self.driver.get(self.graf_site_url)
        self.graf_create_new(self.driver)
        #self.graf_input_heroes_rels(self.driver)
        self.graf_change_names(self.driver)
        self.graf_save(self.driver)
        '''

    def wight_vision_on(self):
        algorithms=self.driver.find_element(By.ID, 'openAlgorithmList')
        algorithms.click()
        algorithms.find_element(By.ID, "OlegSh.ModernGraphStyle").click()







'''
url='https://www.datdota.com/matchfinder/classic?team-a=36&patch=7.28&after=01%2F01%2F2020&before=18%2F01%2F2021&duration=0%3B200&duration-value-from=0&duration-value-to=200&valve-event=does-not-matter&threshold=1#'#input('Enter URL: ')
test=GrafMaker(url)
test.fill_heroes_rel_with_data()
#print(test.heroes_rel_to_str())
#print(test.heroes_dic_to_str())

test.graf_make()

driver=webdriver.Chrome()
driver.get(url)
table=driver.find_elements_by_class_name('table table-striped table-bordered table-hover data-table dataTable no-footer dtr-inline collapsed')
'''

