import os
import datetime
import playsound
import nfc
import threading
import pandas as pd

r = []
db = pd.Series

def open_excel():
    global df
    df = pd.read_excel('全学生名簿2022.xlsx')

def print_info(s, student_info, started):
    global r
    print_list = [
        f"{s}\n",
        f"学科名：{student_info[0][0]}\n",
        f"学科記号：{student_info[0][1]}\n",
        f"学年：{student_info[0][2]}\n",
        f"性別：{student_info[0][3]}\n",
        f"学籍番号：{student_info[0][4]}\n",
        f"氏名：{student_info[0][5]}\n",        
    ]
    
    starttime = str(started).split(".")[0][5:].replace('-', '月', 1).replace(' ', '日 ', 1).replace(':', '時', 1).replace(':', '分', 1) + "秒"
    endtime = str(started + datetime.timedelta(minutes=30)).split(".")[0][5:].replace('-', '月', 1).replace(' ', '日 ', 1).replace(':', '時', 1).replace(':', '分', 1) + "秒"
         
    print_list.append(f"出発時刻：{starttime}\n")
    print_list.append(f"終了可能時刻：{endtime}\n")

    r = print_list

def check_card(student_id):
    global r, df
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
        if cnt_num >= 2:
            r = "すでに参加済みです"
            return
        elif cnt_num % 2 == 0:
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
        # with open("student.csv", 'r', encoding='utf-8') as a:
        #     exiflag = False
        #     index = a.readlines()
        #     for i in index:
        #         if student_id == i[:9]:
        #             student_info = i.split(", ")
        #             exiflag = True
        #             break
        
        student_info = df[["学科名", "記号", "年次", "性別", "学籍番号", "氏名＿漢字", "氏名＿カナ"]][df["学籍番号"].isin([student_id])].values.tolist()

        if len(student_info) == 0:
            exiflag = False
        else:
            exiflag = True

        if not exiflag:
            r = [f"{student_id}は存在しません"]
        elif kitaku_flag or kaishi_flag:
            f.writelines(f"{student_id}, {s}, {now}\n")
            print_info(s, student_info, now)
            sound(student_id, "OK.mp3")
        else:
            print_info("時間未経過", student_info, started)
            r.append(f"\n残り約{30 - int(diff[1])}分後に終了できます\n")
            sound(student_id, "NO.mp3")

def sound(student_id, path):
    if student_id in ["K019C1066", "K019C1166"]:
        playsound.playsound("397.mp3")
    else:
        playsound.playsound(path)

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
