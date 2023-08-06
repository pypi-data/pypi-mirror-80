from skpy import Skype
from rich.console import Console
from rich.table import Column, Table
from tqdm import tqdm
import requests
import os
import argparse


def getUserCread():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-u", "--username", help='Take skype username(needed first time)')
    arg_parser.add_argument("-p", "--password", help='Take skype password(needed first time)')
    arg_parser.add_argument("--default_path", help='Put path where to save downloaded files')
    arg_parser.add_argument("-c", "--contact", help="Put Skype Id whose chat's files you wanna download")
    args = arg_parser.parse_args()

    try:
        config = open('.sk_usr_config', 'r')
        username = config.readline()
        password = config.readline()
        path = config.readline()
        return username, password, path, args.contact
    except FileNotFoundError:
        if args.username is None:
            username = input('Enter Skype username : ')
            password = input('Enter Skype password : ')
            def_path = input('Enter download path : ')
            cred = username, password, def_path, args.contact
            write_cred_into_file(cred)
            return cred
        elif args.password is None:
            password = input('Enter Skype password : ')
            def_path = input('Enter download path : ')
            cred = args.username, password, def_path, args.contact
            write_cred_into_file(cred)
            return cred
        elif args.default_path is None:
            def_path = input('Enter download path : ')
            cred = args.username, args.password, def_path, args.contact
            write_cred_into_file(cred)
            return cred
        else:
            cred = args.username, args.password, args.default_path
            write_cred_into_file(cred)
            return args.username, args.password, args.default_path, args.contact


def write_cred_into_file(cred):
    config = open('.sk_usr_config', 'w')
    config.writelines(cred[0] + '\n')
    config.write(cred[1] + '\n')
    config.write(cred[2])


def download_file(file_name, content_url, auth_token, download_path, console):
    final_file_name = file_name
    file_inc = 1
    while os.path.isfile(os.path.join(download_path, final_file_name)):
        final_file_name = str(file_inc) + '_' + file_name
        file_inc = file_inc + 1

    console.print('Downloading ' + '[bold blue]' + str(file_name) + '[/bold blue]' + '... It will be saved as : [bold red]' + final_file_name + '[/bold red]')
    response = requests.get(content_url, headers={"Authorization": auth_token}, stream=True)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open(os.path.join(download_path, final_file_name), 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        console.print("ERROR, something went wrong", style="red")


def get_msg_list(sk, console, skypr_id):
    console.print('Getting Files Please wait ...', style="blue")
    file_dict = {}
    ch = sk.contacts[skypr_id].chat
    msgs = sk.chats[ch.id].getMsgs()
    i = 1
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column('ID')
    table.add_column('DateTime')
    table.add_column('File Name')
    for msg in msgs:
        if 'RichText/Media_GenericFile' == msg.type:
            table.add_row(str(i), msg.time.strftime("%d-%b-%Y %I:%M %p"), str(msg.file.name))
            file_dict[i] = msg.file.name, "{0}/views/original".format(msg.file.urlAsm)
            i = i + 1
    console.print("Files List : ", style="bold red")
    console.print(table)
    return file_dict


def main():
    cred = getUserCread()
    console = Console()
    if cred[0] is not None and cred[3] is not None:
        console.print('Logging into Skype Please wait ...', style="blue")
        sk = Skype(cred[0], cred[1], "tokenFile")
        file_dict = get_msg_list(sk, console, cred[3])
        while True:
            user_input = input('n/id/quit >> ')
            if user_input.isnumeric():
                index = int(user_input)
                if 1 <= index <= len(file_dict):
                    file_tuple = file_dict[index]
                    download_file(file_tuple[0], file_tuple[1],
                                  "skype_token {0}".format(sk.conn.tokens["skype"]), cred[2], console)
                else:
                    console.print('Please Enter valid Id', style="red")
            else:
                if user_input == 'quit':
                    break
                elif user_input == 'n':
                    file_dict = get_msg_list(sk, console, cred[3])
                else:
                    console.print('Please Enter Valid Option', style="red")

    elif cred[0] is not None and cred[3] is None:
        console.print('Logging into Skype Please wait ...', style="blue")
        sk = Skype(cred[0], cred[1], "tokenFile")
        console.print('Getting Contacts List Please wait ...', style="blue")
        contact = sk.contacts
        contact_dict = {}
        i = 1
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column('ID')
        table.add_column('Name')
        for c in contact:
            table.add_row(str(i), str(c.name))
            contact_dict[i] = c.id
            i = i + 1
        console.print("Contact List : ", style="bold yellow")
        console.print(table)
        console.print('Please type [bold]ID[/bold] and press Enter', style="blue")
        contact_id = int(input())
        file_dict = get_msg_list(sk, console, contact_dict[contact_id])
        while True:
            user_input = input('n/{id}/quit >> ')
            if user_input.isnumeric():
                index = int(user_input)
                if 1 <= index <= len(file_dict):
                    file_tuple = file_dict[index]
                    download_file(file_tuple[0], file_tuple[1],
                                  "skype_token {0}".format(sk.conn.tokens["skype"]), cred[2], console)
                else:
                    console.print('Please Enter valid Id', style="red")
            else:
                if user_input == 'quit':
                    break
                elif user_input == 'n':
                    file_dict = get_msg_list(sk, console, contact_dict[contact_id])
                else:
                    console.print('Please Enter Valid Option', style="red")


if __name__ == "__main__":
    main()
