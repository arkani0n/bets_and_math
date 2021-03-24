import requests
from bs4 import BeautifulSoup


id = 0
all_heroes_dic = {}
hero_rels = []
games = []
for_hero_rename=''
main_page = 'https://www.datdota.com'
url = input('Enter team URL here: ')

team_code = url.split('/')[-1]
print(team_code)
patch_now = '7.28'

with open('all_heroes.txt', 'r') as heroes:
    for hero in heroes.readlines():
        all_heroes_dic[hero.strip()] = (id,[0,0])
        id += 1

for i in range(len(all_heroes_dic)):
    blank = [[0, 0] for x in range(len(all_heroes_dic))]
    hero_rels.append(blank)

html = requests.get(url).text
soup = BeautifulSoup(html, 'lxml')
board = soup.find('table', id="recent-games").tbody
rows = board.find_all('tr')
c = 0
for row in rows:
    heroes = []


    match_result = row.find_all('td')[-1].text
    match_id=row.a['href']

    match = requests.get(main_page + row.a['href']).text
    soup_for_match = BeautifulSoup(match, 'lxml')
    patch = soup_for_match.find('div', class_="row border-bottom white-bg dashboard-header").h2.text.split()[-1]
    data = soup_for_match.find('div', class_="row border-bottom white-bg dashboard-header").find_all('h3')[
        1].text.split()

    if patch!=patch_now:
        break
    print(data)
    print(match_id)
    c += 1
    print(c)

    if soup_for_match.find('div', id='top-level').a['href'].split('/')[-1] == team_code:
        team_board = soup_for_match.find('table', id="team-radiant").tbody
    else:
        team_board = soup_for_match.find('table', id="team-dire").tbody
    for hero in team_board.find_all('tr'):
        heroes.append(hero.td.span.text)
    #print('\n pick',heroes)
    for hero in heroes:
        for other_hero in heroes:
            if other_hero == hero:
                continue
            hero_index = all_heroes_dic[hero][0]
            other_hero_index = all_heroes_dic[other_hero][0]
            hero_rels[hero_index][other_hero_index][match_result != 'Win'] += 1
        all_heroes_dic[hero][1][match_result != 'Win']+=1
            #print('{} {} {}'.format(hero,other_hero, match_result))
    # print(heroes)

# print(all_heroes_dic)
# print(hero_rels)

print()
for i in hero_rels:
    for j in i:
        print(str(j[0]) + '.' + str(j[1]), end=',')
    print()

print('\n Heroes \n')
for i in all_heroes_dic:
    win,lose=all_heroes_dic[i][1][0],all_heroes_dic[i][1][1]
    times_played=win+lose
    if times_played==0:
        win_rate='None'
    elif win==0:
        win_rate=0
    else: win_rate=round(win/times_played,4)
    print('{} {}({}%)'.format(i,times_played,win_rate*100 if win_rate!='None' else 'None'))
print()
input('')