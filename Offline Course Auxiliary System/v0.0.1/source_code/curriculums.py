import os
import zipfile as z

a = "../resource/class/"
dir_name = "class.zip"
column = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]

doing = []
done = []
undone = []
table = []


# 已废弃


def initialize():
    global doing
    global done
    global undone
    global table
    global a
    global dir_name
    address = a + dir_name
    try:
        with z.ZipFile(address) as f:
            f.extractall(a)
            for name in f.namelist():
                real_name = name.encode('cp437').decode('gbk')
                os.rename(a + name, a + real_name)
        f.close()
    except FileNotFoundError:
        print("不存在压缩包")
    doing, flag = search_file("doing")
    done, flag = search_file("done")
    undone, flag = search_file("undone")
    table, flag = search_file("table")


def back_homepage():
    address = a + dir_name
    f = z.ZipFile(address, 'w', z.ZIP_DEFLATED)
    for n in os.listdir('../resource/class'):
        if not n == dir_name:
            address = os.path.join('../resource/class', n)
            f.write(address, n, z.ZIP_DEFLATED)
            os.remove(address)
    f.close()


def judge(items, i):
    i = int(i)
    if i == 1:
        limit = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    elif i == 2:
        limit = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] + [':', '-']
    elif i == 3:
        limit = ["课程名称", "序号", "作业开始时间", "作业结束时间", "作业内容"]
    elif i == 4:
        limit = ['name', 'i', 'start', 'end', 'content']
    elif i == 5:
        limit = column
        if items in limit:
            return True
    else:
        print("输入格式错误")
        return
    for item in items:
        if item not in limit:
            print("输入格式错误")
            return False
    return True


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


def addition_all_work():
    name = input('请输入所属课程名称:')
    work, flag = search_file(name)
    i = str(len(work) + 1)
    t_start = input('请输入作业开始时间:')
    if not judge(t_start, 2):
        return
    t_end = input('请输入作业结束时间:')
    if not judge(t_end, 2):
        return
    content = input('请输入作业内容:')
    card = {'name': name, 'i': i, 'start': t_start, 'end': t_end, 'content': content}
    work.append(card)
    undone.append(card)
    save(work, name)
    save(undone, "undone")
    print("输入完毕")
    print(card)


def addition_all_course():
    name = input('请输入课程名称:')
    t_week = input('请输入星期几:')
    if not judge(t_week, 5):
        return
    t_time = input('请输入第几节:')
    if not judge(t_time, 1):
        return
    place = input('请输入上课地点:')
    teacher = input('请输入课程教师:')
    text_t = input('请输入考试时间:')
    if not judge(text_t, 2):
        return
    text_p = input('请输入考试地点:')
    group = input('请输入课程群:')
    card = {'name': name, 'week': t_week, 'time': t_time, 'place': place,
            'teacher': teacher, 'text_t': text_t, 'text_p': text_p, 'group': group}
    table.append(card)
    save(table, "table")


def modify(n):
    name = input('请输入所属名称:')
    work, flag = search_file(name)
    if not flag:
        return
    s = input('请输入应修改的内容:')
    if judge(s, 2) is False and judge(s, 5) is False:
        return
    for card in work:
        if card['name'] == name and card[n] == s:
            item = input('请输入应修改的项目:')
            if judge(item, 3) is False and judge(item, 4) is False:
                return
            should = input('请输入该项目的正确内容:')
            card[item] = should
            print("修改完毕")
            save(work, name)
            return
    print("不存在{}.txt".format(name))


def clean_work():
    name = input('请输入所属课程名称:')
    work, flag = search_file(name)
    if not flag or len(work) == 0:
        print("课程{}不存在作业".format(name))
        return
    i = int(input('请输入应删除的作业:'))
    done.append(work[i - 1])
    save(done, "done")
    if work[i - 1] in doing:
        doing.remove(work[i - 1])
        save(doing, "doing")
    if work[i - 1] in undone:
        undone.remove(work[i - 1])
        save(undone, "undone")
    del work[i - 1]
    save(work, name)
    print("已删除{}第{}项作业".format(name, i))


def clean_course():
    name = input('请输入课程名称:')
    week = input('请输入上课时间:')
    for card in table:
        if card['name'] == name and card['week'] == week:
            table.remove(card)
            print("删除完毕")
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
    work, flag = search_file(name)
    if not flag or len(work) == 0:
        print("资料库中不存在{}的作业信息，请进行添加".format(name))
        return
    print("显示所有课程")
    print("课程名称 序号 开始时间 结束时间 内容")
    for card in work:
        print(card['name'], card['i'], card['start'], card['end'], card['content'])


def show_all_course():
    work, flag = search_file('table')
    if not flag or len(work) == 0:
        print("资料库中不存在课程信息，请进行添加")
        return
    print("显示所有课程")
    print("课程名称 星期 时间 地点 教师 考试时间 考试地点 课程群")
    for n in work:
        print(n['name'], n['week'], n['time'], n['place'], n['teacher'], n['text_t'], n['text_p'], n['group'])

