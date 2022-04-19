import numpy as np
def initialize():
    try:
        f = open('shopping_cart.txt','r')
        a = f.read()
        global shopping_cart
        shopping_cart = eval(a)
        f.close()
        f = open('buy.txt','r')
        a = f.read()
        global buy
        buy = eval(a)
        f.close()
        f = open('products.txt','r')
        a = f.read()
        global products
        buy = eval(a)
        f.close()
    except FileNotFoundError:
        pass
def show_item(content):
    print("#######")
    if content == 1:
        print("序号{:<10s}商品名称{:<10s}价格{:<10s}".format(" "," "," "))
        k = 0
        for i in products:
            print("{:<14d}{:<18s}{}".format(k,i,products[i]))
            k = k + 1
    elif content == 3:
        print("购物车中有如下商品:")
        print("序号{:<10s}商品名称{:<10s}价格{:<10s}数量{:<10s}".format(" "," "," "," "))
        k = 0
        for i in shopping_cart:
            print("{:<14d}{:<18s}{:<14d}{}".format(k,i,products[i],shopping_cart[i]))
            k = k + 1
def show_operation():
    print("#######")
    print("您可进行如下操作（选择对应序号即可）")
    print("0 退出")
    print("1 查看商品列表")
    print("2 加入购物车")
    print("3 结算购物车")
    print("4 查看余额")
    print("5 清空购物车及购买历史")
    choice = input('您选择的操作是:')
    return choice
def in_cart():
    show_item(1)
    print("您想加入购物车的是?")
    while True:
        choice = input('请输入所选商品的序号:')
        if choice.isdigit():
            choice = int(choice)
            if 0 <= choice <= len(products):
                break
            else:
                print("无该商品")
        else:
            print("无该商品")
    product = list(products)[choice]
    if product in shopping_cart:
        shopping_cart[product] += 1
    else:
        shopping_cart[product] = 1
    print("已帮您加入购物车")
def buy(money):
    show_item(3)
    list_pay = input('您想结算的商品是?')
    xlist = list_pay.split(",")
    xlist = [int(xlist[i]) for i in range(len(xlist)) if 0 <= int(xlist[i]) < len(shopping_cart)]
    c,s = np.unique(xlist,return_counts=True)
    total = 0
    pay_item = [list(shopping_cart)[c[i]] for i in range(len(c))]
    for i in range(len(c)):
        total += products[pay_item[i]]*s[i]
    if total<money:
        for i in range(len(pay_item)):
            if pay_item[i] in buy:
                buy[pay_item[i]] += s[i]
            else:
                buy[pay_item[i]] = 1
            shopping_cart[pay_item[i]] -= 1
            if shopping_cart[pay_item[i]] == 0:
                del shopping_cart[pay_item[i]]
        print("已经结算请!")
        return total
    else:
        print("余额不足!")
        return 0
def clean_history():
    global buy
    buy.clear()
    global shopping_cart
    shopping_cart.clear()