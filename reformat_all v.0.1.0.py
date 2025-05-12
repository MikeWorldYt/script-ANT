#!/usr/bin/env python3
import os, sys, time, re
from datetime import datetime
GAP =   "  |   "
GAP_2 = "  |   "

# store src: { prefix, date, breadcrumb, holder, ident } for batch renaming
rename = { "date": False, "breadcrumb": False, "holder": False, "ident": "ID$"}
path='.'
date_pattern = re.compile(r"\(\d{2}-\d{2}(?:-\d{2})?\)")
date_str = datetime.now().strftime("%y-%m-%d")
new_name_date = None
new_name_bread = None
master_index = 0

# Funcion ignorar el propio scrypt
def ignore_scrypt():
    return os.path.basename(__file__)

# Funcion para limpiar la pantalla
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def clear_last_line():
    sys.stdout.write('\033[F')  # move up
    sys.stdout.write('\033[K')  # clear line
    sys.stdout.flush()

def add_date(date_string, target_fname=None):
    global new_name_date, master_index
    ### print(f"DEBUG::: -25 {target_fname} --target_fname --begin add_DATE")
    match = date_pattern.search(target_fname[:10])
    if match:
        new_name_date = target_fname
        master_index += len(match.group(0))
        return
    new_name = f"({date_string}){target_fname}"
    new_name_date = new_name
    master_index += 10
    ### print(f"DEBUG--> -31 {new_name} --modified")
    ### print(f"{GAP} ::: {new_name_date}")

def add_breadcrumb(bread_string, target_fname=None):
    global new_name_bread, master_index
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
        ###print(f"DEBUG--> -50 {processed_name} --modified")
    else:
        processed_name = f"{bread_string}{target_fname}"
    new_name_bread = processed_name
    master_index += len(bread_string)
    ###print(f"{GAP} ::: {new_name_bread}")

def rename_files():
    global new_name_date, new_name_bread, master_index
    script_name = ignore_scrypt()
    formated_name = ""
    ### print(f"DEBUG::: {rename}")
    for fname in os.listdir(path): # Itera sobre cada archivo
        src = os.path.join(path, fname)
        if not os.path.isfile(src) or fname.startswith('~'): # Ignora si es un directorio o si empieza con `~`
            ###print(f"DEBUG::: >> - ! file its a directory or starts with `~`, skipping --continue \n")
            continue
        if fname == script_name: # Skipea el script
            ###print(f"DEBUG::: >> - ! its me, the script, skipping... --continue \n ")
            continue
        print(f"{GAP} <<<  {fname}")
        if isinstance(rename['date'], str):
            add_date(date_string=rename['date'], target_fname=fname)
        # print(f"DEBUG::: >>p {new_name_date} \n{GAP} -   next step")
        if isinstance(rename['date'], bool): # Si es un booleano, no se aplica
            new_name_date = fname
        add_breadcrumb(bread_string=rename['breadcrumb'], target_fname=new_name_date)
        # print(f"DEBUG::: >>p {new_name_bread} \nDEBUG::: >>p master_index = {master_index} \n{GAP} -   next step")
        formated_name = f"~{new_name_bread[:master_index]}[{rename['holder']}]_{rename['ident']}_{new_name_bread[master_index:]}"
        print(f"{GAP} >>> {formated_name} \n{GAP}")
        #
        # dst = os.path.join(path, formated_name)
        # dst = os.rename(src, dst)
        master_index = 0 # reset master_index
    print(f"{GAP}[i] All files renamed.\n")

# Entrada principal - Entry point
# runs all steps in sequence when executed directly
if __name__ == '__main__':
    bp_1 = "\n \n Step 1/4: Do you need date? (y/n)"
    screen = f"\n FORMAT PREVIEW: myFile.jpg {bp_1}" # BP - Step 1
    print(screen)
    while True: # BP - Step 1
        ans = input(f"{GAP}> > > ").strip().lower()
        if ans in ['', 'y', 'n']:
            if ans in ['y', '']:
                clear_screen()
                date_input = input(f"{screen}\n{GAP}Insert a date (Press Enter to use today's date):\n{GAP}> > > ").strip()
                rename["date"] = date_input if date_input else date_str # store applied date
            break
        print(f"{GAP}! INPUT_ERROR_001:  Invalid option or non-existent... Try again ")

    bp_2 = "\n \n Step 2/4: Add the breadcrumb (y/n)" # BP - Step 2
    date = f"({rename['date']})" if isinstance(rename["date"], str) else ""
    und = f"_" if rename["date"] else ""
    clear_screen()
    print(f"\n FORMAT PREVIEW: {date}{und}myFile.jpg {bp_2}") # BP - Step 2
    while True:
        ans = input(f"{GAP}> > > ").strip().lower()
        if ans in ['y', 'n']:
            if ans == 'n':
                print(f"{GAP}Select an option (or press Enter for default \"$na\"):\n{GAP}{GAP_2}1) $na - Not Apply - Not Available\n{GAP}{GAP_2}2) $cx - No Context")
                while True:
                    opt = input(f"{GAP}{GAP_2}> > > ").strip()
                    if not opt:
                        opt = '1'
                    if opt in ['1', '2']:
                        wildcard = '$na' if opt == '1' else '$cx' if opt == '2' else '' 
                        rename["breadcrumb"] = wildcard  # store applied breadcrumb
                        break
                    else:
                        # error: no selecciono en ruta `n`
                        print(f"{GAP}{GAP_2}! INPUT_ERROR_001:  Invalid option or non-existent... Try again ")
                break
            else:
                custom = input(f"{GAP}{GAP_2}Enter your breadcrumb (or press Enter to use the current folder name):\n{GAP}{GAP_2}> > > ").strip()
                rename["breadcrumb"] = custom if custom else os.path.basename(os.getcwd())
                break
        else:
            print(f"{GAP}! INPUT_ERROR_001:  Invalid option or non-existent... Try again ")

    bp_3 = "\n \n Step 3/4: Add a Holder"
    clear_screen()
    print(f"\n FORMAT PREVIEW: {date}{rename['breadcrumb']}_myFile.jpg {bp_3}") # BP - Step 3
    holder_input = input(f"{GAP}Insert your holder name (or press Enter to choose a predefined option):\n{GAP}> > > ").strip()
    if holder_input:
        rename["holder"] = holder_input
    else:
        print(f"{GAP}Select an option (or press Enter for default \"$uk\"):\n{GAP}{GAP_2}1) $uk - Unknown\n{GAP}{GAP_2}2) $up - Unidentified person\n{GAP}{GAP_2}3) $uc - Unidentified character")
        while True:
            opt = input(f"{GAP}{GAP_2}> > > ").strip()
            if not opt:
                opt = '1'
            if opt in ['1', '2', '3']:
                wildcard = '$uk' if opt == '1' else '$up' if opt == '2' else '$uc'
                rename["holder"] = wildcard
                break
            else:
                print(f"{GAP}{GAP_2}! INPUT_ERROR_001:  Invalid option or non-existent... Try again.")

    bp_4 = "\n \n Step 4/4: Enter a identifier code (or press Enter for default \"$ID\"):"
    clear_screen()
    print(f"\n FORMAT PREVIEW: {date}{rename['breadcrumb']}[{rename['holder']}]_myFile.jpg {bp_4}") # BP - Step 4
    while True: 
        custom_id = input(f"{GAP}> > > ").strip()
        if not custom_id:
            identifier = '$ID'
        elif custom_id.isalpha() and len(custom_id) == 3:
            identifier = custom_id.upper()
        else:
            print(f"{GAP}! INPUT_ERROR_002_n3:  Invalid input; only allows alphabetic characters (no numbers or symbols), must be exactly 3 characters... Try again ")
            continue
        # Confirmation
        print(f"{GAP}\n CONFIRMATION: The ID to be formatted is: {identifier}\n \"ok\" or press Enter to continue - \"c\" to cancel:")
        while True:
            confirm = input(f" > > > ").strip().lower()
            if confirm in ['', 'ok']:  # continuar
                clear_screen()
                rename["ident"] = identifier
                break
            elif confirm == 'c':
                print(f"\n Operation cancelled. One second please...")
                time.sleep(2)
                clear_screen()
                print(f"\n FORMAT PREVIEW: {date}{rename['breadcrumb']}[{rename['holder']}]_myFile.jpg{bp_4}")
                break
            else:
                print(f"{GAP}! INPUT_ERROR_001:  Invalid option or non-existent... Try again")
        if confirm in ['', 'ok']:
            break

    # Final confirmation
    fp = "\n \n ATTENTION: Ckeck the format preview before applying the changes.\n Once confirmed, the script will rename the files to the requested format, there no return.\n \"ok\" to confirm - \"c\" to cancel: "
    preview = (f"\n FORMAT PREVIEW: {date}{rename['breadcrumb']}[{rename['holder']}]_{identifier}_myFile.jpg {fp}") # BP - Step 5
    while True:
        confirm = input(f"{preview}\n > > > ").strip().lower()
        if confirm in ['y', 'ok']:  # continuar
            clear_screen()
            print(f"{preview} \n Applying changes...") # BP - Final Step
            time.sleep(1)
            rename_files()
            break
        elif confirm == 'c':
            clear_screen()
            print(f"\n FORMAT PREVIEW: {date}{rename['breadcrumb']}[{rename['holder']}]_{identifier}_myFile.jpg{fp}")
            print(f"\n Operation cancelled.")
            break
        else:
            clear_screen()

    # Ending process
    print()
    time_close = 500

    for time_close in range(time_close, 0, -1):
        print(f"\r ▲ Its done, You don't have to close this window, it will close by itself. Time remaining ({time_close} seg)", end="")
        time.sleep(1)
