from tkinter import *
import os
table = []

def initialize():
    address = "../resource/class/table.txt"
    global table
    try:
        f = open(address,"r")
        if not os.path.getsize(address) == 0:
            for line in f:
                if not line == "\n":
                    table.append(eval(line))
        f.close()
        return True
    except FileNotFoundError:
        f = open(address, "w")
        f.close()
        return False


def back_homepage():
    address = "../resource/class/table.txt"
    f = open(address,'w')
    for line in table:
        f.write(str(line))
        f.write("\n")
    f.close()


def show_operation():
    print("1.新增课程内容")
    print("2.修改课程信息")
    print("3.删除课程信息")
    print("4.显示课程表")
    print("0.退出系统")
    choice = input('请选择希望执行的操作:')
    return choice


def addition_all():
    name = input('请输入课程名称:')
    t_time = input('请输入上课时间:')
    place = input('请输入上课地点:')
    teacher = input('请输入课程教师:')
    text_t = input('请输入考试时间:')
    text_p = input('请输入考试地点:')
    group = input('请输入课程群:')
    card = {'name':name,'time':t_time,'place':place,'teacher':teacher,'text_t':text_t,'text_p':text_p,'group':group}
    table.append(card)


def modify():
    name = input('请输入课程名称:')
    time = input('请输入上课时间:')
    item = input('请输入所改项目:')
    should = input('请输入正确内容:')
    for card in table:
        if card['name'] == name and card['time'] == time:
            card[item] = should
            print("修改完毕")
            return
    print("不存在该课程，请进行添加")


def clean():
    name = input('请输入课程名称:')
    time = input('请输入上课时间:')
    for card in table:
        if card['name'] == name and card['time'] == time:
            table.remove(card)
            print("删除完毕")
            return
    print("不存在该课程")


def make_table(flag):
    print("该项功能未完成")
    if not flag:
        return
    week = ['星期一','星期二','星期三','星期四','星期五','星期六','星期日']
    y = {}
    top = Tk()  # 创建一个窗体
    top.geometry("1100x400+200+50")
    for card in table:
        x = week.index(card['time'])
        if card['time'] in y:
            y[card['time']] += 1
        else:
            y[card['time']] = 0
        text = Text(top, width=30, height=5)  # 创建一个文本控件
        text.place(x=x * 215 + 10, y=y[card['time']] * 70 + 20)  # 在屏幕上放置文本控件
        text.insert(INSERT,card)  # 在控件上放置文本
    top.mainloop()
