#!/usr/bin/env python3
import os
import re
from datetime import datetime
import time
GAP =   "  |     "
GAP_2 = "  |   "

# store src: { prefix, date, breadcrumb, holder, ident } for batch renaming
rename = { "prefix": "~", "date": False, "breadcrumb": False, "holder": False, "ident": "ID$"}
path='.'
date_pattern = re.compile(r"\(\d{2}-\d{2}(?:-\d{2})?\)")
date_str = datetime.now().strftime("%y-%m-%d")
new_name_date = None
new_name_bread = None
holder = None

# Funcion ignorar el propio scrypt
def ignore_scrypt():
    return os.path.basename(__file__)

def add_date(date_string, target_fname=None):
    global new_name_date
    ### print(f"DEBUG::: -25 {target_fname} --target_fname --begin add_DATE")
    if date_pattern.search(target_fname[:10]):
        new_name_date = target_fname
        return
    new_name = f"({date_string}){target_fname}"
    new_name_date = new_name
    print(f"DEBUG--> -31 {new_name} --modified")
    ### print(f"{GAP} ::: {new_name_date}")

def add_breadcrumb(bread_string, target_fname=None):
    global new_name_bread
    processed_name = ""
    # print(f"DEBUG::: -40 {target_fname} --target_fname --begin add_BREADCRUMB")
    if target_fname is None:
        processed_name = bread_string
        new_name_bread = processed_name
        return
    match = date_pattern.search(target_fname[:10])
    if match:
        insert_index = match.end()
        processed_name = f"{target_fname[:insert_index]}{bread_string}{target_fname[insert_index:]}"
        print(f"DEBUG--> -50 {processed_name} --modified")
    else:
        processed_name = f"{bread_string}{target_fname}"
    new_name_bread = processed_name
    ###print(f"{GAP} ::: {new_name_bread}")

def add_holder(path=path, holder_label='[uk$]'):  # Step 4
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
        idx_paren = fname.find(rename['breadcrumb'])
        if idx_paren != -1:
            insert_index = idx_paren + len(rename['breadcrumb'])
        # cuando `insert_index` tiene un valor, insertara el holder_label y un _
        if insert_index is not None:
            new_name = fname[:insert_index] + holder_label + '_' + fname[insert_index:]
            #dst = os.path.join(path, new_name)
            #dst = os.rename(src, dst)
        rename["holder"] = holder_label  # store applied holder
    print(f"{GAP}[i] Holder formated.\n")
    print(f"{GAP} {rename}")

def add_identifier(path=path, ident='ID$'): # Step 5
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
            #dst = os.path.join(path, new_name)
            #dst = os.rename(src, dst)
        rename["ident"] = ident  # store applied identifier
    print(f"{GAP}[i] Identifier formated.")

def rename_files():
    global new_name_date, new_name_bread
    script_name = ignore_scrypt()
    # print(f"DEBUG::: 114 ~({rename['date']}){rename['breadcrumb']}[{rename['holder']}]_{rename['ident']}_keywords ")
    formated_name = f"~{add_date}{rename['breadcrumb']}[{rename['holder']}]_{rename['ident']}_keywords"
    # print(f"DEBUG::: 116 {formated_name}")
    print(f"DEBUG::: {rename}")
    for fname in os.listdir(path): # Itera sobre cada archivo
        src = os.path.join(path, fname)
        print(f"DEBUG::: <<< {fname} --take the file name")
        if not os.path.isfile(src) or fname.startswith('~'): # Ignora si es un directorio o si empieza con `~`
            print(f"DEBUG::: >> - ! file its a directory or starts with `~`, skipping --continue \n")
            continue
        if fname == script_name: # Skipea el script
            print(f"DEBUG::: >> - ! its me, the script, skipping... --continue \n ")
            continue
        if isinstance(rename['date'], str):
            add_date(date_string=rename['date'], path=path, target_fname=fname)
        # print(f"DEBUG::: >>p {new_name_date} \n{GAP} -   next step")
        if isinstance(rename['date'], bool): # Si es un booleano, no se aplica
            new_name_date = fname
        if isinstance(rename['breadcrumb'], str):
            add_breadcrumb(bread_string=rename['breadcrumb'], path=path, target_fname=new_name_date)
        print(f"DEBUG::: >>p {new_name_bread} \n{GAP} -   next step")

        print(f"{GAP} >>> {fname} -> {new_name_bread} \n")
    print(f"DEBUG::: 131 {new_name_date}")
    print(f"DEBUG::: {fname}")

        # new_name = f"{formated_name}{fname}"
        # dst = os.path.join(path, new_name)
        # dst = os.rename(src, dst)
        # print(f"{GAP}Renamed: {src} -> {dst}")
    print(f"{GAP}[i] All files renamed.\n")

# Entrada principal - Entry point
# runs all steps in sequence when executed directly
if __name__ == '__main__':
    print(f"DEBUG::: {rename}")

    print(f"Step 2: Do you need date? (y/n)") # BP - Step 2
    while True: # BP - Step 2
        ans = input(f"{GAP}> > > ").strip().lower()
        if ans in ['y', 'n']:
            if ans == 'y':
                rename["date"] = date_str  # store applied date
            else:
                print("")
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
                        rename["breadcrumb"] = wildcard  # store applied breadcrumb
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
                        rename["breadcrumb"] = wildcard  # store applied breadcrumb
                        break
                    elif opt == '2':
                        wildcard = input(f"{GAP}Enter your custom breadcrumb name:\n{GAP}> > > ").strip()
                        rename["breadcrumb"] = wildcard  # store applied breadcrumb
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
                holder = 'uk$' if opt == '1' else 'up$' if opt == '2' else 'uc$'
            else:
                custom_holder = input(f"{GAP}Enter custom holder name:\n{GAP}> > > ").strip()
                holder = custom_holder
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

    print("------------------------------------------")
    print(f"Applying changes...") # BP - Final Step
    rename_files()

time.sleep(50000000)
#    # Ending process
#    print()
#    time_close = 50
#
#    for time_close in range(time_close, 0, -1):
#        print(f"\r▲ Its done, You don't have to close this window, it will close by itself. Time remaining ({time_close} seg)", end="")
#        time.sleep(1)

