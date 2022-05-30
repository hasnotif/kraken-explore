#!usr/bin/env python3

import os
import shutil

def main():
    cwd = os.getcwd()
    db_path = os.path.join(cwd, "db")
    dataset_path = os.path.join(cwd, "dataset")
    res_path = os.path.join(cwd, "results")

    # get list of database directories
    db_dirs = [x for x in os.listdir(db_path) if os.path.isdir(os.path.join(db_path, x))]
    db_dirs.remove("base")
    
    # generate Makefile
    mg = MakefileGenerator("run_kraken.mk")
    ds1 = os.path.join(dataset_path, "iss_50r_viral_R1.fastq")
    ds2 = os.path.join(dataset_path, "iss_50r_viral_R2.fastq")
    for dir in db_dirs:
        d = os.path.join(db_path, dir)
        p = os.path.join(res_path, f"{dir}_results")
        r = os.path.join(p, "results.standard")
        os.mkdir(p)
        shutil.copy(os.path.join(d, "params.txt"), os.path.join(p, "params.txt"))
        tgt = p + ".OK"
        dep = ""
        cmd = f"kraken2 --db {d} --threads 12 --paired {ds1} {ds2} > {r}"
        mg.add(tgt, dep, cmd)
    mg.write()

    print("Done")

class MakefileGenerator(object):
    def __init__(self, makefile):
        self.makefile = makefile
        self.tgts = []
        self.deps = []
        self.cmds = []

    def add(self, tgt, dep, cmd):
        self.tgts.append(tgt)
        self.deps.append(dep)
        self.cmds.append(cmd)

    def print(self):
        print('.DELETE_ON_ERROR:')
        for i in range(len(self.tgts)):
            print(f'{self.tgts[i]} : {self.deps[i]}')
            print(f'\t{self.cmds[i]}')
            print(f'\ttouch {self.tgts[i]}')

    def write(self):
        with open(self.makefile, 'w') as f:
            f.write(f".DELETE_ON_ERROR:")
            f.write("\n\n")
            f.write("all : ") 
            for tgt in self.tgts:
                f.write(f'{tgt} ')
            f.write("\n\n")

            for i in range(len(self.tgts)):
                f.write(f'{self.tgts[i]} : {self.deps[i]}\n')
                f.write(f'\t{self.cmds[i]}\n')
                f.write(f'\ttouch {self.tgts[i]}\n\n')
    
if __name__ == "__main__":
    main()