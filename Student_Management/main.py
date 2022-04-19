import tools as t
if not t.initialize():
    print("不存在学生信息资料库，已创建")
while True:
    n = t.show_operation()
    if n == '0':
        t.exit_system()
        break
    elif n == '1':
        t.search()
    elif n == '2':
        t.join_in()
    elif n == '3':
        t.show_item()
    else:
        print("输入错误，请重新输入",n)
