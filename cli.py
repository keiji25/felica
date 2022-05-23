import tkinter
import card
import datetime

r = []
def func():
    global r, bef
    textBox1.delete(0, tkinter.END)
    if s_btn.cget("text") == "自動モード":
        r = card.main()
        txt = ""
        for i in range(len(r)):
            txt += r[i]
        if r != []:
            label2["text"] = txt
        btn.after(100, func)
    approve_check(r)

def calc(event):
    global r
    getvalue = textBox1.get()
    textBox1.delete(0 ,tkinter.END)
    if s_btn.cget("text") == "自動モード":
        textBox1.bind('<Return>', calc)
    else:
        r = card.main(str.upper(getvalue))
        txt = ""
        for i in range( len(r)):
            txt += r[i]
        if r != []:
            label2["text"] = txt
    approve_check(r)

def change():
    getvalue = s_btn.cget("text")
    if getvalue == "手動モード":
        s = "自動モード"
        textBox1.configure(state='readonly')
    elif getvalue == "自動モード":
        s = "手動モード"
        textBox1.configure(state='normal')
    s_btn["text"] = s
    approve_btn.pack_forget()
    func()

def approve_check(r):
    if r == []:
        pass
    elif "時間未経過" == r[0].rstrip("\n"):
        approve_btn.pack()
    else:
        approve_btn.pack_forget()

def approve():
    global r
    with open("inout.gsheet", 'a', encoding='utf-8') as f:
        student_id = r[1].split('：')[1].rstrip('\n')
        txt = f"{student_id}, 終了, {datetime.datetime.now()}\n"
        f.writelines(txt)
    txt = ""
    for i in range(1, len(r) - 2):
        txt += r[i]
    
    r = f"終了許可しました\n\n{txt}終了時刻：{str(datetime.datetime.now()).split('.')[0][5:].replace('-', '月', 1).replace(' ', '日 ', 1).replace(':', '時', 1).replace(':', '分', 1)}秒"
    label2["text"] = r
    card.r = r
    approve_btn.pack_forget()
    

def isOk(after):
    if len(after) > 9:
        return False
    return True

if __name__ == "__main__":
    root = tkinter.Tk()
    root.title(u"入退場管理")
    root.geometry("800x500")
    root.iconbitmap(default='act.ico')
    
    tcl_isOk = root.register(isOk)
    str_v = tkinter.StringVar()
    s_btn = tkinter.Button(text='自動モード', command=change)
    s_btn.pack(anchor='center')

    textBox1 = tkinter.Entry(
        root,
        validate='key',
        vcmd=(tcl_isOk, '%P'),
        textvariable=str_v,
        state='readonly'
    ) 
    textBox1.place(width=100, height=30)
    textBox1.pack(anchor='center')

    label2 = tkinter.Label(font=("Helvetica",14))
    label2.pack()
    textBox1.focus_set()

    btn = tkinter.Button(text='実行', command=func)
    approve_btn = tkinter.Button(text='終了許可', command=approve)

    if s_btn.cget("text") == "自動モード":
        btn.after(100, func)

    textBox1.bind('<Return>', calc)

    root.mainloop()