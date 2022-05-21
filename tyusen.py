import os
import sys
import datetime
import playsound
import nfc

def check_card(student_id):
    path = './tyusen.txt'
    if not os.path.isfile(path):
        with open(path, 'w', encoding='utf-8') as f:
            pass
    with open(path, 'r+', encoding='utf-8') as f:
        index = f.read()
        cnt_num = index.count(student_id)
        if cnt_num == 0:
            print("抽選してください")
            f.writelines(f"{student_id}, {str(datetime.datetime.now())}\n")
            playsound.playsound("OK.mp3")
        else:
            print("すでに参加済みです。")
            
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

if __name__ == "__main__":
    try:
        clf = nfc.ContactlessFrontend('usb')
        while True:
            clf.connect(rdwr={'on-connect': connected,})
    except OSError:
        print("PaSoRiが認識されませんでした\n終了します")
    except KeyboardInterrupt:
        clf.close()
        sys.exit(0)