from selenium import webdriver
from selenium.webdriver.common.by import By
import matplotlib.pyplot as plt
from matplotlib import use
import numpy as np
use('TkAgg') # check https://stackoverflow.com/questions/69870135/attributeerror-module-backend-interagg-has-no-attribute-figurecanvas

class GrafMaker:
    def __init__(self,team_url):
        self.driver=webdriver.Chrome()
        self.Plot = Plot()
        self.team_url=team_url
        self.heroes_dic=self.set_heroes_dic()
        self.heroes_rels=self.set_heroes_rels()
        self.picked_heroes_names=[]
        self.picked_heroes_dict = {}
        self.max_picks = 0

    def plot_graff(self):
        self.set_picked_heroes_dict()
        self.set_picked_heroes_dict_connections()
        self.get_max_number_of_picks()
        self.set_plot_cords_and_names_dict()

        print(self.picked_heroes_dict)
        print()
        print(self.coords_and_names)
        print()
        print(self.max_picks)
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        color_index=0
        counted_heroes = []
        for hero in self.picked_heroes_dict:
            color_index+=1
            color = colors[color_index]
            hero_x_cord = self.picked_heroes_dict[hero]["total_number_of_picks"]
            hero_y_cord = self.picked_heroes_dict[hero]["winrate"]
            for other_hero in self.picked_heroes_dict[hero]["connections"]:
                if self.picked_heroes_dict[hero]["connections"][other_hero]["win_number"] == 0 and self.picked_heroes_dict[hero]["connections"][other_hero]["lose_number"] == 0:
                    continue
                if other_hero in counted_heroes:
                    continue
                other_hero_x_cord = self.picked_heroes_dict[other_hero]["total_number_of_picks"]
                other_hero_y_cord = self.picked_heroes_dict[other_hero]["winrate"]
                other_hero_connection_stat = f'{self.picked_heroes_dict[hero]["connections"][other_hero]["win_number"]} | {self.picked_heroes_dict[hero]["connections"][other_hero]["lose_number"]}'
                self.Plot.plot(x=[hero_x_cord, other_hero_x_cord], y= [hero_y_cord, other_hero_y_cord], color=color)
                self.Plot.annotate(x=(float(hero_x_cord) + float(other_hero_x_cord))/2, y=(float(hero_y_cord) + float(other_hero_y_cord))/2, text=other_hero_connection_stat)
            counted_heroes.append(hero)
        for cords in self.sorted_coords():
            x_cord, y_cord = cords.split()
            # self.Plot.plot(x=int(x_cord),y=float(y_cord))float(hero_x_cord) + float(other_hero_x_cord)
            self.Plot.annotate(x=int(x_cord),y=float(y_cord),text=self.coords_and_names[cords])

        self.Plot.set_x_lim(int(self.max_picks))
        self.Plot.set_y_lim(1)

        self.Plot.show()

    def sorted_coords(self):

        def select_y(coords):
            return coords.split()[1]

        def select_x(coords):
            return coords.split()[0]

        sorted_coords_and_names = sorted(sorted(self.coords_and_names.keys(), key=select_x), key=select_y)
        return sorted_coords_and_names

    def set_plot_cords_and_names_dict(self):
        self.coords_and_names = {}
        for hero in self.picked_heroes_dict:
            x_cord = self.picked_heroes_dict[hero]["total_number_of_picks"]
            y_cord = self.picked_heroes_dict[hero]["winrate"]
            if f"{x_cord} {y_cord}" not in self.coords_and_names:
                self.coords_and_names[f"{x_cord} {y_cord}"] = hero
            else:
                self.coords_and_names[f"{x_cord} {y_cord}"] = self.coords_and_names[f"{x_cord} {y_cord}"] + " | " + hero

    def get_max_number_of_picks(self):
        self.max_picks = max([sum(self.heroes_dic[hero_name][1]) for hero_name in self.heroes_dic])
        # print([sum(self.heroes_dic[hero_name][1]) for hero_name in self.heroes_dic])
        # print("^^^^")

        """
        sum(self.heroes_dic[hero_name][1] is a list in format [number of wins, number of lose]
        max(sum(self.heroes_dic[hero_name][1]) gets the biggest number on matches among all heroes
        """

    def set_picked_heroes_dict(self):
        for hero_name in self.picked_heroes_names:
            self.picked_heroes_dict[hero_name] = {
                "id"                    : self.heroes_dic[hero_name][0], # check def set_heroes_dic for heroes_dic structure
                "total_number_of_picks" : sum(self.heroes_dic[hero_name][1]),
                "winrate"               : round(self.heroes_dic[hero_name][1][0] / (self.heroes_dic[hero_name][1][0] + self.heroes_dic[hero_name][1][1]), 2) if (self.heroes_dic[hero_name][1][0] + self.heroes_dic[hero_name][1][1]) != 0 else 0
            }
        """
        dict{
            hero{
                id : 
                total_number_of_picks : int,
                winrate : float % , # round(float, 2)
                connections { # set in def set_picked_heroes_connections_connections
                    hero_name : {
                        win : int,
                        lose : int
                    }
                }


            }

        }
        """
    def set_picked_heroes_dict_connections(self):
        for hero_name in self.picked_heroes_names:
            connections = {}
            hero_id = self.picked_heroes_dict[hero_name]["id"]

            for other_hero_name in self.picked_heroes_names:
                if hero_name == other_hero_name:
                    continue
                other_hero_id = self.picked_heroes_dict[other_hero_name]["id"]
                connections[other_hero_name] = {
                    "win_number" : self.heroes_rels[hero_id][other_hero_id][0],
                    "lose_number" : self.heroes_rels[hero_id][other_hero_id][1]
                }
            self.picked_heroes_dict[hero_name]["connections"] = connections

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
        #dic{
#            hero = (
    #            id,
    #            [
    #               0, # win
    #               0  # lose
    #            ]
    #         )
#
#
#
#
    def set_heroes_rels(self):
        hero_rels=[]
        for i in range(len(self.heroes_dic)):
            blank = [[0, 0] for x in range(len(self.heroes_dic))]
            hero_rels.append(blank)
        return hero_rels
    # hero_rels[
    #     [
    #         120*[0, 0]
    #     ],
    #     [
    #         120*[0, 0]
    #     ]...
    # ]
    # Hero rels is a list with 120 lists that cointain 120 [0, 0] each

    def heroes_rel_to_str(self):
        heroes_rel_str=''
        print('hero_rel_to_str_start')
        for i in self.heroes_rels:
            for j in i:
                heroes_rel_str+=(str(j[0]) + '.' + str(j[1])+',')
            heroes_rel_str+='\n'
        print('done')
        return heroes_rel_str

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


class Plot:

    def __init__(self):
        self.fig, self.ax = plt.subplots()  # Create a figure containing a single axes.
        self.ax.set_ylabel('Winrate')
        self.ax.set_xlabel('Pick times')

    def plot(self,x,y,color):
        self.ax.plot(x,y, marker='o', color=color)

    def annotate(self,x,y,text):
        self.ax.annotate(str(text), (x, y), fontsize=12, horizontalalignment='center', verticalalignment='center')

    def set_x_lim(self,max_x):
        self.ax.set_xlim(0, int(max_x))

    def set_y_lim(self,max_y):
        self.ax.set_ylim(0, int(max_y))

    def show(self):
        plt.show()




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

