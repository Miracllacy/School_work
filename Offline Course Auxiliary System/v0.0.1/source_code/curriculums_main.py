import curriculums as c
c.initialize()
while True:
    n = c.show_operation()
    if n == "0":
        c.back_homepage()
        break
    elif n == "1":
        c.addition_all_work()
    elif n == "2":
        c.modify("i")
    elif n == "3":
        c.clean_work()
    elif n == "4":
        c.show_all_work()
    elif n == "5":
        c.addition_all_course()
    elif n == "6":
        c.modify("week")
    elif n == "7":
        c.clean_course()
    elif n == "8":
        c.show_all_course()
    elif n == "9":
        c.make_table()
    else:
        print("不存在该操作，请重新选择")
