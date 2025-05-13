#!/usr/bin/env python3
import os, sys, time, re
from datetime import datetime
GAP = "  │   "
SEL = "  └──── ▼  "
ASK = "  └── > > > "


STORE_TEMPLATE = { "date": False, "breadcrumb": False, "holder": False, "ident": ""}
store = STORE_TEMPLATE.copy()
path='.'
date_pattern = re.compile(r"\(\d{2}-\d{2}(?:-\d{2})?\)")
date_str = datetime.now().strftime("%y-%m-%d")
new_name_date = None
new_name_bread = None
master_index = 0

def ignore_scrypt(): # Funcion ignorar el propio scrypt
    return os.path.basename(__file__)

def clear_screen(): # Funcion para limpiar la pantalla
    os.system('cls' if os.name == 'nt' else 'clear')

def format_date_input(raw): # Funcion p formatatear la fecha
    raw = raw.strip().replace('/', '-').replace(' ', '-').replace('.', '-')
    if any(c.isalpha() for c in raw):
        return None
    parts = raw.split('-')
    parts = [p.zfill(2) for p in parts if p]
    if len(parts) == 2:      # MM-DD
        return f"{parts[0]}-{parts[1]}"
    elif len(parts) == 3:    # YY-MM-DD
        return f"{parts[0]}-{parts[1]}-{parts[2]}"
    else:
        return None

def add_date(date_string, target_fname=None):
    global new_name_date, master_index
   # print(f"DEBUG::: -24 {target_fname} --target_fname --begin add_DATE")
    match = date_pattern.search(target_fname[:10])
    if match: # Si ya existe una fecha, dejala como esta
        new_name_date = target_fname
        master_index += len(match.group(0))
        return
    new_name = f"({date_string}){target_fname}"
    new_name_date = new_name
    master_index += len(f"({date_string})")
    print(f"{GAP}  ->  {new_name_date} --modified")

def add_breadcrumb(bread_string, target_fname=None):
    global new_name_bread, master_index
    processed_name = ""
   # print(f"DEBUG::: -38 {target_fname} --target_fname --begin add_BREADCRUMB")
    match = date_pattern.search(target_fname[:10])
    if match: # Si ya tiene una fecha, insertala luego ella
        insert_index = match.end()
        processed_name = f"{target_fname[:insert_index]}{bread_string}{target_fname[insert_index:]}"
    else: # Si no tiene fecha, insertala al principio
        processed_name = f"{bread_string}{target_fname}"
    new_name_bread = processed_name
    master_index += len(bread_string)
    print(f"{GAP}  ->  {new_name_bread} --modified")

def run_survey():
    global store
    def render_preview(filename="myFile.jpg"):
        date = f"({store['date']})" if isinstance(store["date"], str) else ""
        breadcrumb = store["breadcrumb"] or ""
        holder = f"[{store['holder']}]" if store["holder"] else ""
        ident = f"_{store['ident']}" if store["ident"] else ""
        prefix = "".join([date, breadcrumb, holder, ident])
        return f"\n PREVIEW FORMAT: {prefix}_{filename}" if prefix else f"\n PREVIEW FORMAT: {filename}"
    # BP - Step 1
    bp_1 = "\n \n Step 1/4: Do you need date?"
    screen = f"{render_preview()} {bp_1}"
    print(f"{screen} y/n")
    while True: # BP - Step 1
        ans = input(f"{ASK}").strip().lower()
        if ans in ['', 'y', 'n']:
            if ans in ['y', '']:
                clear_screen()
                print(f"{screen} → Yes → [ Editing... ] \n{GAP}Insert a date (Press Enter to use today's date):")
                while True:
                    date_input = input(f"{ASK}").strip()
                    if not date_input:
                        store["date"] = date_str
                        break
                    formatted = format_date_input(date_input)
                    if not formatted:
                        print(f"{GAP}( ! ) INPUT_ERROR: Invalid format. Use YY-MM-DD or MM-DD only (numbers only).")
                        continue
                    store["date"] = formatted
                    break
                break
            elif ans == 'n':
                store["date"] = False
                break
        print(f"{GAP}( ! ) INPUT_ERROR_001:  Invalid option. Use \"y\" to Yes or \"n\" to No. ")
    clear_screen(), print(f"{render_preview()} [ UPDATED ]\n \n Step 1/4: [ Loading... ]")
    time.sleep(1), clear_screen()
   #
    # BP - Step 2
    bp_2 = "\n \n Step 2/4: Would you like to add the breadcrumb now?"
    screen = f"{render_preview()}{bp_2}"
    print(f"{screen} y/n")
    while True: # BP - Step 2
        ans = input(f"{ASK}").strip().lower()
        if ans in ['', 'y', 'n']:
            if ans in ['y', '']:
                clear_screen()
                custom = input(f"{screen} → Yes → [ Editing... ] \n{GAP}Insert your breadcrumb (Press Enter to use the current folder name):\n{ASK}").strip()
                store["breadcrumb"] = custom if custom else os.path.basename(os.getcwd())
                break
            if ans == 'n':
                while True:
                    clear_screen()
                    print(f"{screen} → No, use predefined \n{SEL}Select an option (Press Enter to use default \"$na\"):\n{GAP}{GAP}1) $na - Not Apply - Not Available\n{GAP}{GAP}2) $cx - No Context")
                    opt = input(f"{GAP}{ASK}").strip()
                    if not opt:
                        opt = '1'
                    if opt in ['1', '2']:
                        wildcard = '$na' if opt == '1' else '$cx' if opt == '2' else '' 
                        store["breadcrumb"] = wildcard  # store applied breadcrumb
                        break
                break
        else:
            print(f"{GAP}! INPUT_ERROR_001:  Invalid option or non-existent... Try again ")
    clear_screen(), print(f"{render_preview()} [ UPDATED ]\n \n Step 2/4: [ Loading... ]")
    time.sleep(1), clear_screen()
   #
    # BP - Step 3
    bp_3 = "\n \n Step 3/4: Add a Holder"
    screen = f"{render_preview()} {bp_3}"
    print(f"{screen} → [ Editing... ] ")
    holder_input = input(f"{GAP}Insert the name (Press Enter to choose a predefined option):\n{ASK}").strip()
    if holder_input:
        store["holder"] = holder_input
    else:
        clear_screen()
        print(f"{screen} → predefined \n{SEL}Select an option (Press Enter to use default \"$uk\"):\n{GAP}{GAP}1) $uk - Unknown\n{GAP}{GAP}2) $up - Unidentified person\n{GAP}{GAP}3) $uc - Unidentified character")
        while True:
            opt = input(f"{GAP}{ASK}").strip()
            if not opt:
                opt = '1'
            if opt in ['1', '2', '3']:
                wildcard = '$uk' if opt == '1' else '$up' if opt == '2' else '$uc'
                store["holder"] = wildcard
                break
            else:
                print(f"{GAP}{GAP}! INPUT_ERROR_001:  Invalid option or non-existent... Try again.")
    clear_screen(), print(f"{render_preview()} [ UPDATED ]\n \n Step 3/4: [ Loading... ]")
    time.sleep(1) ,clear_screen()
   #
    # BP - Step 4
    bp_4 = "\n \n Step 4/4: Add a identifier code"
    screen = f"{render_preview()}{bp_4}"
    print(f"{screen} → [ Editing... ] ")
    while True: 
        custom_id = input(f"{GAP} Insert the ID (Press Enter to use default \"$ID\"):\n{ASK}").strip()
        if not custom_id:
            identifier = '$ID'
        elif custom_id.isalpha() and len(custom_id) == 3:
            identifier = custom_id.upper()
        else:
            print(f"{GAP}( ! ) INPUT_ERROR_002: Invalid input; only allows 3 alphabetic characters (no numbers or symbols).")
            continue
        # Confirmation
        clear_screen()
        print(f"{screen} → {identifier}\n{GAP}\n{GAP}CONFIRMATION: The ID to be formatted is \"{identifier}\"\n{GAP}Press \"Enter\" to continue or \"c\" to cancel:\n{GAP}")
        while True:
            confirm = input(f"{ASK}").strip().lower()
            if confirm in ['', 'ok']:  # continuar
                clear_screen()
                store["ident"] = identifier
                break
            elif confirm == 'c':
                print(f"\n Process cancelled. One second please...")
                time.sleep(2)
                clear_screen()
                print(f"{render_preview()}{bp_4} (Press Enter to use default \"$ID\"):")
                break
            else:
                print(f"{GAP}! INPUT_ERROR_001:  Invalid option or non-existent... Try again")
        if confirm in ['', 'ok']:
            break
    clear_screen(), print(f"{render_preview()} [ UPDATED ]\n \n Step 4/4: [ Loading... ]")
    time.sleep(1) ,clear_screen()
   #
    # Final confirmation
    fp = f"{GAP}\n{GAP}ATTENTION: Please review the preview format before proceeding.\n{GAP}Once confirmed, the script will rename your files using this format\n{GAP}This process cannot be undone.\n{GAP}\n{GAP}Note: Folders or any files starting with \"~\" will be ignored.\n{GAP}"
    preview = f"{render_preview()} \n"
    screen = f"{preview}\n Confirmation: Type \"ok\" to confirm or \"r\" to reEdit the format: \n{fp}"
    print(f"{screen}")
    while True:
        confirm = input(f"{ASK}").strip().lower()
        if confirm in ['y', 'ok']:  # continuar
            clear_screen()
            print(f"{preview} \n Applying changes..."), time.sleep(1)
            rename_files()
            return 'done'
        elif confirm == 'r':
            clear_screen()
            print(f"{screen}\n{ASK}[i] Process cancelled, restarting..."), time.sleep(2), clear_screen()
            store = STORE_TEMPLATE.copy()
            return 'restart'
        else:
            clear_screen(), print(f"{screen}")

def rename_files():
    global new_name_date, new_name_bread, master_index
    script_name = ignore_scrypt()
    formated_name = ""
    ### print(f"DEBUG::: {store}")
    for fname in os.listdir(path): # Itera sobre cada archivo
        src = os.path.join(path, fname)
        if not os.path.isfile(src) or fname.startswith('~'): # Ignora si es un directorio o si empieza con `~`
            ###print(f"DEBUG::: >> - ! file its a directory or starts with `~`, skipping --continue \n")
            continue
        if fname == script_name: # Skipea el script
            ###print(f"DEBUG::: >> - ! its me, the script, skipping... --continue \n ")
            continue
        print(f"{GAP} <<<  {fname}")
        if isinstance(store['date'], str):
            add_date(date_string=store['date'], target_fname=fname)
        # print(f"DEBUG::: >>p {new_name_date} \n{GAP} -   next step")
        if isinstance(store['date'], bool): # Si es un booleano, no se aplica
            new_name_date = fname
        add_breadcrumb(bread_string=store['breadcrumb'], target_fname=new_name_date)
        # print(f"DEBUG::: >>p {new_name_bread} \nDEBUG::: >>p master_index = {master_index} \n{GAP} -   next step")
        formated_name = f"~{new_name_bread[:master_index]}[{store['holder']}]_{store['ident']}_{new_name_bread[master_index:]}"
        print(f"{GAP} >>> {formated_name} \n{GAP}")
        #
        # dst = os.path.join(path, formated_name)
        # dst = os.rename(src, dst)
        master_index = 0 # reset master_index
    print(f"{GAP}[i] All files renamed.\n")

# Entrada principal - Entry point
if __name__ == '__main__':
    while run_survey() == 'restart':
        pass

    time_close = 500
    for time_close in range(time_close, 0, -1):
        print(f"\r ▲ Its done, You don't have to close this window, it will close by itself. Time remaining ({time_close} seg)", end="")
        time.sleep(1)
