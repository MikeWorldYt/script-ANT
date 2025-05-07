#!/usr/bin/env python3
import os
import re
from datetime import datetime
import time
GAP =   "  |     "
GAP_2 = "  |   "
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
        os.rename(src, dst)
    print(f"{GAP}[i] Prefix review formated.\n")

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
    print(f"{GAP}[i] Date Formated.\n")

def add_breadcrumb(path='.', wildcard='na$'): # Step 3
    script_name = ignore_scrypt()
    max_index = 11
    # Tercera pasada: Agregar breadcrumbing
    for fname in os.listdir(path):
        if fname == script_name:
            continue
        src = os.path.join(path, fname)
        if not os.path.isfile(src):
            continue
    # Buscar dentro del indice 0 al 11 si existe el )
        insert_index = None
        idx_paren = fname.find(')', 0, max_index)
        if idx_paren != -1:
            insert_index = idx_paren + 1
        # si no existe, buscar si empieza con el ~
        elif fname.startswith('~'):
            insert_index = 1
        # cuando `insert_index` tiene un valor, insertara el breadcrumb
        if insert_index is not None:
            new_name = fname[:insert_index] + wildcard + fname[insert_index:]
            dst = os.path.join(path, new_name)
            os.rename(src, dst)
    print(f"{GAP}[i] Breadcrumbing formated.\n")

def add_holder(path='.', holder_label='[uk$]'):  # Step 4
    script_name = ignore_scrypt()
    # Cuarta pasada: Agregar holder
    for fname in os.listdir(path):
        if fname == script_name:
            continue
        src = os.path.join(path, fname)
        if not os.path.isfile(src):
            continue
        # Buscar dentro del nombre que haga match con el breadcrumb
        insert_index = None
        idx_paren = fname.find(breadcrumb)
        if idx_paren != -1:
            insert_index = idx_paren + len(breadcrumb)
        # cuando `insert_index` tiene un valor, insertara el holder_label y un _
        if insert_index is not None:
            new_name = fname[:insert_index] + holder_label + '_' + fname[insert_index:]
            dst = os.path.join(path, new_name)
            os.rename(src, dst)
    print(f"{GAP}[i] Holder formated.\n")

def add_identifier(path='.', ident='ID$'): # Step 5
    script_name = ignore_scrypt()
    # Quinta pasada: Agregar el ID
    for fname in os.listdir(path):
        if fname == script_name:
            continue
        src = os.path.join(path, fname)
        if not os.path.isfile(src):
            continue
    # Buscar dentro del nombre que haga match con el holder
        idx_holder = fname.find(holder)
        # cuando `idx_holder` tiene un valor, insertara el ident...ificator y un _
        if idx_holder != -1:
            insert_index = idx_holder + len(holder)
            new_name = fname[:insert_index] + ident + fname[insert_index:]
            dst = os.path.join(path, new_name)
            os.rename(src, dst)
    print(f"{GAP}[i] Identifier formated.")

# Entrada principal - Entry point
# runs all steps in sequence when executed directly
if __name__ == '__main__':
    print("Step 1: Prefixing all files with ~")
    add_prefix()
    time.sleep(1)

    print(f"Step 2: Do you need date? (y/n)") # BP - Step 2
    while True: # BP - Step 2
        ans = input(f"{GAP}> > > ").strip().lower()
        if ans in ['y', 'n']:
            if ans == 'y':
                # print(f"\r{GAP}Adding date, Please wait...")
                add_date()
            else:
                print()
            break
        print(f"  | ! INPUT_ERROR_001:  Invalid option or non-existent. \n{GAP}Try again ...")

    print(f"Step 3: Will you add the breadcrumb now? (y/n)") # BP - Step 3
    while True:
        ans = input(f"{GAP}> > > ").strip().lower()
        if ans in ['y', 'n']:
            if ans == 'n':
                print(f"{GAP}Select an option:\n{GAP}{GAP_2}1) na$ - Not Available\n{GAP}{GAP_2}2) cx$ - No Context\n{GAP}{GAP_2}3) nn$ - No Name")
                while True:
                    opt = input(f"{GAP}> > > ").strip()
                    if opt in ['1', '2', '3']:
                        wildcard = 'na$' if opt == '1' else 'cx$' if opt == '2' else 'nn$'
                        add_breadcrumb(wildcard=wildcard)
                        breadcrumb = wildcard
                        break
                    else:
                        # error: no selecciono en ruta `n`
                        print(f"  | ! INPUT_ERROR_001:  Invalid option or non-existent. \n{GAP}Try again ...")
                break
            else:
                print(f"{GAP}Select an option:\n{GAP}{GAP_2}1) Use current folder name\n{GAP}{GAP_2}2) Enter a custom name")
                while True:
                    opt = input(f"{GAP}> > > ").strip()
                    if opt == '1':
                        wildcard = os.path.basename(os.getcwd())
                        add_breadcrumb(wildcard=wildcard)
                        breadcrumb = wildcard
                        break
                    elif opt == '2':
                        wildcard = input(f"{GAP}Enter your custom breadcrumb name:\n{GAP}> > > ").strip()
                        add_breadcrumb(wildcard=wildcard)
                        breadcrumb = wildcard
                        break
                    else:
                        # error: no selecciono en ruta `y`
                        print(f"  | ! INPUT_ERROR_001:  Invalid option or non-existent. \n{GAP}Try again ...")
                break
        else:
            print(f"  | ! INPUT_ERROR_001:  Invalid option or non-existent. \n{GAP}Try again ... ")

    print(f"Step 4: Will you add a holder? (y/n)") # BP - Step 4
    while True:
        ans = input(f"{GAP}> > > ").strip().lower()
        if ans in ['y', 'n']:
            if ans == 'n':
                opt = input(f"{GAP}Select an option:\n{GAP}{GAP_2}1) uk$ - Unknown\n{GAP}{GAP_2}2) up$ - Unidentified person\n{GAP}{GAP_2}3) uc$ - Unidentified character\n{GAP}> > > ").strip()
                holder = '[uk$]' if opt == '1' else '[up$]' if opt == '2' else '[uc$]'
            else:
                custom_holder = input(f"{GAP}Enter custom holder name:\n{GAP}> > > ").strip()
                holder = f"[{custom_holder}]"
            add_holder(holder_label=holder)
            holder = f"[{custom_holder}]_" # Salvar el nombre del holder para usarlo en el paso 5
            break
        print(f"  | ! INPUT_ERROR_001:  Invalid option or non-existent. \n{GAP}Try again ... ")

    print(f"Step 5: Enter a identifier code (or press Enter for default ID$):") # BP - Step 5
    while True: 
        custom_id = input(f"{GAP}> > > ").strip()
        if not custom_id:
            identifier = 'ID$'
        elif custom_id.isalpha() and len(custom_id) == 3:
            identifier = custom_id.upper() + '_keywords'
        else:
            print(f"  | ! INPUT_ERROR_002_n3:  Invalid input; only allows alphabetic characters (no numbers or symbols), must be exactly 3 characters. \n{GAP}Try again ... ")
            continue

        confirm = input(f"{GAP}Are you sure you want to continue? (The ID to be formatted is: {identifier}) (y/n):\n{GAP}> > > ").strip().lower()
        if confirm == 'y':
            break
        else:
            print(f"  | ! INPUT_ERROR_002_n3:  Invalid input; only allows alphabetic characters (no numbers or symbols), must be exactly 3 characters. \n{GAP}Try again ... ")
    add_identifier(ident=identifier)

    # Ending process
    print()
    time_close = 50

    for time_close in range(time_close, 0, -1):
        print(f"\r▲ Its done, You don't have to close this window, it will close by itself. Time remaining ({time_close} seg)", end="")
        time.sleep(1)

