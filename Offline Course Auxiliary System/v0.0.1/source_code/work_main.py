import work as w
w.initialize()
while True:
    n = w.show_operation()
    if n == "0":
        w.back_homepage()
        break
    elif n == "1":
        w.addition_all()
    elif n == "2":
        w.modify()
    elif n == "3":
        w.clean()
    elif n == "4":
        w.show_all()
    else:
        print("不存在该操作，请重新选择")
