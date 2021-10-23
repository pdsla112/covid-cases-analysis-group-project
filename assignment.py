"""
Template for the COMP1730/6730 project assignment, S2 2021.
The assignment specification is available on the course web
site, at https://cs.anu.edu.au/courses/comp1730/assessment/project/
The assignment is due 25/10/2021 at 9:00 am, Canberra time
Collaborators: u6943702, u6841276
"""

import os
import pandas as pd
import glob


def analyse(path_to_files):
    pass


# The section below will be executed when you run this file.
# Use it to run tests of your analysis function on the data
# files provided.

if __name__ == '__main__':
    # test on folder containg all CSV files
    analyse('./covid-data')
    
    

# Question 1 (a):
def find_most_recent():
    all_csv = os.listdir("./covid-data")
    all_csv = [csv_file for csv_file in all_csv if csv_file.endswith(".csv")]
    latest_csv = max(all_csv)
    df = pd.read_csv("./covid-data/" + latest_csv)
    latest_update = max(df["Last_Update"])
    print(F"""
          Analysing data from folder...
          
          Question 1:
          Most recent data is in file `{latest_csv}`
          Last updated at {latest_update}
          """)
        
        
# Question 1 (b):
def find_total_worldwide():
    all_csv = os.listdir("./covid-data")
    all_csv = [csv_file for csv_file in all_csv if csv_file.endswith(".csv")]
    latest_csv = max(all_csv)
    df = pd.read_csv("./covid-data/" + latest_csv)
    latest_update = max(df["Last_Update"])
    total_cases = df["Confirmed"].sum()
    total_deaths = df["Deaths"].sum()
    print(F"""
          Analysing data from folder ...
          
          Question 1:
          Most recent data is in file `{latest_csv}`
          Last updated at {latest_update}
          Total worldwide cases: {total_cases}, Total worldwide deaths: {total_deaths}
          """)
        
# Question 3(a):
def daily_cases_and_death():
    
    df = []
    daily_death = []
    daily_cases = []
    file = os.listdir('./covid-data')
    file.sort()
    file.reverse()
    #date = file[0].split_at('.')[0]

    for csv_name in file:
        path = './covid-data/' + csv_name
        df.append(pd.read_csv(path))
    
    cumulative_death = [sum(df[x]['Deaths']) for x in range(0, 30)] #len(df)-1) this does not working, 28
    
    for i in range(0, len(cumulative_death)-1):
        daily_death.append(cumulative_death[i] - cumulative_death[i+1])
        
    cumulative_cases = [sum(df[x]['Confirmed']) for x in range(0, 30)]
    
    for i in range(0, len(cumulative_cases)-1):
        daily_cases.append(cumulative_cases[i] - cumulative_cases[i+1])
    
    for i in range(0, 30):
        print(df[i]['Last_Update'][0].split(' ')[0] + ' : new cases: ' + str(daily_cases[i]) + ' new deaths: ' + str(daily_death[i]))
        
# Question 3(b)
def weekly_cases_and_deaths():
    
    df = []
    daily_death = []
    weekly_death = []
    file = os.listdir('./covid-data')
    file.sort()
    file.reverse()
    
    for csv_name in file:
        path = './covid-data' + csv_name
        df.append(pd.read_csv(path))
    
    cumulative_death = [sum(df[x]['Deaths']) for x in range(0, 31)] #len(df)-1) this does not working, 28
    
    for i in range(0, len(cumulative_death)):
        daily_death.append(cumulative_death[i] - cumulative_death[i+1])
        
    for i in range(0, len(daily_death)):
        one_week = 7
        if one_week > 0:
            weekly_death.append(daily_death[i] + daily_death[i+1])
            one_week -= 1
        else:
            pass
            
        
    
    
    
    
    
    
        
        

    