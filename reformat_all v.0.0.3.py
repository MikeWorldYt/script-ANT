#!/usr/bin/env python3
import os
import re
from datetime import datetime
import time
GAP = "        "
breadcrumb = None
holder = None

# Funcion ignorar el propio scrypt
def ignore_scrypt(path='.'):
    return os.path.basename(__file__)

def add_prefix(path='.'):  # Step 1
    script_name = ignore_scrypt()
    # Primera pasada: Agrega solo el prefijo ~ en el indice 0
    for fname in os.listdir(path):
        if fname == script_name:
            continue
        src = os.path.join(path, fname)
        if not os.path.isfile(src) or fname.startswith('~'):
            continue
        new_name = f"~{fname}"
        dst = os.path.join(path, new_name)
        print(f"Adding prefix: {fname} -> {new_name}")
        os.rename(src, dst)
    print(f"{GAP}Prefix review formated.")
    print("")

def add_date(path='.'): # Step 2
    script_name = ignore_scrypt()
    # Segunda pasada: Formatear fecha si se necesita YY-MM-DD
    date_str = datetime.now().strftime("%y-%m-%d")
    # Patron para detectar si ya existe una fecha entre parentesis como (27-01-05) o (27-01)
    date_pattern = re.compile(r'\(\d{2}-\d{2}(?:-\d{2})?\)')

    # iteration para agregar fecha
    for fname in os.listdir(path):
        if fname == script_name:
            continue
        src = os.path.join(path, fname)
        # Ignoramos si el archivo ya tiene fecha
        if not os.path.isfile(src):
            continue
        if date_pattern.search(fname):
            continue
        new_name = f"~({date_str}){fname[1:]}"  # Inserta fecha despues del indice 1
        dst = os.path.join(path, new_name)
        
        os.rename(src, dst)
    print(f"{GAP}Date Formated")

def add_breadcrumb(path='.', wildcard='na$'): # Step 3
    script_name = ignore_scrypt()
    max_index = 11

    for fname in os.listdir(path):
        if fname == script_name:
            continue
        src = os.path.join(path, fname)
        if not os.path.isfile(src):
            continue

        insert_index = None
        idx_paren = fname.find(')', 0, max_index)
        if idx_paren != -1:
            insert_index = idx_paren + 1
        elif fname.startswith('~'):
            insert_index = 1

        if insert_index is not None:
            new_name = fname[:insert_index] + wildcard + fname[insert_index:]
            dst = os.path.join(path, new_name)
            os.rename(src, dst)
    print(f"{GAP}Breadcrumbing formated.")

def add_holder(path='.', holder_label='[uk$]'):  # Step 4
    script_name = ignore_scrypt()
    for fname in os.listdir(path):
        if fname == script_name:
            continue
        src = os.path.join(path, fname)
        if not os.path.isfile(src):
            continue

        insert_index = None
        idx_paren = fname.find(breadcrumb)
        if idx_paren != -1:
            insert_index = idx_paren + len(breadcrumb)
        
        if insert_index is not None:
            new_name = fname[:insert_index] + holder_label + '_' + fname[insert_index:]
            dst = os.path.join(path, new_name)
            os.rename(src, dst)
    print(f"{GAP}Holder added.")

# Entrada principal - Entry point
# runs all steps in sequence when executed directly
if __name__ == '__main__':
    print("Step 1: Prefixing all files with ~")
    add_prefix()
    time.sleep(1)

    while True:
        ans = input("Step 2: Do you need date? (y/n): ").strip().lower()
        if ans in ['y', 'n']:
            if ans == 'y':
                print(f"\r{GAP}Adding date, Please wait...")
                add_date()
            else:
                print()
            break
        print("  < ! INPUT_ERROR_001:  Invalid option or non-existent. >\n  Try again ...")

    while True:
        ans = input("Step 3: Will you add the breadcrumb now? (y/n): ").strip().lower()
        if ans in ['y', 'n']:
            if ans == 'n':
                opt = input(f"{GAP}Select an option:\n{GAP}1) na$ - Not Available\n{GAP}2) cx$ - No Context\n{GAP}3) nn$ - No Name\n{GAP}> ").strip()
                wildcard = 'na$' if opt == '1' else 'cx$' if opt == '2' else 'nn$'
            else:
                opt = input(f"{GAP}Select an option:\n{GAP}1) Use current folder name\n{GAP}2) Enter a custom name\n{GAP}> ").strip()
                if opt == '1':
                    wildcard = os.path.basename(os.getcwd())
                else:
                    wildcard = input("Enter your custom breadcrumb name: ").strip()
            add_breadcrumb(wildcard=wildcard)
            breadcrumb = wildcard  # Salvar el nombre del breadcrumb para usarlo en el paso 4
            break
        print("  < ! INPUT_ERROR_001:  Invalid option or non-existent. >\n  Try again ...")

    while True:
        ans = input("Step 4: Will you add a holder? (y/n): ").strip().lower()
        if ans in ['y', 'n']:
            if ans == 'n':
                opt = input(f"{GAP}Select an option:\n{GAP}1) uk$ - Unknown\n{GAP}2) up$ - Unidentified person\n{GAP}3) uc$ - Unidentified character\n{GAP}> ").strip()
                holder = '[uk$]' if opt == '1' else '[up$]' if opt == '2' else '[uc$]'
            else:
                custom_holder = input("Enter custom holder name: ").strip()
                holder = f"[{custom_holder}]"
            add_holder(holder_label=holder)
            holder = custom_holder # Salvar el nombre del holder para usarlo en el paso 5
            break
        print("  < ! INPUT_ERROR_001:  Invalid option or non-existent. >\n  Try again ...")

    # Ending process
    print()
    time_close = 50

    for time_close in range(time_close, 0, -1):
        print(f"\r▲ Its done, You don't have to close this window, it will close by itself. Time remaining ({time_close} seg)", end="")
        time.sleep(1)

