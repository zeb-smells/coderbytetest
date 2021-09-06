import pandas as pd 
import sys




def main(diag = "../data/diagnoses.csv", even = "../data/events.csv"):
    diags = pd.read_csv(diag)
    events = pd.read_csv(even)

    recent_diags = []
    for ids in diags["EventID"].unique():
        most_recent = max(diags[diags["EventID"] == ids]["DiagnosisDateTime"])
        most_recent = diags[diags["DiagnosisDateTime"] == most_recent]["Diagnosis"]
        recent_diags.append(most_recent)

    print(recent_diags)
main()