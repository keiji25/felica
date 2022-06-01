import tkinter as tk
import card
import datetime

class App(tk.Frame):
    r = []
    def __init__(self, root=None):
        super().__init__(root)
        self.pack()

        root.title(u"入退場管理")
        root.geometry("800x500")

        root.iconbitmap(default='act.ico')

        self.tcl_isOk = root.register(self.isOk)
        self.str_v = tk.StringVar()
        self.s_btn = tk.Button(text='自動モード', command=self.change)
        self.s_btn.pack(anchor='center')

        self.textBox1 = tk.Entry(
            root,
            validate='key',
            vcmd=(self.tcl_isOk, '%P'),
            textvariable=self.str_v,
            state='readonly'
        ) 

        self.textBox1.place(width=100, height=30)
        self.textBox1.pack(anchor='center')

        self.label2 = tk.Label(font=("Helvetica",14))
        self.label2.pack()
        self.textBox1.focus_set()

        self.btn = tk.Button(text='実行', command=self.func)
        self.approve_btn = tk.Button(text='終了許可', command=self.approve)

        if self.s_btn.cget("text") == "自動モード":
            self.btn.after(100, self.func)

        self.textBox1.bind('<Return>', self.calc)

    def func(self):
        global r, bef
        self.textBox1.delete(0, tk.END)
        if self.s_btn.cget("text") == "自動モード":
            r = card.main()
            txt = ""
            for i in range(len(r)):
                txt += r[i]
            if r != []:
                self.label2["text"] = txt
            self.btn.after(100, self.func)
            self.approve_check(r)

    def calc(self, event):
        global r
        getvalue = self.textBox1.get()
        self.textBox1.delete(0 ,tk.END)
        if self.s_btn.cget("text") == "自動モード":
            self.textBox1.bind('<Return>', self.calc)
        else:
            r = card.main(str.upper(getvalue))
            txt = ""
            for i in range( len(r)):
                txt += r[i]
            if r != []:
                self.label2["text"] = txt
        self.approve_check(r)

    def change(self):
        getvalue = self.s_btn.cget("text")
        if getvalue == "手動モード":
            s = "自動モード"
            self.textBox1.configure(state='readonly')
        elif getvalue == "自動モード":
            s = "手動モード"
            self.textBox1.configure(state='normal')
        self.s_btn["text"] = s
        self.approve_btn.pack_forget()
        self.func()

    def approve_check(self, r):
        if r == []:
            pass
        elif "時間未経過" == r[0].rstrip("\n"):
            self.approve_btn.pack()
        else:
            self.approve_btn.pack_forget()

    def approve(self):
        global r
        with open("inout.gsheet", 'a', encoding='utf-8') as f:
            student_id = r[5].split('：')[1].rstrip('\n')
            txt = f"{student_id}, 終了, {datetime.datetime.now()}\n"
            f.writelines(txt)
        txt = ""
        for i in range(1, len(r) - 2):
            txt += r[i]
        
        r = f"終了許可しました\n\n{txt}終了時刻：{str(datetime.datetime.now()).split('.')[0][5:].replace('-', '月', 1).replace(' ', '日 ', 1).replace(':', '時', 1).replace(':', '分', 1)}秒"
        self.label2["text"] = r
        card.r = r
        self.approve_btn.pack_forget()
        
    def isOk(self, after):
        if len(after) > 9:
            return False
        return True

def main():
    window = tk.Tk()
    app = App(root=window)
    app.mainloop()

if __name__ == "__main__":
    main()