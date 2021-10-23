"""
Template for the COMP1730/6730 project assignment, S2 2021.
The assignment specification is available on the course web
site, at https://cs.anu.edu.au/courses/comp1730/assessment/project/


The assignment is due 25/10/2021 at 9:00 am, Canberra time

Collaborators: u6943702
"""

import os
import pandas as pd

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
    latest_csv = max(all_csv)
    df = pd.read_csv(path_to_files + "/" + latest_csv)
    print(F"Analysing data from folder {path_to_files}")
    print()
    find_most_recent(df, latest_csv)
    find_total_worldwide(df, latest_csv)
    find_rates(df)


# The section below will be executed when you run this file.
# Use it to run tests of your analysis function on the data
# files provided.

if __name__ == '__main__':
    # test on folder containg all CSV files
    analyse('./covid-data')