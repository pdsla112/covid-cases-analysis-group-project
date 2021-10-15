"""
Template for the COMP1730/6730 project assignment, S2 2021.
The assignment specification is available on the course web
site, at https://cs.anu.edu.au/courses/comp1730/assessment/project/


The assignment is due 25/10/2021 at 9:00 am, Canberra time

Collaborators: u6943702
"""

import os
import pandas as pd

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
        

# Question 1 (b) (still working on it):
def find_total_worldwide():
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
        
