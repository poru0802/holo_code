#20241101 Ver1.0.0 メイン動作デバック完了

import os
import shutil
import datetime
import schedule
import time
import tkinter as tk
from tkinter import filedialog

def path_get():
    typ = [('pyファイル','*.py')] 
    dir = '\\AD-5548\A02section\工機保全室\工機\仕上1\99_自書箱\11_安藤\7.DX\2.コード一覧'
    main_file_path = filedialog.askopenfilename(filetypes = typ, initialdir = dir)
    main_folder_path = os.path.dirname(main_file_path)
    return main_folder_path,main_file_path

def backup_folder_check(main_folder_path):
    folder_path=f'{main_folder_path}/バックアップ'
    return os.path.isdir(folder_path)

def backup_folder_create(main_folder_path):
    new_dir_path = f'{main_folder_path}/バックアップ'
    os.mkdir(new_dir_path)

def folder_10_check(main_folder_path):
    global file_list
    file_list=os.listdir(f'{main_folder_path}/バックアップ')
    if len(file_list)<10:
        return True
    else:
        return False
    
def old_file_deleat(main_folder_path):
    os.remove(f'{main_folder_path}/バックアップ/{file_list[0]}')

def backup_file_create(main_folder_path,main_file_path):
    backup_file_path=f'{main_folder_path}/バックアップ/{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")} {os.path.basename(main_file_path)}'
    shutil.copy2(main_file_path, backup_file_path)
    print('バックアップ完了')


def main(main_folder_path,main_file_path):
    if not backup_folder_check(main_folder_path):
        backup_folder_create(main_folder_path)
    if not folder_10_check(main_folder_path):
        old_file_deleat(main_folder_path)
    backup_file_create(main_folder_path,main_file_path)

if __name__=='__main__':
    main_folder_path,main_file_path=path_get()
    schedule.every(5).minutes.do(lambda:main(main_folder_path,main_file_path))
    while True:
        schedule.run_pending()
        time.sleep(1)

