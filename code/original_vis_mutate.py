
import pandas as pd 
import sys
import numpy as np



def main(diag = "../data/diagnoses.csv", even = "../data/events.csv"):
    diags = pd.read_csv(diag)
    events = pd.read_csv(even)

    recent_diags = pd.DataFrame(columns=list(diags.columns))

    for ids in diags["EventID"].unique():
        most_recent = max(diags[diags["EventID"] == ids]["DiagnosisDateTime"])
        most_recent = diags[diags["DiagnosisDateTime"] == most_recent]
        recent_diags = recent_diags.append(most_recent, ignore_index=False)

    print(recent_diags)

    return None

if __name__ == "__main__":
    status = main()
    sys.exit(status)
