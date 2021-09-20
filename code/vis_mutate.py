""" 
Program Name: vis.mutate.py
Author:       Zebulon(Zeb) Bond
Contact:      bondzeb@gmail.com

A simple program which adds a new column onto an events .csv containing the most recent diagnosis
After that event. 

The program takes two arguments from the command line the directory addresses of a diagnosis.csv 
and a events.csv if no arguments are provided two default files are used. 
"""

# IMPORTS
import pandas as pd 
import sys
import numpy as np

# FUNCTIONS
def extract_mrdiag(diags):
    """
    Extracts the most recent diagnosis for each Event ID
    
    ARGUMENTS
    diags: a pandas.DataFrame containing a minimum of 2 columns named EventID and
           DiagnosisDateTime 
    
    OUTPUT
    recent_diags: a pandas.DataFrame of the most recent diagnosis for each EventID
    """
    recent_diags = pd.DataFrame(columns=list(diags.columns))
    
    for ids in diags["EventID"].unique():
        #extract most recent diagnosis time
        most_recent = max(diags[diags["EventID"] == ids]["DiagnosisDateTime"])
        #get diagnosis at most recent time
        most_recent = diags[diags["DiagnosisDateTime"] == most_recent]
        recent_diags = recent_diags.append(most_recent, ignore_index=False)
    
    return(recent_diags)
	
def apply_diags(recent_diags, events):
    """
    adds diagnosis column to events DataFrame
    
    ARGUMENTS
    recent_diags: a pandas.DataFrame of the most recent diagnosis for each EventID
    events: the events.csv as a dataframe
    
    OUTPUT
    events: the events.csv with additional column
    """
    
    #preallocate
    diags = np.empty(len(events), dtype=object)
    diags[:] = np.nan
    
    #create additional column
    for id_ in events["EventID"]:
        for id_d in recent_diags["EventID"]:
            if id_ == id_d:
                diag = recent_diags[recent_diags["EventID"] == id_]["Diagnosis"]
                diags[events["EventID"] == id_] = diag
                break
     
    #add additional column               
    events["Diagnosis"] = diags
    return events

# MAIN
def main(args):
    """
    The main function -> runs the whole program
    """
    
    #check if arguments provided on the command line
    if len(args) == 1:
        print("No Arguments Provided: Performing Default Mutation")
        diags, events = ["../data/diagnoses.csv", "../data/events.csv"] 
    else:
        diags, events = args[1:2]
    
    #load csvs
    diags = pd.read_csv(diags)
    events = pd.read_csv(events)
    
    #extract most recent diags
    recent_diags = extract_mrdiag(diags)
    events = apply_diags(recent_diags, events)
    
    events.to_csv("../results/new_events.csv")
    
    return 0

if __name__ == "__main__":
    status = main(sys.argv)
    sys.exit(status)
