#!usr/bin/env python3

import os

def main():
    cwd = os.getcwd()
    res_path = os.path.join(cwd, "results")
    mg = MakefileGenerator("analyse.mk")

    res_dirs = [x for x in os.listdir(res_path) if os.path.isdir(os.path.join(res_path, x))]
    for dir in res_dirs:
        db = os.path.join(res_path, dir)
        tgt = os.path.join(res_path, dir, "analysis.OK")
        dep = ""
        cmd = f"python analyse_kraken_results.py -i {db}"
        mg.add(tgt, dep, cmd)

    mg.write()

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