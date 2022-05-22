import tkinter
import card

r = []
def func():
    global r
    textBox1.delete(0, tkinter.END)
    if s_btn.cget("text") == "自動モード":
        r = card.main()
        txt = ""
        for i in range(1, len(r)):
            txt += r[i]
        label2["text"] = txt
        btn.after(100, func)

def calc(event):
    global r
    getvalue = textBox1.get()
    textBox1.delete(0 ,tkinter.END)
    if s_btn.cget("text") == "自動モード":
        textBox1.bind('<Return>', calc)
    else:
        r = card.main(str.upper(getvalue))
        txt = ""
        for i in range(1, len(r)):
            txt += r[i]
        label2["text"] = txt

def change():
    getvalue = s_btn.cget("text")
    if getvalue == "手動モード":
        s = "自動モード"
        textBox1.configure(state='readonly')
    elif getvalue == "自動モード":
        s = "手動モード"
        textBox1.configure(state='normal')
    s_btn["text"] = s
    func()

def approve():
    pass
    
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
    s_btn = tkinter.Button(text='手動モード', command=change)
    s_btn.pack(anchor='center')

    textBox1 = tkinter.Entry(
        root,
        validate='key',
        vcmd=(tcl_isOk, '%P'),
        textvariable=str_v
    ) 
    textBox1.place(width=100, height=30)
    textBox1.pack(anchor='center')

    label2 = tkinter.Label(font=("Helvetica",14))
    label2.pack()
    textBox1.focus_set()

    btn = tkinter.Button(text='実行', command=func)
    approve_btn = tkinter.Button(text='実行', command=approve)
    if s_btn.cget("text") == "自動モード":
        btn.after(100, func)

    textBox1.bind('<Return>', calc)

    root.mainloop()