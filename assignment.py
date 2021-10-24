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
          F"Total worldwide cases: {total_cases:,}, Total worldwide deaths: {total_deaths:,}\n")


# Question 2:
def get_question_2_results(df, all_csv, path_to_files):
    """
    Function that prints the relevant results for question 2. Requires inputs of 
    the lastest dataframe df, list of all csv file names all_csv, and string
    path to data files path_to_files. Please read all the comments to know the
    various assumptions made for estimation of active cases. Assumes that covid symptoms 
    disappear after 10 days for most people according to CDC.
    """
    # Working for question 2 (a)
    df = df.groupby("Country_Region", as_index=False)[["Confirmed", "Deaths"]].sum()
    
    # Working for question 2 (b)
    all_csv.sort()
    second_latest_csv = all_csv[-2]
    df2 = pd.read_csv(path_to_files + "/" + second_latest_csv)
    df2 = df2.groupby("Country_Region", as_index=False)["Confirmed"].sum()
    df["new_cases"] = df["Confirmed"] - df2["Confirmed"]
    
    # Working for question 2 (c)
    file_10_days_ago = all_csv[-10]  # Get the csv data from 10 days ago.
    df_10_days_ago = pd.read_csv("./covid-data/" + file_10_days_ago)
    df_10_days_ago = df_10_days_ago.groupby("Country_Region", as_index=False)["Confirmed"].sum()
    df["active"] = df["Confirmed"] - df_10_days_ago["Confirmed"]
    
    df = df.sort_values(by="Confirmed", ascending=False)
    df = df.iloc[0:10, :]  # Get the top ten rows according to the number of confirmed cases
    
    print("Question 2:")
    for row in df.itertuples(index=False):
        print(F"{row.Country_Region} - total cases: {row.Confirmed:,} | deaths: {row.Deaths:,} | new cases: {row.new_cases:,} | active: {row.active:,}")
    print()  # Leave a line spacing afterwards for cleaner presentation


#total_cases = total_deaths + active + total_recovery
#1024 = 30 + 24 + total_recovery

# Question 3 (a):
def question_3_a(all_csv, path_to_files):
    all_csv.sort()
    all_csv.reverse()
    
    all_read_csv = [pd.read_csv(path_to_files + "/" + i) for i in all_csv]
    
    print("Question 3:")
    for j in range(len(all_csv) - 1): 
        new_df = all_read_csv[j]
        old_df = all_read_csv[j + 1]
        new_cases = new_df["Confirmed"].sum() - old_df["Confirmed"].sum()
        new_deaths = new_df["Deaths"].sum() - old_df["Deaths"].sum()
        file_name = all_csv[j].split(".")[0]
        print(F"{file_name} : new cases: {new_cases:,} | new deaths: {new_deaths:,}")
    print()
    

# Question 3 (b):
def question_3_b(all_csv, path_to_files):
    all_csv.sort()
    all_csv.reverse()
    all_csv = get_only_relevant_csv(all_csv)
    all_read_csv = [pd.read_csv(path_to_files + "/" + i) for i in all_csv]
    
    print("Differece:")
    print(all_read_csv[0]["Deaths"].sum() - all_read_csv[1]["Deaths"].sum())
    
    print("Weekly Changes:")
    for j in range(0, len(all_csv) - 1, 2):
        new_df = all_read_csv[j]
        new_file_name = all_csv[j].split(".")[0]
        index = j + 1 if (j == len(all_csv) - 2) else (j + 2)
        old_df = all_read_csv[index]
        old_file_name = all_csv[j + 1].split(".")[0]
        new_cases = new_df["Confirmed"].sum() - old_df["Confirmed"].sum()
        new_deaths = new_df["Deaths"].sum() - old_df["Deaths"].sum()
        print(F"Week {old_file_name} to {new_file_name} new cases: {new_cases:,} | new deaths: {new_deaths:,}")
    print()
    
    
def get_only_relevant_csv(all_csv):
    result = []
    for i in range(len(all_csv)):
        file_name = all_csv[i].split(".")[0]
        month = int(file_name.split("-")[0])
        day = int(file_name.split("-")[1])
        year = int(file_name.split("-")[2])
        date = dt.datetime(year, month, day)
        if i == 0 or i == (len(all_csv) - 1) or date.weekday() == 0 or date.weekday() == 6:
            result.append(all_csv[i])
    return result
    
    

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
    question_3_b(all_csv, path_to_files)
    
    #Q4
    find_rates(df)


# The section below will be executed when you run this file.
# Use it to run tests of your analysis function on the data
# files provided.

if __name__ == '__main__':
    # test on folder containg all CSV files
    analyse('./covid-data')