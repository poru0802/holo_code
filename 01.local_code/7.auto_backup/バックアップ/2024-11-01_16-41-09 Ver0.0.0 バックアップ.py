import os

def baukup_folder_check():
    folder_path='./バックアップ'
    print(os.getcwd())
    print(os.path.isdir(folder_path))




def main():
    baukup_folder_check()
    #if baukup_folder_check==True:
   #     baukup_folder_create()
   # folder_10_check()
   # if folder_10_check==false:
   #     old_faile_deleat()
   # baukup_faile_create()

if __name__=='__main__':
    main()

