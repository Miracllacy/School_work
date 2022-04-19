st = []
address = "./student.txt"
limit_score = 3
limit_house = 3
limit_phone = 11
limit_sex = ['男','女']
limit_count = ['1','2','3','4','5','6','7','8','9','0']

def is_not_CN(name):  # 判断是否为中文
    for n in name:
        if '\u4e00' <= n <='\u9fff':
            return False
    return True


def judge_digit(content):
    for n in content:
        if n not in limit_count:
            return False
    return True


def initialize():
    global st
    try:
        f = open(address)
        for line in f:
            st.append(eval(line))
        f.close()
        return True
    except FileNotFoundError:
        f = open(address,'w')
        f.close()
        return False


def show_operation():
    print('*' * 50)
    print("欢迎使用【宿舍管理系统】")
    print("1.查找学生")
    print("2.新增学生")
    print("3.显示全部")
    print("0.退出系统")
    print('*' * 50)
    choice = input('请选择希望执行的操作:')
    return choice


def search():  # only学号
    print('-' * 50)
    print("查找学生")
    if len(st) == 0:
        print("资料库中不存在学生信息，请进行添加")
    num = input('请输入要搜索的学号:')
    if not len(num) == limit_score or not judge_digit(num):
        print("学号格式错误")
        return
    for card in st:
        if num == card['score']:
            print("学号 姓名 性别 房间号 电话")
            print('=' * 50)
            print(card['score'],card['name'],card['sex'],card['house'],card['phone'])
            return
    print("资料库中不存在学生信息，请进行添加")


def join_in():
    print('-' * 50)
    print("新增学生")
    score = input('请输入学号:')
    if not len(score) == limit_score or not judge_digit(score):
        print("学号格式错误")
        return
    name = input('请输入姓名:')
    if is_not_CN(name):
        print("姓名格式错误")
        return
    sex = input('请输入性别:')
    if sex not in limit_sex:
        print("无该性别")
        return
    house = input('请输入房间号:')
    if not len(house) == limit_house or not judge_digit(house):
        print("房间号格式错误")
        return
    phone = input('请输入电话:')
    if not len(phone) == limit_phone or not judge_digit(phone):
        print("电话格式错误")
        return
    card = {'score':score,'name':name,'sex':sex,'house':house,'phone':phone}
    st.append(card)
    print("添加{:}成功".format(score))


def show_item():
    print('-' * 50)
    print("显示全部")
    print("学号 姓名 性别 房间号 电话")
    print('=' * 50)
    if len(st) == 0:
        print("资料库中不存在学生信息，请进行添加")
        return
    for card in st:
        print(card['score'],card['name'],card['sex'],card['house'],card['phone'])


def exit_system():
    f = open('student.txt','w')
    for line in st:
        f.write(str(line))
        f.write("\n")
    f.close()
    print("欢迎再次使用【宿舍管理系统】")
