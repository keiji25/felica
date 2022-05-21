import tkinter
import card
def func():
    getvalue = textBox1.get()
    print("in the function =",getvalue)
    textBox1.delete(0,tkinter.END)
    label2["text"] = getvalue

def calc(event):
    getvalue = textBox1.get()
    textBox1.delete(0,tkinter.END)
    label2["text"] = getvalue
    card.main()


root = tkinter.Tk()
root.title(u"入退場管理")
root.geometry("500x300") 

# 入出力エリア
textBox1 = tkinter.Entry() 
textBox1.place(width=100, height=30)


label2 = tkinter.Label(font=("Helvetica",14))
textBox1.focus_set()
btn = tkinter.Button(text='実行', command=func)

textBox1.bind('<Return>', calc)

textBox1.pack(anchor='center')
btn.pack()
label2.pack()


root.mainloop() 