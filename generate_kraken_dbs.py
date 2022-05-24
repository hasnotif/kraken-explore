#!usr/bin/env python3

import os
import shutil

def main():
    cwd = os.getcwd() # assuming inside kraken2_explore/db
    
    # minimiser lengths to test
    ls = [31, 29, 33]

    # generate Makefile
    mg = MakefileGenerator("build_dbs.mk")

    # create database directories and copy identical items from base database
    for l in ls:
        ks = []
        for i in range(l, l+11):
            ks.append(i)
        for k in ks:
            db_path = f"viral_k{k}_l{l}"
            shutil.copytree(os.path.join(cwd, "base"), os.path.join(cwd, db_path))
            tgt = f"{db_path}.OK"
            dep = ""
            cmd = f"kraken2-build --build --db {db_path} --kmer-len {k} --minimizer-len {l} --threads 12"
            mg.add(tgt, dep, cmd)

    # write Makefile
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
