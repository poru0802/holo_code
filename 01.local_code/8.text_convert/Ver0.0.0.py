#20241106 Ver0.0.0 メインプログラム作成

import keyboard  
  
def display_and_edit_strings(strings):  
    print("現在の文字列一覧：")  
    for i, sublist in enumerate(strings):    
        print(f"{sublist[2]}")  
    print("\n全ての文字列を一度に修正または消去します。")  
    print("修正しない場合はそのままEnterを押してください。")  
    print("サブリスト全体を消去する場合は、任意の文字列でデリートキーを押してください。")  
    updated_strings = []  
    for i, sublist in enumerate(strings):  
        delete_sublist = False   
        string = sublist[2] 
        print(f"\n{string} -> 新しい文字列：", end='', flush=True)  
        new_string = []  
        while True:  
            event = keyboard.read_event()  
            if event.event_type == keyboard.KEY_DOWN:  
                if event.name == 'enter':  
                    break  
                elif event.name == 'delete':  
                    delete_sublist = True  
                    break  
                elif event.name == 'backspace':  
                    if new_string:  
                        print('\b \b', end='', flush=True)  
                        new_string.pop()  
                else:  
                    new_string.append(event.name)  
                    print(event.name, end='', flush=True)  
        if delete_sublist:  
            continue  
        if new_string:  
            sublist[2] = ''.join(new_string)  
        else:  
            sublist[2] = string  # 修正しない場合は元の文字列を保持  
        if not delete_sublist:  
            updated_strings.append(sublist)  
    return updated_strings  
strings = [["start", "end","appel"], ["start", "end", "banana"], ["start", "end", "cherry"]]  
updated_strings = display_and_edit_strings(strings)  
print("更新された配列：", updated_strings) 