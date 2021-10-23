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


# Question 1 (a):
def find_most_recent(df, latest_csv):
    """
    Function for printing desired results for question 1 (a). Requires parameter
    inputs of a Pandas dataframe of the most recent data, and the name of the
    latest csv file. Returns null, but prints the desired information for this question.
    """
    latest_update = max(df["Last_Update"])
    print("Question 1 (a):\n"
          F"Most recent data is in file `{latest_csv}`\n"
          F"Last updated at {latest_update}\n")
        
        
# Question 1 (b):
def find_total_worldwide(df, latest_csv):
    """
    Function for printing desired results for question 1 (b). Requires parameter
    inputs of a Pandas dataframe of the most recent data, and the name of the
    latest csv file. Returns null, but prints the desired information for this question.
    """
    latest_update = max(df["Last_Update"])
    total_cases = df["Confirmed"].sum()
    total_deaths = df["Deaths"].sum()
    print("Question 1 (b):\n"
          F"Most recent data is in file `{latest_csv}`\n"
          F"Last updated at {latest_update}\n"
          F"Total worldwide cases: {total_cases}, Total worldwide deaths: {total_deaths}\n")
    
# Question 2(a)

from os import listdir

def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]



#filenames = []#find_csv_filenames("covid-data")




def find_total_cases_and_death_each_country():
     confirm_cases_dict = {}
     death_cases_dict = {}
    
     name = "09-14-2021.csv"
     df = pd.read_csv ("covid-data/"+name)
     df = pd.DataFrame(df, columns= ['Country_Region','Confirmed','Deaths'])
     for index,row in df.iterrows():
         if not row['Country_Region'] in confirm_cases_dict:
             confirm_cases_dict[row['Country_Region']] = int(row['Confirmed'])
             death_cases_dict[row['Country_Region']] = int(row['Deaths'])
           
         else:
             confirm_cases_dict[row['Country_Region']] += int(row['Confirmed'])
             death_cases_dict[row['Country_Region']] += int(row['Deaths'])
             
     #print(confirm_cases_dict)
     confirmed_arr = sorted(confirm_cases_dict.items(), key=lambda x: x[1], reverse=True)
     death_arr = sorted(death_cases_dict.items(), key=lambda x: x[1], reverse=True)
     
     
     for i in range(10):
        print('total cases in '+ str(confirmed_arr[i][0]) + ' is '+ str(confirmed_arr[i][1]))
      
      
     for i in range(10):
        print('Death in '+ str(death_arr[i][0]) + ' is '+ str(confirmed_arr[i][1]))
      
     return confirmed_arr
     return death_arr



#Question 2(b)

#filenames = find_csv_filenames("covid-data")

def find_new_cases_last_two():
    
    confirm_arr = find_total_cases_and_death_each_country()
    confirm_second_dict = {}
    
    name = '09-13-2021.csv'
    df = pd.read_csv ("covid-data/"+ name)
    df = pd.DataFrame(df, columns= ['Country_Region','Confirmed'])

    
    for index,row in df.iterrows():
        
        if not row['Country_Region'] in confirm_second_dict:
             confirm_second_dict[row['Country_Region']] = int(row['Confirmed'])
        else:
             confirm_second_dict[row['Country_Region']] += int(row['Confirmed'])
    
           
    confirmed_second_arr = sorted(confirm_second_dict.items(), key=lambda x: x[1], reverse=True)
    
    for i in range(0,10):
        
        print('total new '
              + str(confirmed_second_arr[i][0]) + ' is ' + str(confirm_arr[i][1]-confirmed_second_arr[i][1]))
     
    
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

# Question 4:
def find_rates(df):
    """
    Function for printing desired results for question 4. Requires parameter
    input of a Pandas dataframe of the most recent data. Returns null, but prints
    the desired information for this question. Depends on two helper functions
    get_population and print_stats_country.
    """
    pd.options.mode.chained_assignment = None
    df = df.dropna(subset=["Incident_Rate"])
    df["population"] = get_population(df.loc[:,"Confirmed"], df.loc[:,"Incident_Rate"])
    df = df.groupby("Country_Region", as_index=False)[["population", "Confirmed", "Deaths"]].sum()
    print("Question 4:")
    for row in df.itertuples(index=False):
        print_stats_country(row.Country_Region, row.population, row.Confirmed, row.Deaths)
    print("\n")
    
def get_population(cases, incident_rate):
    """
    Helper function for find_rates function. Returns the population of each 
    row/country-region. Requires inputs of the confirmed cases and incident_rate
    for that row.
    """
    population = (100000 * cases) / incident_rate
    return population

def print_stats_country(country, population, confirmed, deaths):
    """
    Helper function for find_rates function. Calculates the incident_rate and 
    case_fatality_rate of that row. This row contains the data of the entire 
    country, not its smaller regions. Prints the desired result for question 4 
    for each country into the console. Requires country name, population count, 
    confirmed cases, and death cases as inputs. 
    """
    incident_rate = round((confirmed / population) * 100000, 3)
    case_fatality_rate = round((deaths / confirmed) * 100, 3)
    print(F"{country} : {incident_rate} cases per 100,000 people and case-fatality ratio: {case_fatality_rate} %")
    
    
    
    
    
    
    
    

def analyse(path_to_files):
    all_csv = os.listdir(path_to_files)
    all_csv = [csv_file for csv_file in all_csv if csv_file.endswith(".csv")]
    all_csv = all_csv.sort(reverse=True)
    latest_csv = all_csv[0]
    df = pd.read_csv(path_to_files + "/" + latest_csv)
    print(F"Analysing data from folder {path_to_files}")
    print()
    find_most_recent(df, latest_csv)
    find_total_worldwide(df, latest_csv)
    find_total_cases_deaths(df)
    find_rates(df)


# The section below will be executed when you run this file.
# Use it to run tests of your analysis function on the data
# files provided.

if __name__ == '__main__':
    # test on folder containg all CSV files
    analyse('./covid-data')