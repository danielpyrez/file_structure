import os
import sys
import re
import glob
from colorama import Fore, Style

#======TREE=======#
from rich.tree import Tree
from rich.console import Console
#=================#

class StructureError(Exception):
    def __init__(self, errormsg):
        self.error = str(errormsg)
    def __str__(self):
        return "\n" + self.error

#====================(CONTENT WRITTING VARIABLES)=====================#

start_filling = '*/start'
write_text = start_filling + 'write'
write_byte = start_filling + 'byte'
end_filling = '*/end'
writting = False

no_reverse = False

#=====================================================================#

def colored(text: str, color: str):
    try:
        return Style.BRIGHT + getattr(Fore, color.upper()) + text + Style.RESET_ALL
    except:
        raise ValueError(f"Color '{color}' not recognized by colorama, use RGB/CMY")

#=====================================================================#

console = Console()

def preview(files: list, name: str = "Main Directory"):
    tree = Tree(colored(f"\n{name}", 'magenta'))
    cont = False
    stack = [tree]

    for line in files:
        if not cont:
            if line.startswith('#') or line.isspace() or writting:
                continue
            if ':' in line:
                name = colored(line.strip().split(':')[0], 'green')
            else:
                name = colored(line.strip().split(':')[0], 'cyan')
            depth = line.count('\t')

            stack = stack[:depth+1]

            parent = stack[-1]
            new_node = parent.add(name)
            stack.append(new_node)
            if start_filling in line:
                cont = True
        else:
            if end_filling in line:
                cont = False

    console.print(tree)
    print()
      
#=====================================================================#

try:
    main_file_location = os.getcwd()
    tab_count = 0
    line_count = 0
    last_count = 0
    last_dir = ''

#=========================(SEARCH STRU FILE)============================#
    
    if len(sys.argv) > 1:
        stru_file = sys.argv[1]
    else:
        s_files = glob.glob("*.stru")
        if not s_files:
            raise StructureError("Failed to find structure file (*.stru)")
        if len(s_files) > 1:
            print(colored("Many Structure files have been found.\nPlease select one:\n", 'cyan'))
            while True:
                for file in s_files:
                    print(f"\t{int(s_files.index(file))+1}) {file}\n")
                try:
                    selection = int(input("> "))
                    if (selection) <= len(s_files):
                        stru_file = s_files[selection-1]
                        os.system('cls')
                        break
                    else:
                        raise ValueError
                except ValueError:
                    os.system('cls')
                    print(colored("Invalid option, try again.\nPlease select one:\n", 'red'))
        else:
            stru_file = s_files[0]

#=====================================================================#

    with open(stru_file,'r',encoding = 'utf-8') as f:
        lines = f.readlines()
        preview(lines)
        directory = input(colored("Name of the Main Directory: ", 'magenta'))
        if directory == '.' or directory == '..':
            os.chdir(directory)
        else:
            os.makedirs(directory)
            os.chdir(directory)
        os.system('cls')
        while True:
            preview(lines,os.getcwd()+"\\")
            ask_sure = input(f"Are you sure you want to do this? [y/n]: ")
            if ask_sure.lower().startswith('y'):
                os.system('cls')
                break
            else:
                input("No changes will be applied. Press enter to exit. . .")
                exit()
        while lines[0] == '\n':
            del lines[0]
        if lines[0].startswith('#!structure'):
            for line in lines:
                line_count += 1
                if not writting:
                    if line.strip().startswith('#') or line.isspace() and not writting:
                        continue
                    file = line.replace('\n','')
                    file_name = file.replace('\t','')
                    tab_count = file.count('\t')
                    try:
                        if tab_count == last_count +1:
                            os.chdir(last_dir)
                        elif tab_count < last_count:
                            os.chdir(f'..'+'/..' * (last_count - tab_count - 1))
                        elif tab_count > last_count:
                            raise Exception

                        if ':' in file_name:
                            match = re.match(r"^([\w.]+)\.(\w+):\s*(.+)$", file_name)
                            empty_file = re.match(r"^([\w.]+)\.(\w+):$", file_name)
                            if match:
                                with open(f'{match.group(1)}.{match.group(2)}','wt',encoding = 'utf-8') as f:
                                    content = match.group(3)
                                    if content.startswith(start_filling):
                                        writting_file = f'{match.group(1)}.{match.group(2)}'
                                        writting = True
                                    else:
                                        f.write(content)
                            elif empty_file:
                                ef = open(f'{empty_file.group(1)}.{empty_file.group(2)}','x', encoding='utf-8')
                                ef.close()
                        else:
                            os.mkdir(file_name)
                        last_count = tab_count
                        last_dir = file_name
                    except:
                        raise StructureError(f"Unexpected format in '{stru_file}': Line {line_count} -> '{file_name}'")
                else:
                    try:
                        if line.strip() == end_filling:
                            writting = False
                        else:
                            if content.startswith(write_text):
                                with open(writting_file, 'a', encoding='utf-8') as wf:
                                    wf.write('\n' if line.isspace() else line)
                            elif content.startswith(write_byte):
                                with open(writting_file, 'ab') as wf:
                                    wf.write(eval(f"b'{line.strip()}'"))
                            else:
                                raise Exception
                    except:
                        raise StructureError(f"An exception ocurred while writting '{writting_file}': {stru_file} Line {line_count} -> '{line.replace('\n','').replace('\t','')}'")
        else:
            no_reverse = True
            raise StructureError("Invalid structure file. Expected '#!structure' at the start of the file")
    
    input(colored("Success! Press Enter to exit. . .", "green"))

except Exception as e:
    input(f'{str(e)} \nPress Enter to reverse changes. . .')
    if not no_reverse:
        try:
            reverse = os.path.join(main_file_location, directory)
            os.chdir(reverse)
            if os.path.exists(reverse):
                for root, dirs, files in os.walk(reverse, topdown=False):
                    for file in files:
                        try:
                            os.remove(os.path.join(root, file))
                        except: pass
                    for dir in dirs:
                        try:
                            os.rmdir(os.path.join(root, dir))
                        except: pass
                try:
                    os.chdir(main_file_location)
                    os.rmdir(reverse)
                except: pass
        except: pass
