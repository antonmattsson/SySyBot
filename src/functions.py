import csv
import os
from prettytable import PrettyTable


def insert_event(event):
    f = open("player_table.txt")
    tbl = list(csv.reader(f,delimiter = "\t"))
    f.close()
    found = False
    if os.path.getsize('player_table.txt') > 0:
        for i in range(0,len(tbl)):
            if tbl[i][0] == event['player'] and tbl[i][1] == event['team']:
                found = True
                tbl[i][3] = float(tbl[i][3]) + event['duration']
                if event['sport'] not in tbl[i][2]:
                    tbl[i][2] = ''.join([tbl[i][2],";",event['sport']])
                    tbl[i][3] += 2
    if not found:
        tbl.append([event['player'],event['team'],event['sport'],float(event['duration']) + 2])
    with open("player_table.txt",'w',newline='') as f:
        wrtr = csv.writer(f,delimiter = "\t")
        wrtr.writerows(tbl)
    with open("log.txt",'a',newline = '') as f:
        wrtr = csv.writer(f,delimiter = "\t")
        wrtr.writerow([event['player'],event['team'],event['sport'],event['duration']])


def update_teams():
    f = open("player_table.txt")
    tbl = list(csv.reader(f,delimiter = "\t"))
    f.close()
    teams = []
    for row in tbl:
        teams.append(row[1])
    teams = list(set(teams)) # Unique teams
    for i in range (0,len(teams)):
        teams[i] = [teams[i],0,0]
        for row in tbl:
            if row[1] == teams[i][0]:
                teams[i][1] += 1
                teams[i][2] += float(row[3])
        teams[i] = [teams[i][0],teams[i][2]/teams[i][1]]
    srtd = sorted(teams, key=lambda x: x[1], reverse=True)
        
    with open("team_table.txt",'w',newline='') as f:
        wrtr = csv.writer(f,delimiter = "\t")
        wrtr.writerows(srtd)


def get_scores():
    f = open("team_table.txt")
    tbl = list(csv.reader(f,delimiter = "\t"))
    p = PrettyTable()
    for row in tbl:
        p.add_row(row)
    return (p.get_string(header=False, border=False))


def dumbass(string):
    string = string.strip()
    string = string.lower()
    string = string.capitalize()
    return string