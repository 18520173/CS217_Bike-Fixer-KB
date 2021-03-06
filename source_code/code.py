import tkinter as tk
from tkinter import scrolledtext
from tkinter.ttk import *

class rule:
    gt = []
    kl = []
    flag = 0
    def __init__(self,lstgt,lstkl):
        self.gt = lstgt.copy()
        self.kl = lstkl.copy()
def fileevent(path_event):
    file_event = open(path_event,'r',encoding='utf-8')
    list_event = file_event.readlines()
    event = dict()
    for i in range(len(list_event)):
        temp = list_event[i].split(':')
        event[temp[0]] = temp[1][:-1]
    return event
def filerule(path_rules):#,path_hypo,path_goal):
    file_rules = open(path_rules)
    list_rules = file_rules.readlines()
    rules = []
    for i in range(len(list_rules)):
        temp = list_rules[i].split('/')
        new_rule = rule(list(temp[0].split()),list(temp[1].split()))
        rules.append(new_rule)
    file_rules.close()
    return rules
def addhypo1(rules_,event_,key_,value_):
    hypo = []
    hypo.append(key_)
    temp = []
    for i in range(len(rules_)):
        if check(hypo,rules_[i].gt) and rules_[i].flag != value_:
            add(temp,rules_[i].kl)
            rules_[i].flag = value_
    return hypo,temp
def addhypo2(rules_,event_,hypo,key_):
    hypo.append(key_)
    return hypo
def add(lst,lst1):
    for i in range(len(lst1)):
        if lst1[i] not in lst:
            lst.append(lst1[i])
def check(lst,lst1):
    for i in range(len(lst1)):
        if lst1[i] not in lst:
            return False
    return True
def forwardchaining(hypothesis_,rules_,value_):
    temp = []
    resolve = dict()
    while temp != hypothesis_:
        temp = hypothesis_.copy()
        for i in range(len(rules_)):
            if check(hypothesis_,rules_[i].gt) and rules_[i].flag != value_:
                add(hypothesis_,rules_[i].kl)
                lst_s = []
                for k in rules_[i].kl:
                    if k[0]=='S':
                        lst_s.append(k)
                if lst_s:
                    resolve[''.join(rules_[i].gt)] = lst_s
                rules_[i].flag = value_
    return resolve
def explanation(dict_,event_):
    f = open('solution.txt','w',encoding='utf-8')
    for i in dict_:
        f.write(event_[i]+'\n')
        for k in dict_[i]:
            f.write('-> '+event_[k]+'\n')
    f.close()
rules = filerule('rules.txt')
event = fileevent('event.txt')
temp = []
hypothesis = []
valu = 1
valu1 = 1
window = tk.Tk()
window.geometry('700x800')
window.title("fix your bike")
lbl = tk.Label(window,text="fix your bike",font=("Arial",28))
lbl.pack()
def clicked1():
    global hypothesis
    global temp
    global valu
    global valu1
    temp = []
    hypothesis = []
    valu *= -1
    valu1 *= -1
    window.geometry('700x800')
    lbl.pack()
    lbl1 = tk.Label(window,text="what's wrong",font=("Arial",14))
    lbl1.place(x=10,y=50)
    combo = Combobox(window)
    lstcobo = [event['A'],event['B'],event['C']]
    lstcobo2 = []
    combo['values']=(lstcobo)
    combo.place(x=10,y=100)
    def clicked():
        global hypothesis
        global lstcobo2
        value = 1
        for key,value in event.items():
            if combo.get()==value:
                hypothesis,temp = addhypo1(rules,event,key,valu)
                lstcobo2 = [event[i] for i in temp]
                lbl2 = tk.Label(window,text="failure part",font=("Arial",14))
                lbl2.place(x=160,y=50)
                combo2 = Combobox(window,width=47)
                combo2['values']=(lstcobo2)
                combo2.place(x=160,y=100)
                def clicked2():
                    global hypothesis
                    for key,value in event.items():
                        if combo2.get()==value:
                            hypothesis = addhypo2(rules,event,hypothesis,key)
                            solution = forwardchaining(hypothesis,rules,valu1)
                            explanation(solution,event)
                            txt = scrolledtext.ScrolledText(window,wrap = tk.WORD,width=80,height=30)
                            f = open('solution.txt','r',encoding='utf-8')
                            text_here = f.readlines()
                            for i in text_here:
                                txt.insert(tk.INSERT,i)
                            txt.configure(state ='disabled')
                            txt.place(x=0,y=200)
                            f.close()
                button2 = tk.Button(window,text="Accept",command=clicked2)
                button2.place(x=160,y=150)
    button = tk.Button(window,text="Accept",command=clicked)
    button.place(x=10,y=150)

button1 = tk.Button(window,text="Start",command=clicked1)
button1.place(x=650,y=10)
window.mainloop()
