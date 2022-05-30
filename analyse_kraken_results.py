#!usr/bin/env python3

import os
import argparse
from ete3 import NCBITaxa

def main():
    cwd = os.getcwd()
    dataset_path = os.path.join(cwd, "dataset")
    ncbi = NCBITaxa()

    parser = argparse.ArgumentParser(description = "Generates Makefile that runs Kraken2 sensitivity analysis")
    parser.add_argument("-i", required = True, help = "specify input Kraken2 database to analyse")
    args = parser.parse_args()

    # read in acc2speciesid mapping
    acc2specid_dict = {}
    with open(os.path.join(dataset_path, "iss_50r_viral_acc2speciesid.map"), "r") as r1:
        for line in r1:
            tabs = line.strip("\n").split("\t")
            acc = tabs[0]
            taxid = int(tabs[1])
            acc2specid_dict[acc] = (taxid, ncbi.get_descendant_taxa(taxid), ncbi.get_lineage(taxid))

    # read in database parameters
    with open(os.path.join(args.i, "params.txt"), "r") as r:
        params = r.readlines()[1].strip("\n").split("\t")
        k, l, s = params[0], params[1], params[2]

    # read in Kraken2 results for each database and perform calculations
    analysis_lines = []
    header = f"Database\tk\tl\ts\tTP\tFP\tVP\tFN\tClassification_rate\tSensitivity\tPPV\n"
    analysis_lines.append(header)
    num_c = num_u = num_tp = num_fp = num_fn = num_vp = 0
    
    with open(os.path.join(args.i, "results.standard"), "r") as r2:
        for line in r2:
            tabs = line.strip("\n").split("\t")
            # classified reads can be either TP, FP or VP
            if tabs[0] == "C":
                num_c += 1
                query_acc = tabs[1].split(".")[0]
                assigned_taxid = int(tabs[2])
                entry = acc2specid_dict[query_acc]
                putative_taxid, putative_taxid_desc, putative_taxid_lineage = entry[0], entry[1], entry[2]
                # compare assigned_taxid with mapping
                if assigned_taxid == putative_taxid: # assigned_taxid is exactly the putative_taxid
                    num_tp += 1
                elif assigned_taxid in putative_taxid_desc: # assigned_taxid is a descendant of putative_taxid (I)
                    num_tp += 1
                elif putative_taxid in ncbi.get_lineage(assigned_taxid): # assigned_taxid is a descendant of putative_taxid (II - ETE3 bug workaround)
                    num_tp += 1
                elif assigned_taxid in putative_taxid_lineage: # assigned_taxid is an ancestor of putative_taxid
                    num_vp += 1
                else: # assigned_taxid is neither a descendant nor an ancestor of putative_taxid
                    num_fp += 1
            # unclassified reads are automatically FN
            elif tabs[0] == "U":
                num_u += 1
                num_fn += 1
            else:
                print("Invalid result found, skipping.")
                continue

    classification_rate = "{:.2%}".format(num_c/(num_c + num_u))
    sensitivity = "{:.2%}".format(num_tp/(num_tp + num_fn + num_fp + num_vp))
    ppv = "{:.2%}".format(num_tp/(num_tp+num_fp))
    analysis_lines.append(f"{args.i}\t{k}\t{l}\t{s}\t{num_tp}\t{num_fp}\t{num_vp}\t{num_fn}\t{classification_rate}\t{sensitivity}\t{ppv}")
    
    '''classification_rate = "{:.4}".format((num_c/(num_c + num_u))*100)
    sensitivity = "{:.4}".format((num_tp/(num_tp + num_fn + num_fp + num_vp))*100)
    ppv = "{:.4}".format((num_tp/(num_tp + num_fp))*100)
    res_lines.append(f"{args.i}\t{classification_rate}\t{sensitivity}\t{ppv}\n")'''

    with open(os.path.join(args.i, "analysis.txt"), "w") as w1:
        w1.writelines(analysis_lines)  

    print(f"Analysis for {args.i} complete.")

if __name__ == "__main__":
    main()
