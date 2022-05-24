#!usr/bin/env python3

from ete3 import NCBITaxa

def main():
    ncbi = NCBITaxa()
    
    with open("iss_50r_viral_acc2taxid.map", "r") as r:
        new_lines = []
        for line in r:
            tabs = line.strip("\n").split("\t")
            acc, taxid = tabs[0], tabs[1]
            rank = (ncbi.get_rank([taxid]))[int(taxid)]
            # if taxid is not at species level, push it up to species level:
            if rank != "species":
                lineage = ncbi.get_lineage(taxid)
                for id in lineage:
                    if (ncbi.get_rank([id]))[int(id)] == "species":
                        taxid = id
            new_lines.append(f"{acc}    {taxid}\n")

    with open("iss_50r_viral_acc2speciesid.map", "w") as w:
        w.writelines(new_lines)

if __name__ == "__main__":
    main()
