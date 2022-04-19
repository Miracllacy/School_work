import os
import time
import zipfile as z
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import shutil

# Todo: add 远程服务器请求 "works"


def initialize():
    try:
        if not os.path.exists("../resource"):
            os.mkdir("../resource", 777)
        z_all = z.ZipFile("../resource/resource.zip")
        for name in z_all.namelist():
            if name[-1] == '/' and not os.path.exists(os.path.join("../resource", name)):
                os.makedirs(os.path.join("../resource", name))
            else:
                ext_filename = os.path.join("../resource", name)
                ext_dir = os.path.dirname(ext_filename)
                if not os.path.exists(ext_dir):
                    os.makedirs(ext_dir, 777)
                outfile = open(ext_filename, 'wb')
                outfile.write(z_all.read(name))
                outfile.close()
    except FileNotFoundError:
        messagebox.showinfo(title='警告', message="压缩包不存在！")

    global table
    table = search_file(a + "table.txt")
    global work_books
    work_books = search_file(a + "works.txt")
    global extras
    extras = search_file(a + "extras.txt")


def search_file(address):
    work = []
    try:
        f = open(address)
        if not os.path.getsize(address) == 0:
            for line in f:
                if not line == "\n":
                    work.append(eval(line))
        f.close()
        return work
    except FileNotFoundError:
        f = open(address, 'w')
        f.close()
        name = [s for s in address.split('/')]
        messagebox.showinfo(title='提示', message="不存在" + name[-1] + "，已创建")
        return work


def back_homepage():
    def compress():
        filelist = []
        other_dir = []
        if os.path.isfile("../resource"):
            filelist.append("../resource")
        else:
            for root, dirs, files in os.walk("../resource", topdown=False):
                if not files and not dirs:
                    filelist.append(root)
                for name in files:
                    filelist.append(os.path.join(root, name))
                if root == "../resource":
                    other_dir = dirs
        zf = z.ZipFile("../resource/resource.zip", "w", z.ZIP_DEFLATED)
        for tar in filelist:
            arc_name = tar[len("../resource"):]
            zf.write(tar, arc_name)
            if os.path.isfile(tar):
                os.remove(tar)
        for tar in filelist:
            if os.path.isdir(tar):
                os.rmdir(tar)
        for others in other_dir:
            if os.path.exists("../resource/" + others):
                temp = os.listdir("../resource/" + others)
                if temp:
                    for temp_path in temp:
                        os.rmdir("../resource/" + others + "/" + temp_path)
                os.rmdir("../resource/" + others)
        zf.close()

    curriculum_main.quit()
    if os.path.exists("../resource/resource.zip"):
        os.remove("../resource/resource.zip")
    compress()


def save(work, address, flag):
    f = open(address, 'w')
    for line in work:
        f.write(str(line))
        f.write("\n")
    if flag == 1:
        messagebox.showinfo(title='提示', message="文件保存成功")
    elif flag == 2:
        messagebox.showinfo(title='提示', message="文件上传成功")
    f.close()


# 格式:{'name': str, 'flag': str, 'state': str, 'start': str, 'end': str, 'content': str}
def add_works_base(contents, others):
    def input_work_books():
        works.withdraw()
        temp = str(time.time())
        name = entry1.get()
        state = s2.get()
        t_start = entry3.get()
        t_end = entry4.get()
        content = entry5.get()
        card = {'name': name, 'flag': temp, 'state': state, 'start': t_start, 'end': t_end,
                'content': content}
        if others[1] == "works":
            work_books.append(card)
            save(work_books, a + "works.txt", 1)
            if contents == {'课程名称': '', '状态': '', '开始时间': '', '结束时间': '', '内容': ''}:
                for n in table:
                    if n['name'] == name:
                        table.remove(n)
                        n['work'].append(temp)
                        table.append(n)
                        save(table, a + 'table.txt', 0)
                        return
                course = {'name': name, 'time': [], 'place': [], 'teacher': [], 'text_t': [],
                          'text_p': [], 'group': [], 'work': []}
                course['work'].append(temp)
                table.append(course)
                save(table, a + 'table.txt', 0)
            show_work(others, work_books)
        elif others[1] == "extras":
            extras.append(card)
            save(extras, a + "extras.txt", 1)
            show_work(others, extras)

    works = tk.Toplevel()
    works.title("新增" + others[2] + "内容")
    works.geometry("250x200+500+400")
    works.attributes('-topmost', True)
    tk.Label(works, text="").grid(row=0, column=1)
    tk.Label(works, text="    ").grid(row=4, column=0, rowspan=7)
    tk.Label(works, text=others[0] + ":").grid(row=1, column=1)
    tk.Label(works, text="状态:").grid(row=2, column=1)
    tk.Label(works, text="开始时间:").grid(row=3, column=1)
    tk.Label(works, text="结束时间:").grid(row=4, column=1)
    tk.Label(works, text="内容:").grid(row=5, column=1)
    # 课程名称
    entry1 = tk.Entry(works, width=20)
    entry1.grid(row=1, column=2, columnspan=5)
    # 作业状态
    s2 = tk.Spinbox(works, values=('未完成', '已完成', '进行中',), width=18)
    s2.grid(row=2, column=2, columnspan=5)
    # 开始时间
    entry3 = tk.Entry(works, width=20)
    entry3.grid(row=3, column=2, columnspan=5)
    # 结束时间
    entry4 = tk.Entry(works, width=20)
    entry4.grid(row=4, column=2, columnspan=5)
    # 作业内容
    entry5 = tk.Entry(works, width=20)
    entry5.grid(row=5, column=2, columnspan=5)
    if not contents == {others[0]: '', '状态': '', '开始时间': '', '结束时间': '', '内容': ''}:
        entry1.insert(0, contents[others[0]])
        entry3.insert(0, contents['开始时间'])
        entry4.insert(0, contents['结束时间'])
        entry5.insert(0, contents['内容'])
        v = tk.StringVar()
        s2.config(textvariable=v)
        v.set(contents['状态'])
    tk.Button(works, text="完成", command=input_work_books).grid(row=7, column=1)
    tk.Button(works, text="退出", command=works.withdraw).grid(row=7, column=4)


# 格式:{'time':[], 'content': str}
def addition(string, course, add, temp):
    if add == "":
        return course
    else:
        for item in course[string]:
            if item['content'] == add:
                course[string].remove(item)
                item['time'].append(temp)
                course[string].append(item)
                return course
        new = {'time': [temp], 'content': add}
        course[string].append(new)
        return course


# 格式:{'name': str, 'time': [{}, {}], 'place': [{}, {}], 'teacher': [{}, {}], 'text_t': [{}, {}],
#                   'text_p': [{}, {}], 'group': [{}, {}], 'work': [str, str]}
def add_course_base(content):
    def input_table():
        courses.withdraw()
        temp = str(time.time())
        t_time = {'week': s21.get(), 'lesson': []}
        for i in range(int(s22.get()), int(s23.get()) + 1):
            t_time['lesson'].append(i)
        name = entry1.get()
        place = entry3.get()
        teacher = entry4.get()
        text_t = entry5.get()
        text_p = entry6.get()
        group = entry7.get()
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
        save(table, a + "table.txt", 1)
        show_course()

    def warning_out():
        messagebox.showwarning(title='警告', message='超出范围')
        return False

    courses = tk.Toplevel()
    courses.title("新增课程信息")
    courses.geometry("330x240+500+400")
    courses.attributes('-topmost', True)
    tk.Label(courses, text="").grid(row=0, column=1)
    tk.Label(courses, text="    ").grid(row=4, column=0, rowspan=7)
    tk.Label(courses, text="课程名称:").grid(row=1, column=1)
    tk.Label(courses, text="上课时间:").grid(row=2, column=1)
    tk.Label(courses, text="上课地点:").grid(row=3, column=1)
    tk.Label(courses, text="课程教师:").grid(row=4, column=1)
    tk.Label(courses, text="考试时间:").grid(row=5, column=1)
    tk.Label(courses, text="考试地点:").grid(row=6, column=1)
    tk.Label(courses, text="课程群:").grid(row=7, column=1)
    entry1 = tk.Entry(courses, width=30)
    entry1.grid(row=1, column=2, columnspan=8)
    # 星期几
    s21 = tk.Spinbox(courses, values=tuple(weeks), width=5, invalidcommand=warning_out)
    s21.grid(row=2, column=2)
    # 第几节开始
    tk.Label(courses, text="第", width=1).grid(row=2, column=3)
    s22 = tk.Spinbox(courses, from_=1, to=14, increment=1, width=2, invalidcommand=warning_out)
    s22.grid(row=2, column=4)
    tk.Label(courses, text="节", width=1).grid(row=2, column=5)
    tk.Label(courses, text="—", width=1).grid(row=2, column=6)
    # 第几节结束
    tk.Label(courses, text="第", width=1).grid(row=2, column=7)
    s23 = tk.Spinbox(courses, from_=1, to=14, increment=1, width=2, invalidcommand=warning_out)
    s23.grid(row=2, column=8)
    tk.Label(courses, text="节", width=1).grid(row=2, column=9)
    entry3 = tk.Entry(courses, width=30)
    entry3.grid(row=3, column=2, columnspan=8)
    entry4 = tk.Entry(courses, width=30)
    entry4.grid(row=4, column=2, columnspan=8)
    entry5 = tk.Entry(courses, width=30)
    entry5.grid(row=5, column=2, columnspan=8)
    entry6 = tk.Entry(courses, width=30)
    entry6.grid(row=6, column=2, columnspan=8)
    entry7 = tk.Entry(courses, width=30)
    entry7.grid(row=7, column=2, columnspan=8)
    if not content == {'课程名称': "", '星期': "", '节数': [1], '地点': '', '教师': '', '考试时间': '', '考试地点': '', '课程群': ''}:
        entry1.insert(0, content['课程名称'])
        entry3.insert(0, content['地点'])
        entry4.insert(0, content['教师'])
        entry5.insert(0, content['考试时间'])
        entry6.insert(0, content['考试地点'])
        entry7.insert(0, content['课程群'])
        v21 = tk.StringVar()
        v22 = tk.StringVar()
        v23 = tk.StringVar()
        s21.config(textvariable=v21)
        s22.config(textvariable=v22)
        s23.config(textvariable=v23)
        v21.set(content['星期'])
        v22.set(content['节数'][0])
        v23.set(content['节数'][-1])
    tk.Button(courses, text="完成", command=input_table).grid(row=8, column=2)
    tk.Button(courses, text="退出", command=courses.withdraw).grid(row=8, column=6)


def add_all():
    def add_extra():
        temp = {'活动名称': '', '状态': '', '开始时间': '', '结束时间': '', '内容': ''}
        add_works_base(temp, ["活动名称", "extras", "活动"])

    def add_course():
        temp = {'课程名称': "", '星期': "", '节数': [1], '地点': '', '教师': '', '考试时间': '', '考试地点': '', '课程群': ''}
        add_course_base(temp)

    def add_work():
        temp = {'课程名称': '', '状态': '', '开始时间': '', '结束时间': '', '内容': ''}
        add_works_base(temp, ["课程名称", "works", "作业"])

    add_ = tk.Toplevel()
    add_.title("新增信息")
    add_.geometry("270x210+500+400")
    add_.attributes('-topmost', True)
    tk.Button(add_, command=add_extra, width=20, height=2, text="新增课外活动", font=font[0]).place(x=40, y=20)
    tk.Button(add_, command=add_course, width=20, height=2, text="新增课程信息", font=font[0]).place(x=40, y=70)
    tk.Button(add_, command=add_work, width=20, height=2, text="新增作业信息", font=font[0]).place(x=40, y=120)


def delete_course_base(content):
    def delete_item(items):
        for it in items:
            if it['time'] == temp:
                return items.remove(it)
        return items

    if not type(content['节数']) == list:
        content['节数'] = content['节数'].replace("第", "")
        content['节数'] = content['节数'].replace("节", "")
        content['节数'] = content['节数'].replace(" ", "")
        content['节数'] = [int(s) for s in content['节数'].split(',')]
    for courses in table:
        if courses['name'] == content['课程名称']:
            for t in courses['time']:
                if t['content'] == {'week': content['星期'], 'lesson': content['节数']}:
                    temp = t['time']
                    table.remove(courses)
                    courses['time'].remove(t)
                    courses['place'] = delete_item(courses['place'])
                    courses['teacher'] = delete_item(courses['teacher'])
                    courses['text_t'] = delete_item(courses['text_t'])
                    courses['text_p'] = delete_item(courses['text_p'])
                    courses['group'] = delete_item(courses['group'])
                    table.append(courses)
                    save(table, a + "table.txt", 1)
                    return


def delete_work_base(content):
    for works in work_books:
        if works['name'] == content['课程名称']:
            if works['content'] == content['内容']:
                work_books.remove(works)
                save(work_books, a + "works.txt", 1)
                for courses in table:
                    for flag in courses['work']:
                        if flag == works['flag']:
                            table.remove(courses)
                            courses['work'].remove(flag)
                            table.append(courses)
                            save(table, a + "table.txt", 0)
                            return
                return


def delete_extra_base(content):
    for card in extras:
        if card['name'] == content['活动名称'] and card['content'] == content['内容']:
            extras.remove(card)
            return


def switch_course(course):
    def get_the_same_time(items, time_flag):
        flags = 0
        i = 0
        for item in items:
            if item['content']:
                flags = 1
            else:
                if flags == 0:
                    i += 1
            # 内容存在
            if item['content']:
                for item_time in item['time']:
                    if item_time == time_flag:
                        return item['content']
        if flags and items[i]['content']:
            return items[i]['content']
        else:
            return ""

    cards = []
    card = {'name': course['name']}
    for course_time in course['time']:
        temp = course_time['time']
        card['week'] = course_time['content']['week']
        card['lesson'] = course_time['content']['lesson']
        card['place'] = get_the_same_time(course['place'], temp)
        card['teacher'] = get_the_same_time(course['teacher'], temp)
        card['text_t'] = get_the_same_time(course['text_t'], temp)
        card['text_p'] = get_the_same_time(course['text_p'], temp)
        card['group'] = get_the_same_time(course['group'], temp)
        cards.append(card)
        card = {'name': course['name']}
    return cards
# 格式:[{'name', 'week', 'lesson':[int, ], 'place', 'teacher', 'text_t', 'text_p', 'group'}, {}]


def upload_base(content):
    old_path = filedialog.askopenfilename(title="选择文件")
    temp = [s for s in old_path.split('/')]
    new_path = "../resource/accessory/" + content + "/" + temp[-1]
    shutil.copyfile(old_path, new_path)


# {'课程名称', '星期', '节数', '地点', '教师', '考试时间', '考试地点', '课程群'}
def show_course():
    def add_course():
        temp = {'课程名称': "", '星期': "", '节数': [1], '地点': '', '教师': '', '考试时间': '', '考试地点': '', '课程群': ''}
        add_course_base(temp)
        all_course.withdraw()

    def delete_course():
        selected_id = tree.selection()[0]
        selected_content = tree.set(selected_id)
        tree.delete(selected_id)
        delete_course_base(selected_content)
        all_course.withdraw()

    def edit_course():
        selected_id = tree.selection()[0]
        selected_content = tree.set(selected_id)
        delete_course_base(selected_content)
        add_course_base(selected_content)
        all_course.withdraw()

    def upload_course_file():
        upload_base("courses")

    all_course = tk.Toplevel()
    all_course.title("课程信息")
    all_course.geometry("850x540+200+100")
    all_course.attributes('-topmost', True)
    cards = []
    for course in table:
        cards.append(switch_course(course))
    if cards == [[]] or cards == []:
        messagebox.showinfo(title='提示', message="不存在课程信息，请进行添加")
        all_course.withdraw()
        return
    scroll = ttk.Scrollbar(all_course, orient='vertical')
    tree = ttk.Treeview(all_course, show="headings", height=20, yscrollcommand=scroll.set)
    scroll.config(command=tree.yview)
    tree['column'] = ('课程名称', '星期', '节数', '地点', '教师', '考试时间', '考试地点', '课程群')
    for n in tree['column']:
        tree.column(n, width=100, anchor="center")  # 设置列
        tree.heading(n, text=n)  # 设置显示的表头名
    for card in cards:
        for item in card:
            if not item['lesson'] == []:
                item['lesson'] = "第" + str(item['lesson'])[1:-1] + "节"
            value = tuple(item.values())
            tree.insert("", "end", values=value)
    tree.place(x=20, y=25)
    scroll.place(x=830, y=25, height=425)
    tk.Button(all_course, command=upload_course_file, width=8, height=2, text="上传附件", font=font[0]).place(x=120, y=480)
    tk.Button(all_course, command=add_course, width=8, height=2, text="新增", font=font[0]).place(x=240, y=480)
    tk.Button(all_course, command=edit_course, width=8, height=2, text="编辑", font=font[0]).place(x=360, y=480)
    tk.Button(all_course, command=delete_course, width=8, height=2, text="删除", font=font[0]).place(x=480, y=480)
    tk.Button(all_course, command=all_course.withdraw, width=8, height=2, text="退出", font=font[0]).place(x=600, y=480)


# ('课程名称', '状态', '开始时间', '结束时间', '内容')
def show_work(others, files):
    def add_works():
        temp = {others[0]: '', '状态': '', '开始时间': '', '结束时间': '', '内容': ''}
        add_works_base(temp, others)
        all_work.withdraw()

    def delete_works():
        selected_id = tree.selection()[0]
        selected_content = tree.set(selected_id)
        tree.delete(selected_id)
        if others[1] == "works":
            delete_work_base(selected_content)
        elif others[1] == "extras":
            delete_extra_base(selected_content)
        all_work.withdraw()

    def edit_works():
        selected_id = tree.selection()[0]
        selected_content = tree.set(selected_id)
        if others[1] == "works":
            delete_work_base(selected_content)
        elif others[1] == "extras":
            delete_extra_base(selected_content)
        add_works_base(selected_content, others)
        all_work.withdraw()

    def upload_work_file():
        upload_base(others[1])

    all_work = tk.Toplevel()
    all_work.title(others[2] + "信息")
    all_work.geometry("750x540+200+100")
    all_work.attributes('-topmost', True)
    if not files:
        messagebox.showinfo(title='提示', message="不存在" + others[2] + "信息，请进行添加")
        return
    scroll = ttk.Scrollbar(all_work, orient='vertical')
    tree = ttk.Treeview(all_work, show="headings", height=20, yscrollcommand=scroll.set)
    scroll.config(command=tree.yview)
    tree['column'] = (others[0], '状态', '开始时间', '结束时间', '内容')
    for n in tree['column']:
        if n == '内容':
            tree.column(n, width=300, anchor="center")  # 设置列
        else:
            tree.column(n, width=100, anchor="center")
        tree.heading(n, text=n)  # 设置显示的表头名
    for work in files:
        temp_work = {'name': work['name'], 'state': work['state'], 'start': work['start'], 'end': work['end'],
                     'content': work['content']}
        value = tuple(temp_work.values())
        tree.insert("", "end", values=value)
    tree.place(x=20, y=25)
    scroll.place(x=730, y=25, height=425)
    tk.Button(all_work, command=upload_work_file, width=8, height=2, text="上传附件", font=font[0]).place(x=80, y=480)
    tk.Button(all_work, command=add_works, width=8, height=2, text="新增", font=font[0]).place(x=200, y=480)
    tk.Button(all_work, command=edit_works, width=8, height=2, text="编辑", font=font[0]).place(x=320, y=480)
    tk.Button(all_work, command=delete_works, width=8, height=2, text="删除", font=font[0]).place(x=440, y=480)
    tk.Button(all_work, command=all_work.withdraw, width=8, height=2, text="退出", font=font[0]).place(x=560, y=480)


# {'课程名称': , '星期': , '节数': [int, ], '地点': '', '教师': '', '考试时间': '', '考试地点': '', '课程群': ''}
def make_table():
    def add_course_all():
        temp = {'课程名称': '', '星期': '', '节数': [1], '地点': '', '教师': '', '考试时间': '',
                '考试地点': '', '课程群': ''}
        add_course_base(temp)
        class_schedule.withdraw()

    class_schedule = tk.Toplevel()
    class_schedule.title("课程表")
    class_schedule.geometry("770x685+200+100")
    class_schedule.attributes('-topmost', True)
    cards = []
    gotten_course = []
    for i in range(len(weeks)):
        # 星期几
        tk.Label(class_schedule, text=weeks[i], width=12, height=1, bg=color[2]).grid(row=0, column=i + 1)
    for i in range(len(lessons)):
        # 第几节
        tk.Label(class_schedule, text=lessons[i], width=15, height=2, bg=color[2]).grid(row=i + 1, column=0)
    for course in table:
        # 将cards(即不同时间的同一种课)转换成单独的card，p.s. 列表嵌套列表再嵌套字典
        cards.append(switch_course(course))
    # 同一种课
    for card in cards:
        # 单独的课
        for item in card:
            new = item['name'] + '\n' + item['place'] + '\n' + item['teacher']
            for lesson in item['lesson']:
                if not lesson == 0:  # int型
                    gotten_course.append([lesson, weeks.index(item['week']) + 1])
                    tk.Button(class_schedule, text=new, width=12, height=3, font=font[1], bg=color[3],
                              command=add_course_all).grid(row=lesson, column=weeks.index(item['week']) + 1)
    for i in range(1, 15):
        for j in range(1, 8):
            # only 填充空间
            if [i, j] not in gotten_course:
                tk.Button(class_schedule, text="", width=12, height=2, command=add_course_all).grid(row=i, column=j)


def main():
    def trick_it():
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        l1.config(text=current_time)
        curriculum_main.update()
        l1.after(1000, trick_it)

    def show_works():
        show_work(["课程名称", "works", "作业"], work_books)

    def show_extras():
        show_work(["活动名称", "extras", "活动"], extras)

    curriculum_main.title("课程信息管理和查询")
    curriculum_main.geometry("1200x750+150+60")  # 改变窗体的大小
    curriculum_main.attributes('-topmost', True)  # 设置窗口置于顶层
    background_img = Image.open(image_address + "background.gif").resize((1200, 750))
    background = ImageTk.PhotoImage(background_img)
    button_img = Image.open(image_address + "3.gif").resize((160, 30))
    button_image = ImageTk.PhotoImage(button_img)
    clock_img = Image.open(image_address + "label.gif").resize((300, 60))
    clock_image = ImageTk.PhotoImage(clock_img)
    curriculum_main.iconbitmap(image_address + "icon.ico")
    tk.Label(curriculum_main, image=background).place(x=0, y=0)
    b1 = tk.Button(curriculum_main, command=show_extras, image=button_image, bg=color[0], width=160, height=30)
    b1.config(text="课外信息", compound=tk.CENTER, fg=color[1], font=font[0])
    b1.place(x=200, y=250)
    b1 = tk.Button(curriculum_main, command=show_course, image=button_image, bg=color[0], width=160, height=30)
    b1.config(text="课程信息", compound=tk.CENTER, fg=color[1], font=font[0])
    b1.place(x=200, y=300)
    b2 = tk.Button(curriculum_main, command=show_works, image=button_image, bg=color[0], width=160, height=30)
    b2.config(text="作业信息", compound=tk.CENTER, fg=color[1], font=font[0])
    b2.place(x=200, y=350)
    b3 = tk.Button(curriculum_main, command=make_table, image=button_image, bg=color[0], width=160, height=30)
    b3.config(text="课程表", compound=tk.CENTER, fg=color[1], font=font[0])
    b3.place(x=200, y=400)
    b12 = tk.Button(curriculum_main, command=add_all, image=button_image, bg=color[0], width=160, height=30)
    b12.config(text="新增", compound=tk.CENTER, fg=color[1], font=font[0])
    b12.place(x=200, y=450)
    b0 = tk.Button(curriculum_main, command=back_homepage, image=button_image, bg=color[0], width=160, height=30)
    b0.config(text="退出", compound=tk.CENTER, fg=color[1], font=font[0])
    b0.place(x=200, y=500)
    l1 = tk.Label(image=clock_image, bg="black", text=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    l1.config(font=("Ink free", 16, "bold"), compound=tk.CENTER)
    l1.place(x=810, y=60)
    l1.after(1000, trick_it)
    curriculum_main.mainloop()


if __name__ == "__main__":
    a = "../resource/record/"
    dir_name = "class.zip"
    image_address = "../resource/images/"
    # 按钮背景， 操作字体， 课程表星期, 课程表
    color = ["#1661ab", "#d0dfe6", "#7CCD7C", "#2bae85"]
    # 操作字体, 课程表字体
    font = [("华文新魏", 12), ("宋体", 8)]
    table = []
    work_books = []
    extras = []
    lessons = ['8:00——8:45', '8:50——9:35', '9:50——10:35', '10:40——11:25', '11:30——12:15', '13:00——13:45',
               '13:50——14:35', '14:45——15:30', '15:40——16:25', '16:35——17:20', '17:25——18:10', '18:30——19:15',
               '19:20——20:05', '20:10——20:55']
    weeks = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    curriculum_main = tk.Tk()  # 创建一个窗体
    initialize()
    main()
