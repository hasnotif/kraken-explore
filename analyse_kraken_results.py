#!usr/bin/env python3

import os
from ete3 import NCBITaxa

def main():
    cwd = os.getcwd()
    res_path = os.path.join(cwd, "results")
    dataset_path = os.path.join(cwd, "dataset")
    ncbi = NCBITaxa()

    # read in acc2speciesid mapping
    acc2specid_dict = {}
    with open(os.path.join(dataset_path, "iss_50r_viral_acc2speciesid.map"), "r") as r1:
        for line in r1:
            tabs = line.strip("\n").split("\t")
            acc = tabs[0]
            taxid = tabs[1]
            acc2specid_dict[acc] = taxid

    # read in Kraken2 results for each database and perform calculations
    res_dirs = [x for x in os.listdir(res_path) if os.path.isdir(os.path.join(res_path, x))]
    res_lines = []
    header = f"Database\tClassification_Rate\tSensitivity\n"
    res_lines.append(header)
    for dir in res_dirs:
        print(f"Analysing {dir}...", end = " ")
        num_c = 0 # classified
        num_u = 0 # unclassified
        num_tp = 0 # true positive
        num_fp = 0 # false positive
        num_fn = 0 # false negative
        num_vp = 0 # vague positive
        with open(os.path.join(res_path, dir, "results.standard"), "r") as r2:
            for line in r2:
                tabs = line.strip("\n").split("\t")
                # classified reads can be either TP, FP or VP
                if tabs[0] == "C":
                    num_c += 1
                    query_acc = tabs[1].split(".")[0]
                    assigned_taxid = tabs[2]
                    true_taxid = acc2specid_dict[query_acc]
                    # compare assigned_taxid with mapping
                    if assigned_taxid == true_taxid:
                        num_tp += 1
                    elif true_taxid in ncbi.get_lineage(assigned_taxid): # assigned_taxid is a descendant of true_taxid
                        num_tp += 1
                    elif assigned_taxid in ncbi.get_lineage(true_taxid): # assigned_taxid is an ancestor of true_taxid
                        num_vp += 1
                    else: # assigned_taxid is neither a descendant nor an ancestor of true_taxid
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
        ppv = "{:.2%}".format(num_tp/(num_tp + num_fp))
        res_lines.append(f"{dir}\t{classification_rate}\t{sensitivity}\t{ppv}\n")
        print("Done.")

    with open(os.path.join(cwd, "analysis_summary.txt"), "w") as w:
        w.writelines(res_lines)

    print("Analysis complete.")

if __name__ == "__main__":
    main()