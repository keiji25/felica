import os
import datetime
import playsound
import nfc
import threading
r = []

def print_info(s, student_info, *started):
    global r
    print_list = [
        f"{s}\n",
        f"学籍番号：{student_info[0]}\n",
        f"氏名：{student_info[1]}\n",
        f"性別：{student_info[4]}\n",
        f"学年：{student_info[5]}\n",
        f"カレッジ名：{student_info[2]}\n",
        f"学科名：{student_info[3]}\n",
    ]
    if len(started) > 0:
        s = str(started[0]).split(".")[0][5:].replace('-', '月', 1).replace(' ', '日 ', 1).replace(':', '時', 1).replace(':', '分', 1) + "秒"
        print_list.append(f"開始時刻：{s}\n")

    r = print_list

def check_card(student_id):
    global r
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
                    started = i.rstrip().split(",")[2].lstrip(" ")
                    started = datetime.datetime.strptime(started, '%Y-%m-%d %H:%M:%S.%f')
                    break
            diff = str(now - started).split(":")
            if int(diff[0]) >= 1 or int(diff[1]) >= 30:
                    kitaku_flag = True            
                
        # os.system('cls')
        with open("student.csv", 'r', encoding='utf-8') as a:
            exiflag = False
            index = a.readlines()
            for i in index:
                if student_id == i[:9]:
                    student_info = i.split(", ")
                    exiflag = True
                    break
        if not exiflag:
            r = [False, f"{student_id}は存在しません"]
        elif kitaku_flag or kaishi_flag:
            f.writelines(f"{student_id}, {s}, {now}\n")
            # 出力
            print_info(s, student_info, started)
            playsound.playsound("OK.mp3")
        else:
            print_info("時間未経過", student_info, started)
            r.append(f"\n残り約{30 - int(diff[1])}分後に終了できます\n")
            playsound.playsound("NO.mp3")

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

class Card(object):
    global r
    def __init__(self):
        self.flag = False
    def __call__(self):
        try:
            with nfc.ContactlessFrontend('usb') as clf:
                clf.connect(rdwr={'on-connect': connected}, terminate=lambda: self.flag)
        except Exception as e:
            pass

def main(*student_id):
    global r
    if len(student_id) > 0:
        check_card(student_id[0])
    else:
        threading.Thread(target=(Card())).start()
        Card.flag = True
    return r