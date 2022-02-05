import sys
import binascii
import nfc

service_code = 0x200B
def connected(tag):
    if isinstance(tag, nfc.tag.tt3.Type3Tag):
        try:
            svcd = nfc.tag.tt3.ServiceCode(service_code >> 6, service_code & 0x3f)
            blcd = nfc.tag.tt3.BlockCode(0,service=0)
            block_data = tag.read_without_encryption([svcd], [blcd])
            student_id = str(block_data[0:9].decode("utf-8"))
            print(student_id)
        except Exception as e:
            print("Error:%s" % e)
    else:
        print("Error:tag isn't Type3Tag")
    return True
clf = nfc.ContactlessFrontend('usb')
def main():
    while True:
        clf.connect(rdwr={'on-connect': connected,})
try:
    main()
except KeyboardInterrupt:
    print("Forced termination")
    clf.close()
    sys.exit(0)