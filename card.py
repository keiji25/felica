import os
import sys
import datetime
import playsound
import nfc

r = []

def print_info(s, student_info):
    if s == "出発":
        print(f"\033[33m{s}モード\033[0m")
    elif s == "時間未経過":
        print(f"\033[31m{s}モード\033[0m")
    print_list = [
        f"\t　学籍番号：{student_info[0]}\n",
        f"\t　　　氏名：{student_info[1]}\n",
        f"\tカレッジ名：{student_info[2]}\n",
        f"\t　　学科名：{student_info[3]}\n",
        f"\t　　　性別：{student_info[4]}\n",
        f"\t　　　学年：{student_info[5]}\n"
    ]
    return print_list

def check_card(student_id):
    path = './inout.gsheet'
    if not os.path.isfile(path):
        with open(path, 'w', encoding='utf-8') as f:
            pass
        
    with open(path, 'r+', encoding='utf-8') as f:
        index = f.readlines()
        now = datetime.datetime.now()
        kaishi_flag, kitaku_flag = False, False
        cnt_num = 0
        for i in index:
            if student_id in i and str(now).split( )[0] in i:
                cnt_num += 1

        if cnt_num % 2 == 0:
            s = "出発"
            kaishi_flag = True
        else:
            s = "終了"
            for i in reversed(index):
                if student_id in i:
                    bef = i.rstrip().split(",")[2].lstrip(" ")
                    bef = datetime.datetime.strptime(bef, '%Y-%m-%d %H:%M:%S.%f')
                    break
            diff = str(now - bef).split(":")
            if int(diff[0]) >= 1 or int(diff[1]) >= 30:
                    kitaku_flag = True            
                
        os.system('cls')
        with open("student.csv", 'r', encoding='utf-8') as a:
                index = a.readlines()
                for i in index:
                    if student_id in i:
                        student_info = i.split(", ")
                        break
        if kitaku_flag or kaishi_flag:
            f.writelines(f"{student_id}, {s}, {now}\n")
            # 出力
            r = print_info(s, student_id)
            playsound.playsound("OK.mp3")
        else:
            r = [print_info("時間未経過", student_info), f"残り\033[33m{30 - int(diff[1])}分後\033[0mに終了できます"]
    
    return r
            

def connected(tag):
    global r
    service_code = 0x200B
    try: 
        if isinstance(tag, nfc.tag.tt3.Type3Tag):
            try:
                svcd = nfc.tag.tt3.ServiceCode(service_code >> 6, service_code & 0x3f)
                blcd = nfc.tag.tt3.BlockCode(0,service=0)
                block_data = tag.read_without_encryption([svcd], [blcd])
                student_id = str(block_data[0:9].decode("utf-8"))
                r = check_card(student_id)
            except Exception as e:
                print("Error:%s" % e)
    except AttributeError:
        pass
    return True

def main():
    global r
    try:
        clf = nfc.ContactlessFrontend('usb')
        clf.connect(
            rdwr={'on-connect': connected}
        )
    except OSError as e:
        print("PaSoRiが認識されませんでした")
        print(f"エラー： {e}")
        
    except KeyboardInterrupt:
        clf.close()
        sys.exit(0)
    except Exception as e:
        print("何らかのエラーが発生しました")
        print(f"エラー： {e}")
        print("考えられる原因")
        print("\tPaSoliのセットアップが正しくできていない")
        print("\tパソコンのやる気がない")
    clf.close()
    return r

# main()

