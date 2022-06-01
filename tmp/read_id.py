import threading
import nfc

def connected(tag):
    service_code = 0x200B
    if isinstance(tag, nfc.tag.tt3.Type3Tag):
        try:
            svcd = nfc.tag.tt3.ServiceCode(service_code >> 6, service_code & 0x3f)
            blcd = nfc.tag.tt3.BlockCode(0,service=0)
            block_data = tag.read_without_encryption([svcd], [blcd])
            student_id = str(block_data[0:9].decode("utf-8"))
            
            """
            student_id変数に学籍番号が格納される
            """
            
        except IOError as e:
            print("デバイスが見つかりません")
            print(f"Error:{e}")
        except Exception as e:
            print(f"Error:{e}")
    return True

class Card(object):
    def __init__(self):
        self.flag = False
    def __call__(self):
        try:
            with nfc.ContactlessFrontend('usb') as clf:
                clf.connect(rdwr={'on-connect': connected}, terminate=lambda: self.flag)
        except Exception as e:
            print(f"Error:{e}")

if __name__ == "__main__":
    threading.Thread(target=(Card())).start()
    Card.flag = True