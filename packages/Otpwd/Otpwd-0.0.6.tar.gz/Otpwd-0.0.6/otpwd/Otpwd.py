import time
import hashlib
from tkinter import *
from tkinter import messagebox
class Ept:
        
        

    def pwd_(self):
        day=time.localtime().tm_mday
        mon=time.localtime().tm_mon

        data=str(mon)+str(day)
        h1=hashlib.md5(data.encode(encoding='UTF-8'))

        after_=h1.hexdigest()

        pwd_=after_[1:7]
        print(pwd_)
        return pwd_
    def main(self):
        root=Tk()

        root.geometry("250x200+500+200")
        root.title('请输入密码')
        Label(root,text='请输入六位数字密码   ').grid(pady=40,padx=75)
        e=Entry(root,width=8,background='yellow')
        e.grid(row=1)
        num=['0']
        pwd_=Ept().pwd_()
        def sub():
            c1=e.get()
            if c1==pwd_:
                num[0]='vk'
                root.withdraw()
                
                root.destroy()
                

            else:
                message=messagebox.showerror('错误','请联系作者获取密码')            
        Button(root,text='确定',width=10,command=sub).grid(row=3,pady=25)
        
        mainloop()
        return num[0]

if __name__=='__main__':
    Ept().main()
