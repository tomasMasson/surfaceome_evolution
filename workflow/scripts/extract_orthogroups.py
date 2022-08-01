#!/usr/bin/env python3.8

"""
"""


import click
import pandas as pd
from Bio import SeqIO


def extract_orthogroups(orthogroups, multifasta, outdir):

    seqs = SeqIO.to_dict(SeqIO.parse(multifasta, "fasta"))
    df = pd.read_csv(orthogroups, sep="\t").dropna()
    dc = {}
    for row in df.iterrows():
        key = row[1].values[0]
        genes = []
        for column in row[1].values[1:]:
            for value in column.split(", "):
                genes.append(value)
        if len(genes) == 6:
            dc[key] = genes
    for key in dc:
        p = outdir + f"{key}.fasta"
        with open(p, "w") as fh:
            for i in dc[key]:
                seq = seqs[i]
                fh.write(f"{seq.id}\n{seq.seq}\n")


# CLI options
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command()
@click.option("-o",
              "--orthogroups",
              help="")
@click.option("-s",
              "--sequences",
              help="")
@click.option("-d",
              "--directory",
              help="")
def cli(orthogroups, sequences, directory):
    """
    """
    extract_orthogroups(orthogroups, sequences, directory)


if __name__ == "__main__":
    cli()
