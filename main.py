import sys
import json
import time
import os
import subprocess
import gdb
from pycparser import parse_file, c_ast, c_generator, c_parser

def get_type(v: gdb.Value):
    return str(v.type)

def get_value(v: gdb.Value):
    var_type = get_type(v)
    if var_type == "char *" or var_type == "const char *" or var_type.startswith("char ["):
        return v.string()
    return v.cast(gdb.lookup_type(str(v.type)))



class InjectBreakpoint(gdb.Breakpoint):
    def __init__(self, config):
        super(InjectBreakpoint, self).__init__(config['inject_point'], gdb.BP_BREAKPOINT)
        # read & write variables: (variable_name: gdb.Value)
        self.variables = {}
        self.cnt = 0
            
    
    def trigger(self):
        with open(program_path, 'r') as f:
            lines = f.readlines()
        
        with open(program_path, 'w') as f:
            f.write("#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n")
            first = True
            for line in lines:
                print(line)
                if line.strip().startswith("// @read"):
                    variable = line.split("@read")[1].strip()
                    self.variables[variable] = gdb.parse_and_eval(variable)
                    var_type = get_type(self.variables[variable])
                    if 
                    statement = f"{var_type} {variable} = {get_value(self.variables[variable])};\n"
                    if first:
                        first = False
                        statement += f'char buf_{ts}[100];\nFILE* fp_{ts} = fopen("{ts}", "w");\n'
                elif line.strip().startswith("// @write"):
                    variable = line.split("@write")[1].strip()
                    if variable not in self.variables.keys():
                        print("Write a invalid variable")
                        exit()
                    variable_type = get_type(self.variables[variable])
                    if variable_type == "int":
                        statement = f'sprintf(buf_{ts}, "{variable}=%d\\n", {variable});\nfwrite(buf_{ts}, sizeof(char), strlen(buf_{ts}), fp_{ts});\n'
                    else:
                        #todo
                        pass
                elif line.startswith("}"):
                    statement = f'fclose(fp_{ts});\n'+"}"
                else:
                    statement = line
                f.write(statement)
        os.system(f"gcc -shared -fPIC {program_path} -o {program_path}.so")
        gdb.execute(f'print (int)__libc_dlclose((long long)__libc_dlopen_mode("{program_path}.so", 2))')
        with open(str(ts), 'r') as f:
            for line in f:
                gdb.execute(f"print {line}")

                 

    def stop(self):
        # todo meet condition
        self.trigger()
        return True


config_path = "/root/aoptrace/AOP-GDB/config.json"
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)
program_path = config['inject_logic']['program_path']
occurrences = config['inject_logic']['occurrences']

for i in range(occurrences):
    os.system(f'cp {program_path} {program_path+".bak"}')
    ts = int(time.time())
    bp = InjectBreakpoint(config)
    gdb.execute("c")
    os.system(f"rm {program_path} {ts}")
    os.system(f'mv {program_path+".bak"} {program_path}')
    bp.delete()
gdb.execute("detach")


    