#! -*- coding: utf-8 -*-
from tkinter import *
import os
import re


master = Tk()
master.geometry("+500+250")
master.resizable(0,0)
master.title('MAC address calculater')
t1 = Text(master,width=35,height=40)
t1.grid(row=0,rowspan=3,column=1)
t2 = Text(master,width=45,height=40)
t2.grid(row=0,rowspan=3,column=3)
t2.bind("<KeyPress>",lambda e:"break")
##Display steps of how to use the tool
with open('help.txt','r',encoding='cp936') as f:
    t2.insert(END,f.read())

### sort according slot number
def my_sort(l):
    for i in range(0,len(l)):
        if(l[i].startswith('| 0-')):
            l[i] = l[i].replace('| 0-','1')
        elif(l[i].startswith('| 1-')):
            l[i] = l[i].replace('| 1-','33')
        elif(l[i].startswith('| 2-')):
            l[i] = l[i].replace('| 2-','444')

    for i in range(0,len(l)):
        l[i] = re.search('(\d+) +\| (.*) \|',l[i]).groups()

    l.sort(key = lambda x:int(x[0]))
    return l

### create formated data
def create_file(l):
    l1 = []
    for i in l:
        l1.append(i[1].replace(':',''))
    t2.delete(1.0,END)
    d = {1:' eth3 ethernet ',2:' eth4 ethernet ',5:' eth5 ethernet ',6:' eth6 ethernet '}
    for x in range(1,len(l1)+1):
        for i in d.keys():
            t2.insert(END,'interface '+str(x)+d.get(i)+':'.join(re.findall('(\w\w)',('%x' % (int(l1[x-1],16)+i))))+'\n')
        t2.insert(END,'\n\n')

##Go---> Button function
def bf_translate():

    s = t1.get(1.0,END)
    t = re.findall('\| [012].*\|.*\|\n',s)
    #t = t1.get(1.0,END).split('\n')
    #Delete space line
    while '' in t:
        t.remove('')
    
    t = my_sort(t)
    create_file(t)

def bf_clear():
    t1.delete(1.0,END)
Button(master,text='<---Clear --->',command=bf_clear,bg='yellow').grid(row=0,column=2)
Button(master,text='Go--->',command=bf_translate,bg='yellow').grid(row=1,column=2,sticky=E+W)

def bf_quit():
    master.destroy()
Button(master,text='Exit',command=bf_quit,bg='red').grid(row=2,column=2,ipady=10,sticky=S+E+W)


def bf_copy():
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(t2.get(1.0,END))
    r.update()
    r.destroy()
def bf_about():
    s = '''当前版本：v1.0

更新日志:
1,2018年6月28日---无

问题反馈：
maguanglei@etonetech.com'''
    r = Tk()
    r.geometry("200x250+650+250")
    Message(r,text=s).grid()

Button(master,text='about',command=bf_about).grid(row=0,column=2,sticky=N+E+W)

Button(master,text=' Copy---> ',bg='yellow',command=bf_copy).grid(row=2,column=2,sticky=E+W)
    



sb = Scrollbar(master)
sb.grid(row=2, column=4, sticky='ns')
t2.configure(yscrollcommand=sb.set)
sb.configure(command=t2.yview)

mainloop()
