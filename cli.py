import tkinter
import card
import datetime

def func():
    getvalue = textBox1.get()
    textBox1.delete(0, tkinter.END)
    if s_btn.cget("text") == " 実行中 ":
        print(s_btn.cget("text"))
        label2["text"] = card.main()
        btn.after(100, func)

def calc(event):
    getvalue = textBox1.get()
    textBox1.delete(0 ,tkinter.END)
    if s_btn.cget("text") == " 実行中 ":
        label2["text"] = card.main()
        btn.after(100, func)
        textBox1.bind('<Return>', calc)

def change():
    getvalue = s_btn.cget("text")
    if getvalue == "停止中":
        s = " 実行中 "
    elif getvalue == " 実行中 ":
        s = "停止中"
    s_btn["text"] = s
    

root = tkinter.Tk()
root.title(u"入退場管理")
root.geometry("500x300") 

# 入出力エリア
s_btn = tkinter.Button(text='停止中', command=change)
s_btn.pack(anchor='center')

textBox1 = tkinter.Entry() 
textBox1.place(width=100, height=30)
textBox1.pack(anchor='center')


label2 = tkinter.Label(font=("Helvetica",14))
label2.pack()
textBox1.focus_set()

btn = tkinter.Button(text='実行', command=func)

if s_btn.cget("text") == " 実行中 ":
    btn.after(100, func)

textBox1.bind('<Return>', calc)

root.mainloop()