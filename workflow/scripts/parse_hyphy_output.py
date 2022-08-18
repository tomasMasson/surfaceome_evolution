#!/usr/bin/env python3

"""
Parse individual JSON files from Hyphy FUBAR and aBSREL methods into a TSV row
"""

import click
import csv
import json
import pandas as pd
from pathlib import Path


def load_fubar(fubar):
    """
    Read FUBAR JSON file
    """

    # Load file
    with open(fubar, "r") as fh:
        data = json.load(fh)
    # Read column headers and contents
    headers = [h[0] for h in data["MLE"]["headers"]]
    # Intialize a DataFrame for further calculations
    content = data["MLE"]["content"]["0"]
    # Drop empty columns and assign headers
    df = pd.DataFrame(content).drop([6, 7], axis=1)
    df.columns = headers

    return df


def compute_fubar_feaures(fubar):
    """
    Calculates a set of features from a FUBAR JSON file
    """

    df = load_fubar(fubar)
    # Create a dN/dS (Omega) column
    df["omega"] = df["beta"] / df["alpha"]
    # Define the features to be saved from the DataFrame
    alpha = df["alpha"].mean()
    beta = df["beta"].mean()
    omega = df["omega"].mean()
    # Fractions of negatively and positively selected residues
    f_neg = df[df["Prob[alpha>beta]"] > 0.9].shape[0] / df.shape[0]
    f_pos = df[df["Prob[alpha<beta]"] > 0.9].shape[0] / df.shape[0]
    # Store features into a list before returning them
    features = [alpha, beta, omega, f_neg, f_pos]

    return features


def load_absrel(absrel):
    """
    Read aBSREL JSON file
    """

    with open(absrel, "r") as fh:
        data = json.load(fh)

    return data


def parse_absrel_branches(absrel):
    """
    Extracts branches under positive selection,
    according to aBSREL results
    """

    data = load_absrel(absrel)
    selected_branches = []
    # Get species tested
    species = list(data["branch attributes"]["0"].keys())
    # For each species, assess if the branch test is significant
    for specie in species:
        content = data["branch attributes"]["0"][specie]
        if content["Corrected P-value"] < 0.05:
            # Save results
            selected_branches.append(specie)

    return selected_branches


def merge_fubar_absrel(fubar, absrel):
    """
    Merge into a single list the orthogroup name,
    FUBAR and aBSREL results
    """

    # Get OG from file's name
    og = Path(fubar).name.split(".")[0]
    features = compute_fubar_feaures(fubar)
    branches = parse_absrel_branches(absrel)

    return [og] + features + [branches]


@click.command()
@click.option("-f",
              "--fubar",
              help="FUBAR results from Hyphy")
@click.option("-a",
              "--absrel",
              help="aBSREL results from Hyphy")
@click.option("-o",
              "--output",
              help="Output file")
def cli(fubar, absrel, output):
    """
    Parse individual JSON files from Hyphy FUBAR and aBSREL methods into a TSV row
    """

    # Get results
    results = merge_fubar_absrel(fubar, absrel)
    # Save results as a single row (tab-delimited)
    with open(output, "w") as fh:
        writer = csv.writer(fh, delimiter="\t")
        writer.writerow(results)


if __name__ == "__main__":
    cli()
