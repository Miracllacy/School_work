import os
import zipfile as z
import time
from tkinter import *

a = "../resource/class/"
dir_name = "class.zip"
table = []
work_books = []
lessons = ['8:00——8:45', '8:50——9:35', '9:50——10:35', '10:40——11:25', '11:30——12:15', '13:00——13:45',
           '13:50——14:35', '14:45——15:30', '15:40——16:25', '16:35——17:20', '17:25——18:10', '18:30——19:15',
           '19:20——20:05', '20:10——20:55']
weeks = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]


# gotten: 增减及查询信息、课程表可视化
# Todo: 上传、下载资料 + 导入excel课程表 + 可视化


def initialize():
    global table
    global work_books
    global a
    global dir_name
    address = a + dir_name
    try:
        with z.ZipFile(address) as f:
            f.extractall(a)
            for name in f.namelist():
                # 中文标题转化
                real_name = name.encode('cp437').decode('gbk')
                os.rename(a + name, a + real_name)
        f.close()
    except FileNotFoundError:
        print("不存在压缩包")
    table, flag = search_file("table")
    work_books, flag = search_file("work")


def back_homepage():
    address = a + dir_name
    f = z.ZipFile(address, 'w', z.ZIP_DEFLATED)
    for n in os.listdir('../resource/class'):
        if not n == dir_name:
            address = os.path.join('../resource/class', n)
            f.write(address, n, z.ZIP_DEFLATED)
            os.remove(address)
    f.close()


def save(work, name):
    address = a + name + ".txt"
    f = open(address, 'w')
    for line in work:
        f.write(str(line))
        f.write("\n")
    print("{}保存成功".format(name))
    f.close()


def search_file(name):
    address = a + name + ".txt"
    work = []
    try:
        f = open(address)
        if not os.path.getsize(address) == 0:
            for line in f:
                if not line == "\n":
                    work.append(eval(line))
        f.close()
        return work, True
    except FileNotFoundError:
        f = open(address, 'w')
        f.close()
        print("不存在{}.txt，已创建".format(name))
        return work, False


def addition(item_name, items, add, temp):
    if add == "":
        return items
    else:
        new = {'time': temp, 'content': add}
        items[item_name].append(new)
        return items


def addition_all_work():
    temp = str(time.time())
    name = input('请输入所属课程名称:')
    state = input('请输入作业状态:')
    t_start = input('请输入作业开始时间:')
    t_end = input('请输入作业结束时间:')
    content = input('请输入作业内容:')
    card = {'name': name, 'flag': temp, 'state': state, 'start': t_start, 'end': t_end,
            'content': content}
    work_books.append(card)
    save(work_books, "work")
    new = {'state': state, 'time': temp}
    for n in table:
        if n['name'] == name:
            table.remove(n)
            n['work'].append(new)
            table.append(n)
            save(table, 'table')
            print("输入完毕")
            print(card)
            return
    course = {'name': name, 'time': [], 'place': [], 'teacher': [], 'text_t': [],
              'text_p': [], 'group': [], 'work': []}
    course['work'].append(new)
    table.append(course)
    save(table, 'table')


def addition_all_course():
    temp = str(time.time())
    name = input('请输入课程名称:')
    t_time = input('请输入课程时间:')
    place = input('请输入上课地点:')
    teacher = input('请输入课程教师:')
    text_t = input('请输入考试时间:')
    text_p = input('请输入考试地点:')
    group = input('请输入课程群:')
    course = {'name': name, 'time': [], 'place': [], 'teacher': [], 'text_t': [],
              'text_p': [], 'group': [], 'work': []}
    for card in table:
        if card['name'] == name:
            course = card
            table.remove(card)
    course = addition("time", course, t_time, temp)
    course = addition("place", course, place, temp)
    course = addition("teacher", course, teacher, temp)
    course = addition("text_t", course, text_t, temp)
    course = addition("text_p", course, text_p, temp)
    course = addition("group", course, group, temp)
    table.append(course)
    save(table, "table")


def modify_work(points, name):
    item = input('请输入应修改的项目:')
    wrong = input('请输入错误内容:')
    should = input('请输入正确内容:')
    for work in work_books:
        for point in points:
            if point['time'] == work['flag']:
                if work['name'] == name and work[item] == wrong:
                    work_books.remove(work)
                    work[item] = should
                    save(work_books, "work")
                    print("修改完毕")
                    return
    print("课程{}不存在该项作业".format(name))


def modify(item):
    name = input('请输入所属名称:')
    for card in table:
        if card['name'] == name:
            table.remove(card)
            if item == "work":
                modify_work(card['work'], name)
                table.append(card)
                return
            item = input('请输入应修改的项目:')
            wrong = input('请输入错误内容:')
            should = input('请输入正确内容:')
            for n in card[item]:
                if n['content'] == wrong:
                    card[item].remove(n)
                    n['content'] = should
                    card[item].append(n)
                    table.append(card)
                    save(table, "table")
                    print("修改完毕")
                    return
            print("{}的{}中不存在该内容".format(name, item))
            return
    print("不存在{}.txt".format(name))


def clean(items, temp, key):
    for item in items:
        if item[key] == temp:
            items.remove(item)
            return items
    if items:
        print("清理未完成")
    return items


def clean_work():
    name = input('请输入所属课程名称:')
    for course in table:
        if course['name'] == name:
            table.remove(course)
            n = input('请输入应删除的作业内容:')
            for card in course['work']:
                work_time = card['time']
                for work in work_books:
                    if work['flag'] == work_time and work['content'] == n:
                        work_books.remove(work)
                        course['work'].remove(card)
                        table.append(course)
                        save(work_books, "work")
                        save(table, "table")
                        return
            print("课程{}不存在{}的作业".format(name, n))
            return
    print("该课程无作业")


def clean_course():
    name = input('请输入课程名称:')
    for course in table:
        if course['name'] == name:
            course_should_time = input('请输入上课时间:')
            course_times = course['time']
            course_places = course['place']
            course_teachers = course['teacher']
            temp = ""
            for course_time in course_times:
                if course_time['content'] == course_should_time:
                    temp = course_time['time']
                    course_times.remove(course_time)
                    break
            if temp == "":
                break
            table.remove(course)
            course['place'] = clean(course_places, temp, 'time')
            course['teacher'] = clean(course_teachers, temp, 'time')
            table.append(course)
            save(table, "table")
            return
    print("不存在该课程")


def show_operation():
    print("1.新增作业内容")
    print("2.修改作业信息")
    print("3.删除作业信息")
    print("4.显示全部作业")
    print("5.新增课程内容")
    print("6.修改课程信息")
    print("7.删除课程信息")
    print("8.显示课程信息")
    print("9.显示课程表")
    print("0.退出系统")
    choice = input('请选择希望执行的操作:')
    return choice


def show_all_work():
    name = input('请输入所属课程名称:')
    print("显示{}课程的所有作业".format(name))
    print("开始时间 结束时间 内容 状态")
    i = 0
    for work in work_books:
        if work['name'] == name:
            i += 1
            print(work['start'], work['end'], work['content'], work['state'])
    if i == 0:
        print("资料库中不存在{}的作业信息，请进行添加".format(name))


def get_the_same_time(items, time_flag):
    flag = 0
    i = 0
    for item in items:
        if item['content']:
            flag = 1
        else:
            if flag == 0:
                i += 1
        if item['time'] == time_flag and item['content']:
            return item['content']
    if flag and items[i]['content']:
        return items[i]['content']
    else:
        return ""


def switch_course(course):
    cards = []
    flag = 0
    card = {'name': course['name']}
    for course_time in course['time']:
        temp = course_time['time']
        card['time'] = course_time['content']
        if card['time']:
            flag = 1
        card['place'] = get_the_same_time(course['place'], temp)
        card['teacher'] = get_the_same_time(course['teacher'], temp)
        card['text_t'] = get_the_same_time(course['text_t'], temp)
        card['text_p'] = get_the_same_time(course['text_p'], temp)
        card['group'] = get_the_same_time(course['group'], temp)
        cards.append(card)
        card = {'name': course['name']}
    if flag == 0:
        return []
    else:
        return cards


def show_all_course():
    cards = []
    for course in table:
        cards.append(switch_course(course))
    if cards == [[]]:
        print("不存在课程信息，请进行添加")
        return
    print("显示所有课程")
    print("课程名称 时间 地点 教师 考试时间 考试地点 课程群")
    for card in cards:
        for item in card:
            print(item['name'], item['time'], item['place'], item['teacher'],
                  item['text_t'], item['text_p'], item['group'])


def convert_to_digit(upper_digit):
    if upper_digit == "一":
        lower_digit = 1
    elif upper_digit == "二":
        lower_digit = 2
    elif upper_digit == "三":
        lower_digit = 3
    elif upper_digit == "四":
        lower_digit = 4
    elif upper_digit == "五":
        lower_digit = 5
    elif upper_digit == "六":
        lower_digit = 6
    elif upper_digit == "七" or upper_digit == "日":
        lower_digit = 7
    elif upper_digit == "八":
        lower_digit = 8
    elif upper_digit == "九":
        lower_digit = 9
    elif upper_digit == "十":
        lower_digit = 10
    else:
        lower_digit = 0
    return lower_digit


def get_time_cards(time_string):
    card = {'week': [], 'lesson': []}
    for i in range(len(time_string)):
        if time_string[i] == "星" and time_string[i + 1] == "期":
            card['week'] = convert_to_digit(time_string[i + 2])
        elif time_string[i - 1] == "、" or (time_string[i] == "第" and time_string[i + 2] == "节"):
            n = convert_to_digit(time_string[i + 1])
            if not time_string[i - 2] == "—" and not time_string[i - 1] == "—":
                card['lesson'].append(n)
            else:
                if abs(n - card['lesson'][-1]) == 1:
                    card['lesson'].append(n)
                else:
                    for j in range(n, card['lesson'][-1]):
                        card['lesson'].append(j)
    return card


def make_table():
    cards = []
    gotten_course = []
    course_table = Tk()  # 创建一个窗体
    course_table.title("课程表")
    course_table.geometry("770x680")  # 改变窗体的大小
    course_table.attributes('-topmost', True)  # 设置窗口置于顶层
    for i in range(7):
        # 星期几
        Label(course_table, text=weeks[i], width=12, height=1, bg="#7CCD7C").grid(row=0, column=i + 1)
    for i in range(14):
        # 第几节
        Label(course_table, text=lessons[i], width=15, height=2, bg="#7CCD7C").grid(row=i + 1, column=0)
    for course in table:
        # 将cards(即不同时间的同一种课)转换成单独的card，p.s. 列表嵌套列表再嵌套字典
        cards.append(switch_course(course))
    # 同一种课
    for card in cards:
        # 单独的课
        for item in card:
            # 得到具体时间，e.g. {'week':1,'lesson':[1,2]}
            time_card = get_time_cards(item['time'])
            new = item['name'] + '\n' + item['place'] + '\n' + item['teacher']
            week = time_card['week']
            for lesson in time_card['lesson']:
                if not lesson == 0:
                    gotten_course.append([lesson, week])
                    Button(course_table, text=new, width=12, height=3, font=("宋体", 8),
                           command=addition_all_course).grid(row=lesson, column=week)
    for i in range(1, 15):
        for j in range(1, 8):
            # only 填充空间
            if [i, j] not in gotten_course:
                Button(course_table, text="", width=12, height=2, command=addition_all_course).grid(row=i, column=j)
    # 进入消息循环
    course_table.mainloop()
