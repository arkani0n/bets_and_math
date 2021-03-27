from selenium import webdriver
from datetime import date

class DictBuilder:


    def __init__(self,team_name):
        self.search_page='https://www.datdota.com/matchfinder/classic?default=true'
        self.driver=webdriver.Chrome()
        self.driver.get(self.search_page)
        self.heroes_stats=self.prepare_hero_dict()
        self.glico_dict=self.fill_glico_dict()
        self.team_glico=None
        self.team_name=team_name
        self.heroes_for_analyze=[]
        self.heroes_power = 0
        self.connection_power = 0
        self.start_value_hero_power=0
        self.start_value_connections_power = 0
        self.matches_analyzed=0

    def get_matches_analyzed(self):
        return self.matches_analyzed

    def manual_search_preparation(self,url,id):
        self.driver.get(url)
        self.team_id=id
        self.team_glico=float(self.glico_dict[self.team_id])



    def choose_date(self,date):
        date='{}/{}/{}'.format(date[0],date[1],date[2])

        date_input_field=self.driver.find_element_by_id('before')
        date_input_field.clear()
        date_input_field.send_keys(date)



    def print_an(self):
        print(self.heroes_for_analyze)

    def reset_hero_and_connections_powers(self):
        self.heroes_power=self.start_value_hero_power
        self.connection_power=self.start_value_connections_power

    def analyze(self):
        self.reset_hero_and_connections_powers()
        counted_heroes=[]

        for hero_name in self.heroes_for_analyze:
            for match_id in self.heroes_stats[hero_name]:
                match=self.heroes_stats[hero_name][match_id]

                self.heroes_power+=match[0]

                for other_hero_in_match in match[1]:
                    if other_hero_in_match in self.heroes_for_analyze and other_hero_in_match not in counted_heroes:
                        self.connection_power+=match[0]
            counted_heroes.append(hero_name)

    def fill_glico_dict(self):
        dict={}

        with open('glico_logs/'+str(date.today())+'.txt','r') as glico_log:
            for row in glico_log.readlines():
                row=row.strip().split(':')
                dict[row[0]]=row[1]
            return dict

    def prepare_hero_dict(self):
        dic = {}
        with open('all_heroes.txt', 'r') as heroes:
            for hero in heroes.readlines():
                hero=hero.strip()
                dic[hero]={}
            return dic

    def get_team_glico_and_id(self,id):
        self.team_id=id
        self.team_glico=float(self.glico_dict[self.team_id])

    def find_all_matches(self):
        try:
            if self.driver.find_element_by_class_name('select2-selection__choice__remove'):
                self.driver.find_element_by_class_name('select2-selection__choice__remove').click()
        except:
            pass

        self.driver.find_element_by_class_name('select2-search__field').send_keys(self.team_name)
        search_opionts = self.driver.find_element_by_id('select2-team-a-results')
        search_opionts = search_opionts.find_elements_by_tag_name('li')
        while len(search_opionts)<2:
            search_opionts = self.driver.find_element_by_id('select2-team-a-results')
            search_opionts = search_opionts.find_elements_by_tag_name('li')

        raw_team_id=search_opionts[0].find_element_by_tag_name('span').get_attribute('innerText')
        self.team_id=raw_team_id.split(': ')[1].replace(')','')
        self.team_glico=float(self.glico_dict[self.team_id])

        search_opionts[0].click()

        for button in self.driver.find_elements_by_tag_name('button'):
            if button.get_attribute('innerText')=='Query':
                button.click()

    def fill_hero_dict(self):
        self.matches_analyzed=0
        all_pages_buttons = self.driver.find_element_by_id('DataTables_Table_0_paginate').find_elements_by_tag_name(
            'li')
        pages = int(all_pages_buttons[-2].get_attribute('innerText'))

        for table_page in range(pages):
            rows = self.driver.find_element_by_id(
                'DataTables_Table_0').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
            for row in rows:
                self.matches_analyzed+=1
                columns = row.find_elements_by_tag_name('td')
                match_number = columns[0].get_attribute('innerText')
                match_result = 'Win' if columns[-1].get_attribute("innerText") == 'Team A' else 'Lose'
                other_team=columns[8].find_element_by_tag_name('a').get_attribute('href').split('/')[-1]
                other_team_glico=float(self.glico_dict[other_team])
                glico_points_for_match=other_team_glico/self.team_glico if match_result=='Win' else -(self.team_glico/other_team_glico)

                picked_heroes = columns[7].find_elements_by_tag_name('img')

                for hero_index in range(len(picked_heroes)):
                    picked_heroes[hero_index]=picked_heroes[hero_index].get_attribute('title')

                for hero in picked_heroes:
                    self.heroes_stats[hero][match_number]=(glico_points_for_match,[])
                    s=self.heroes_stats[hero][match_number][1]

                    for other_hero in picked_heroes:
                        if other_hero == hero:
                            continue
                        s.append(other_hero)

            all_pages_buttons = self.driver.find_element_by_id('DataTables_Table_0_paginate').find_elements_by_tag_name(
                'li')
            if table_page != pages:
                all_pages_buttons[-1].find_element_by_tag_name('a').click()
