#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup

def table_writer(data):
    #write the data to sqlite table
    print(data)
    pass

def entry_maker(data):
    # Generate a dict for each entry
    for entry in range(1, len(data[0])):
        print("{} of {}".format(entry, len(data[0])-1))
        row = {}
        for item in data:
            try:
                row[item[0]] = item[entry]
            except IndexError:
                row[item[0]] = item[entry-1]
        table_writer(row)

r=requests.get("http://www.d20srd.org/indexes/monsters.htm")
c=r.content
soup=BeautifulSoup(c, "html.parser")

monsters_list=soup.find_all("ul",{"class": "column"})
monsters = monsters_list[0].find_all("a")
monster_urls = []
for monster in monsters:
    if monster['href'].find("#") == -1:
        monster_urls.append(monster['href'])
    else:
        pass

for each in monster_urls:
    payload_url = "http://www.d20srd.org{}".format(each)
    with requests.get(payload_url) as m_data:
        c = m_data.content
        soup=BeautifulSoup(c, "html.parser")
        monster_name = soup.find_all("h1")[0].text
        print(monster_name)

    # This pulls out names for monsters that have variations on the same page
    # each with its own stat block
    titles = soup.find_all("h2")

    title = []
    formatted_head_row = []
    for item in titles:
        if item.text == "Combat":
            combat_info = item.text
        else:
            title.append(item.text)

    # Get all tables with the statBlock class
    block = soup.find_all("table", {"class": "statBlock"})
    
    i = 0
    true_name = None
    for item in block:
        if not title:
            true_name = monster_name
        elif len(title) < 2:
            true_name = monster_name
        else:
            true_name = title[i]
            i += 1
            
        
        multi_table = False   
        block_rows = item.find_all('tr')
        
        first_row = block_rows[0].text.strip().split("\n")
        second_row = block_rows[1].text.strip().split("\n")
        
        if len(first_row) != len(second_row):
            first_row.insert(0, "Name:")
            block_rows[0] = first_row
            multi_table = True
        
        if first_row[0] == 'Size/Type:':
            block_rows.insert(0,["Name:", true_name])

        stat_table_raw = []
        for item in block_rows:          

            try:
                stat_row = item.text.strip().split("\n")
            except AttributeError:
                stat_row = item    
            
            stat_table_raw.append(stat_row)
        
        entry_maker(stat_table_raw)