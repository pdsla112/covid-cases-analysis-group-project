"""
Template for the COMP1730/6730 project assignment, S2 2021.
The assignment specification is available on the course web
site, at https://cs.anu.edu.au/courses/comp1730/assessment/project/
The assignment is due 25/10/2021 at 9:00 am, Canberra time
Collaborators: u6943702, u6841276, u7067919
"""

import os
import pandas as pd
import datetime as dt

         
# Question 1:
def find_total_worldwide(df, latest_csv):
    """
    Function for printing desired results for question 1 (b). Requires parameter
    inputs of a Pandas dataframe of the most recent data, and the name of the
    latest csv file. Returns null, but prints the desired information for this question.
    """
    latest_update = max(df["Last_Update"])
    total_cases = df["Confirmed"].sum()
    total_deaths = df["Deaths"].sum()
    print("Question 1:\n"
          F"Most recent data is in file `{latest_csv}`\n"
          F"Last updated at {latest_update}\n"
          F"Total worldwide cases: {total_cases:,} , Total worldwide deaths: {total_deaths:,}\n")


# Question 2:
def get_question_2_results(df, all_csv, path_to_files):
    df = df.groupby("Country_Region", as_index=False)[["Confirmed", "Deaths"]].sum()
    
    all_csv.sort()
    second_latest_csv = all_csv[-2]
    df2 = pd.read_csv(path_to_files + "/" + second_latest_csv)
    df2 = df2.groupby("Country_Region", as_index=False)["Confirmed"].sum()
    df["new_cases"] = df["Confirmed"] - df2["Confirmed"]
    
    file_10_days_ago = all_csv[-10]
    df_10_days_ago = pd.read_csv("./covid-data/" + file_10_days_ago)
    df_10_days_ago = df_10_days_ago.groupby("Country_Region", as_index=False)["Confirmed"].sum()
    df["active"] = df["Confirmed"] - df_10_days_ago["Confirmed"]
    
    df = df.sort_values(by="Confirmed", ascending=False)
    df = df.iloc[0:10, :]
    
    print("Question 2:")
    for row in df.itertuples(index=False):
        print(F"{row.Country_Region} - total cases: {row.Confirmed:,} | deaths: {row.Deaths:,} | new cases: {row.new_cases:,} | active: {row.active:,}")
    print()


#total_cases = total_deaths + active + total_recovery
#1024 = 30 + 24 + total_recovery

# Question 3 (a):
def question_3_a(all_csv, path_to_files):
    all_csv.sort()
    all_csv.reverse()
    
    all_read_csv = [pd.read_csv(path_to_files + "/" + i) for i in all_csv]
    
    print("Question 3 (a):")
    for j in range(len(all_csv) - 1): 
        new_df = all_read_csv[j]
        old_df = all_read_csv[j + 1]
        new_cases = new_df["Confirmed"].sum() - old_df["Confirmed"].sum()
        new_deaths = new_df["Deaths"].sum() - old_df["Deaths"].sum()
        file_name = all_csv[j].split(".")[0]
        print(F"{file_name} : new cases: {new_cases:,} new deaths: {new_deaths:,}")
    print()
    
    
# Question 3(b)
def weekly_cases_and_deaths(file, path_to_files):
    print("\nQuestion 3 b)")
    df = []
    file.sort()

    for csv_name in file:
        path = path_to_files + "/" + csv_name
        df.append(pd.read_csv(path))

    '''This code is designed to work in the generic case where the number of date files is unkown and the days of the week they start with are random.
    To do this the code is divided into three print statement cases:
        1. The first week since it doesnt start on a Monday; start=??, end=Mon
        2. The middle weeks which start and and on a Monday; start=end=Mon
        3. The final week which doesnt have to end on a MOnday; start=Mon, end=??
    '''
    
    ''' Some assumptions on the input: if your first day is a date other than monday you must still have files for monday untill that specific day in the folder'''
    n = (len(file)-1) // 7 # Calculated the number of complete weeks + the first week
    r = (len(file)-1) - n*7 # calculated the number of days in the final week
    
    def formatted_date(index):#takes index of file
        start_d = dt.datetime.strptime(file[index].split(".")[0], '%m-%d-%Y')
        return dt.date.strftime(start_d, "%Y-%m-%d")
    
    """ This prints the cases for an incomplete week, that is a week that ends on a day other than sunday"""
    if r != 0:
        new_end_date = formatted_date(n*7+r) # last day of last week
        new_start_date = formatted_date(n*7+1) # monday of the last week
        deaths = str(sum(df[n*7+r]['Deaths']) - sum(df[n*7]['Deaths']))
        confirmed = str(sum(df[n*7+r]['Confirmed']) - sum(df[n*7]['Confirmed']))
        print("Week "+ new_start_date +" to " + new_end_date + " new cases: " + confirmed + " new deaths: " + deaths)
       
    
    """ This prints the cases for the first week regardless whether complete or not and all the following complete weeks """
    starting_day = 1 #monday=0, tues=1 .... Sunday = 6 - this is the starting day for the first week
    
    # the reason for decrementing the for loop is to avoid a reverse sort later
    for i in range(n-1,-1,-1): # repeats the code n times where n is the number weeks; in revers order
        new_start_date = formatted_date((i+1)*7)
        """ this is the special print statement for the first week since it may be incomplete"""
        if i==0:
            new_end_date = formatted_date(i*7+starting_day+1)
            deaths = str(sum(df[(i+1)*7]['Deaths']) - sum(df[i*7+starting_day]['Deaths']))
            confirmed = str(sum(df[(i+1)*7]['Confirmed']) - sum(df[i*7+starting_day]['Confirmed']))
            print("Week "+new_end_date + " to " + new_start_date + " new cases: "+ confirmed + " new deaths: " + deaths )
        else:
            new_end_date = formatted_date(i*7+1)
            deaths = str(sum(df[(i+1)*7]['Deaths']) - sum(df[i*7]['Deaths']))
            confirmed = str(sum(df[(i+1)*7]['Confirmed']) - sum(df[i*7]['Confirmed']))  
            print("Week " + new_end_date + " to " + new_start_date + " new cases: " + confirmed + " new deaths: " + deaths) 
    print()
    

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
    df["combined_incidence"] = get_combined_incident_rate(df["Confirmed"], df["population"])
    df["case_fatality_rate"] = get_case_fatality(df["Deaths"], df["Confirmed"])
    df = df.sort_values(by="combined_incidence", ascending=False)
    df = df.iloc[0:10,:]
    print("Question 4:")
    for row in df.itertuples(index=False):
        print(F"{row.Country_Region} : {row.combined_incidence:,} cases per 100,000 people | case-fatality ratio: {row.case_fatality_rate} %")
    print("\n")
    
def get_population(cases, incident_rate):
    """
    Helper function for find_rates function. Returns the population of a 
    row/country-region. Requires inputs of the confirmed cases and incident_rate
    for that row.
    """
    population = (100000 * cases) / incident_rate
    return population

def get_combined_incident_rate(confirmed, population):
    """
    Helper function for find_rates function. Returns the calculated incident
    rate for a country. Requires inputs of the confirmed cases and
    population for that row.
    """
    incident_rate = round((confirmed / population) * 100000, 3)
    return incident_rate

def get_case_fatality(deaths, confirmed):
    """
    Helper function for find_rates function. Returns the calculated case
    fatality for a country. Requires inpurs of the total deaths and confirmed
    cases for that row.
    """
    case_fatality_rate = round((deaths / confirmed) * 100, 3)
    return case_fatality_rate
    
    
    
    
    
    

def analyse(path_to_files):
    all_csv = os.listdir(path_to_files)
    all_csv = [csv_file for csv_file in all_csv if csv_file.endswith(".csv")]
    latest_csv = max(all_csv)
    df = pd.read_csv(path_to_files + "/" + latest_csv)
    print(F"Analysing data from folder {path_to_files}")
    print()
    
    #Q1
    find_total_worldwide(df, latest_csv)
    
    #Q2
    get_question_2_results(df, all_csv, path_to_files)
    
    #Q3
    question_3_a(all_csv, path_to_files)
    weekly_cases_and_deaths(all_csv, path_to_files)
    
    #Q4
    find_rates(df)


# The section below will be executed when you run this file.
# Use it to run tests of your analysis function on the data
# files provided.

if __name__ == '__main__':
    # test on folder containg all CSV files
    analyse('./covid-data')