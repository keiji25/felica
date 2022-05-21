import os
import sys
import datetime
import time
import playsound
import nfc




def print_info(s, student_info):
    if s == "出発":
        print(f"\033[33m{s}モード\033[0m")
    elif s == "時間未経過":
        print(f"\033[31m{s}モード\033[0m")
    print(f"\t　学籍番号：{student_info[0]}")
    print(f"\t　　　氏名：{student_info[1]}")
    print(f"\tカレッジ名：{student_info[2]}")
    print(f"\t　　学科名：{student_info[3]}")
    print(f"\t　　　性別：{student_info[4]}")
    print(f"\t　　　学年：{student_info[5]}")

def check_card(student_id):
    path = './inout.gsheet'
    if not os.path.isfile(path):
        with open(path, 'w', encoding='shift_jis') as f:
            pass
        
    with open(path, 'r+', encoding='shift_jis') as f:
        index = f.readlines()
        now = datetime.datetime.now()
        kaishi_flag, kitaku_flag = False, False
        cnt_num = 0
        for i in index:
            if student_id in i:
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
            print_info(s, student_info)
            playsound.playsound("OK.mp3")
        else:
            print_info("時間未経過", student_info)
            print(f"残り\033[33m{30 - int(diff[1])}分後\033[0mに終了できます")
            
            

def connected(tag):
    service_code = 0x200B
    try: 
        if isinstance(tag, nfc.tag.tt3.Type3Tag):
            try:
                svcd = nfc.tag.tt3.ServiceCode(service_code >> 6, service_code & 0x3f)
                blcd = nfc.tag.tt3.BlockCode(0,service=0)
                block_data = tag.read_without_encryption([svcd], [blcd])
                student_id = str(block_data[0:9].decode("utf-8"))
                check_card(student_id)
            except Exception as e:
                print("Error:%s" % e)
    except AttributeError:
        pass
    return True

def main():
    print("ウォークラリー時間管理だぉ\nすたーーーーと！\n")
    print("-------------------------------------------\n")
    try:
        clf = nfc.ContactlessFrontend('usb')
        while True:
            clf.connect(rdwr={'on-connect': connected,})
    except OSError as e:
        print("PaSoRiが認識されませんでした")
        print(f"エラー： {e}")
        for i in range(10, 0, -1):
            print(f"\r{i}秒後に自動終了します　　", end="")
            time.sleep(1)
    except KeyboardInterrupt:
        clf.close()
        sys.exit(0)
    except Exception as e:
        print("何らかのエラーが発生しました")
        print(f"エラー： {e}")
        print("考えられる原因")
        print("\tPaSoliのセットアップが正しくできていない")
        print("\tパソコンのやる気がない")
        for i in range(10, 0, -1):
            print(f"\r{i}秒後に自動終了します", end="")
            time.sleep(1)