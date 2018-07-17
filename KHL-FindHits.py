import csv
import time 
import re

def average_stats(my_stats):
    answer = 0
    try:
        #sum(map(int,re.sub(';','',re.sub('[A-Z]','0',my_stats)).split("-")))/len(re.sub(';','',re.sub('[A-Z]','0',my_stats)).split("-"))"
        #test=';5-9-3-4-3'
        #test[:5]
        #sum(map(int,re.sub(';','',re.sub('[A-Z]','0',test)).split("-")))/len(re.sub(';','',re.sub('[A-Z]','0',test)).split("-"))
        answer=sum(map(int,re.sub(';','',re.sub('[A-Z]','0',my_stats))[:-1].split("-")))/len(re.sub(';','',re.sub('[A-Z]','0',my_stats))[:-1].split("-"))
    except ValueError:
        answer=0
    return str(answer)

#Set output location
base_file = "C:\\Temp\\Results\\SportStats-Output\\"
KHL=base_file+"KHL\\Review-test.csv"

#Inputs
DB_KHL =  base_file+"DB_KHL-test.csv"
KHL_Week= base_file+"DB_KHL_Week-test.csv"

#Initialise file
with open(KHL,'w') as t:
    t.write("Date,Home Team, Away Team,Exact Match Up,EMU-Average,Reverse Match Up, RMU-Average,Home Recent, HR-Average, Away Recent, AR-Average,\n")

#Opens Days racing
with open(KHL_Week,newline='') as f:
    reader = csv.reader(f)

    #Skip first row
    next(reader)
    for row in reader:
        #Initialise lists
        game_match=[]
        r_game_match=[]
        home_form=[]
        away_form=[]
        #Open database
        with open(DB_KHL, newline = '')as p:
            db_reader = csv.reader(p)
            #Skip header
            next(db_reader)
            #Parse through full database
            for db_row in db_reader:   
                if row[1]==db_row[1]:
                    home_form.append(db_row[4])
                if row[2]==db_row[2]:
                    away_form.append(db_row[4])
                if row[1]==db_row[1] and row[2]==db_row[2]:
                    game_match.append(db_row[4])
                if row[2]==db_row[1] and row[1]==db_row[2]:
                    r_game_match.append(db_row[4])
        matchup_write=";"
        r_matchup_write=";"
        home_form_write=";"
        away_form_write=";"
        match_avg = None
        r_match_avg = None
        home_avg = None
        away_avg = None
        delimiter = "-"
        for hf in home_form[:5]:
            home_form_write += hf+delimiter 
        home_avg = average_stats(home_form_write)
        for af in away_form[:5]:
            away_form_write += af+delimiter 
        away_avg=average_stats(away_form_write)
        for gm in game_match[:5]:
            matchup_write += gm+delimiter 
        match_avg=average_stats(matchup_write)
        for rm in r_game_match[:5]:
            r_matchup_write += rm+delimiter 
        r_match_avg=average_stats(r_matchup_write)

        with open(KHL,'a') as a:
            #t.write("Date,Home Team, Away Team,Exact Match Up,EMU-Average,Reverse Match Up, RMU-Average,Home Recent, HR-Average, Away Recent, AR-Average,\n")
            a.write(row[0]+","+row[1]+","+row[2]+","+matchup_write[:-1]+","+match_avg+","+r_matchup_write[:-1]+","+r_match_avg+","+home_form_write[:-1]+","+home_avg+","+away_form_write[:-1]+","+away_avg+"\n")
print("Complete")
    