import course as c

if not c.initialize():
    print("文件不存在，已创建")
while True:
    n = c.show_operation()
    if n == "0":
        break
    elif n == "1":
        c.addition_all()
        c.back_homepage()
    elif n == "2":
        c.modify()
        c.back_homepage()
    elif n == "3":
        c.clean()
        c.back_homepage()
    elif n == "4":
        c.make_table(flag=False)
        c.back_homepage()
    else:
        print("不存在该操作，请重新选择")
