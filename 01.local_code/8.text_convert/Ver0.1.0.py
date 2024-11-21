#20241106 Ver0.0.0 メインプログラム作成
#20241114 Ver0.1.0 文字手入力input関数に変更
#20241118 Ver1.1.0 動画リアルタイムチェック機能追加

import vlc
import time
  
def display_and_edit_strings(strings):  
    print("現在の文字列一覧：")  
    for i, sublist in enumerate(strings):    
        print(f"{sublist[2]}")  
    print("\n全ての文字列を一度に修正または消去します。")  
    print("修正しない場合はそのままEnterを押してください。")  
    print("サブリスト全体を消去する場合は、任意の文字列でデリートキーを押してください。")  
    updated_strings = []   
    player = vlc.MediaPlayer('test.mp4')   
    player.play()
    time.sleep(1)
    while True:  
        for i, sublist in enumerate(strings):  
            delete_sublist = False   
            string = sublist[2]  
            new_string = []
            input_string='s' 
            while input_string=='s' or input_string=='ｓ': 
                target_time = sublist[0]  # 例: 60秒の位置にジャンプ  
                player.set_time(target_time * 1000) 
                input_string=input(f"{string} -> 新しい文字列：") 
                if input_string=="": 
                    pass  
                elif input_string=="d" or input_string=="ｄ":  
                    delete_sublist = True  
                elif input_string=="s" or input_string=="ｓ":
                    target_time = sublist[0]  # 例: 60秒の位置にジャンプ  
                    player.set_time(target_time * 1000)  
                else:  
                    new_string.append(input_string) 
            if delete_sublist:  
                continue  
            if new_string:  
                sublist[2] = ''.join(new_string)  
            else:  
                sublist[2] = string  # 修正しない場合は元の文字列を保持  
            if not delete_sublist:  
                updated_strings.append(sublist)  
        return updated_strings  
strings = [[10, 15,"appel"], [17, 19, "banana"], [21, 24, "cherry"]]  
updated_strings = display_and_edit_strings(strings)  
print("更新された配列：", updated_strings) 