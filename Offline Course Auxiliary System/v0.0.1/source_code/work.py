import os
import zipfile as z
a = "../resource/class/"
dir_name = "class.zip"
s_limit = ['0','1','2','3','4','5','6','7','8','9']
t_limit = s_limit + [':','-']
item_limit = ["课程名称","序号","作业开始时间","作业结束时间","作业内容"]
item_limit_other = ['name','i','start','end','content']

doing = []
done = []
undone = []


def judge(items,limit):
    for item in items:
        if item not in limit:
            print("输入格式错误")
            return False
    return True


def save(work,name):
    address = a + name + ".txt"
    f = open(address,'w')
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
        for line in f:
            work.append(eval(line))
        f.close()
        return work,True
    except FileNotFoundError:
        f = open(address,'w')
        f.close()
        print("不存在{}.txt，已创建".format(name))
        return work,False


def addition_all():
    name = input('请输入所属课程名称:')
    work,flag = search_file(name)
    i = len(work) + 1
    t_start = input('请输入作业开始时间:')
    if not judge(t_start,t_limit):
        return
    t_end = input('请输入作业结束时间:')
    if not judge(t_end,t_limit):
        return
    content = input('请输入作业内容:')
    card = {'name':name,'i':i,'start':t_start,'end':t_end,'content':content}
    work.append(card)
    undone.append(card)
    save(work,name)
    save(undone,"undone")
    print("输入完毕")
    print(card)


def modify():
    name = input('请输入所属课程名称:')
    work,flag = search_file(name)
    if not flag:
        return
    s = input('请输入应修改的作业:')
    if not judge(s,s_limit):
        return
    for card in work:
        if card['name'] == name and card['i'] == int(s):
            item = input('请输入应修改的项目:')
            if judge(item,item_limit) is False and judge(item,item_limit_other) is False:
                return
            should = input('请输入该项目的正确内容:')
            card[item] = should
            print("修改完毕")
            save(work,name)
            return
    print("不存在该项作业")


def clean():
    name = input('请输入所属课程名称:')
    work,flag = search_file(name)
    if not flag or len(work) == 0:
        print("课程{}不存在作业".format(name))
        return
    i = int(input('请输入应删除的作业:'))
    done.append(work[i-1])
    save(done,"done")
    if work[i-1] in doing:
        doing.remove(work[i-1])
        save(doing,"doing")
    if work[i-1] in undone:
        undone.remove(work[i-1])
        save(undone,"undone")
    del work[i-1]
    save(work,name)
    print("已删除{}第{}项作业".format(name,i))


def show_operation():
    print("1.新增作业内容")
    print("2.修改作业信息")
    print("3.删除作业信息")
    print("4.显示全部作业")
    print("0.退出系统")
    choice = input('请选择希望执行的操作:')
    return choice


def show_all():
    name = input('请输入所属课程名称:')
    work,flag = search_file(name)
    if not flag or len(work) == 0:
        print("资料库中不存在{}的作业信息，请进行添加".format(name))
        return
    print("显示所有作业")
    print("课程名称 序号 开始时间 结束时间 内容")
    for card in work:
        print(card['name'],card['i'],card['start'],card['end'],card['content'])


def initialize():
    global doing
    global done
    global undone
    global t_limit
    global s_limit
    global item_limit
    global item_limit_other
    global a
    global dir_name
    address = a + dir_name
    try:
        with z.ZipFile(address) as f:
            f.extractall(a)
            for name in f.namelist():
                real_name = name.encode('cp437').decode('gbk')
                os.rename(a+name,a+real_name)
        f.close()
    except FileNotFoundError:
        print("不存在压缩包")
    doing,flag = search_file("doing")
    done,flag = search_file("done")
    undone,flag = search_file("undone")


def back_homepage():
    address = a + dir_name
    f = z.ZipFile(address,'w',z.ZIP_DEFLATED)
    for n in os.listdir('../resource/class'):
        if not n == dir_name:
            address = os.path.join('../resource/class',n)
            f.write(address,n,z.ZIP_DEFLATED)
            os.remove(address)
    f.close()
