import time


def updateDictionary(text):
    if ';' in text:
        lst = text.split(";")
    else:
        lst = text.split("；")
    myDict = {}
    myDict["memberName"] = lst[0]
    myDict["phone"] = lst[1]
    myDict["name"] = lst[2]
    myDict["description"] = lst[3]
    myDict["link"] = lst[4]
    myDict["price"] = int(lst[5])
    myDict["quantity"] = int(lst[6])
    myDict["place"] = lst[7]
    return myDict

# 使用者登入函式


def updateMember(id, j, cursor, conn):
    cursor.execute(
        'SELECT "lineID" FROM member WHERE "lineID" = \'%s\'' % str(id))
    query = cursor.fetchall()
    if query != []:
        # print("使用者已登入")
        pass
    else:
        cursor.execute('SELECT MAX("memberNumber") FROM member')
        query = cursor.fetchall()
        maxnum = query[0][0]
        if maxnum == None:
            maxnum = 0
        memberNum = maxnum+1
        # print(type(j))
        name = j["memberName"]
        phone = j["phone"]
        cursor.execute("INSERT INTO member VALUES(%s,%s,%s,%s);",
                       (memberNum, name, phone, id))
        conn.commit()

# 上架函式


def updateProduct(id, j, cursor, conn):
    cursor.execute(
        "SELECT \"memberNumber\" From member WHERE \"lineID\" = '%s'" % str(id))
    query = cursor.fetchall()
    memberNum = query[0][0]
    cursor.execute('SELECT MAX("productNumber") FROM product')
    query = cursor.fetchall()
    maxnum = query[0][0]
    if maxnum == None:
        maxnum = 0
    proNum = maxnum+1
    cursor.execute('INSERT INTO product("productNumber","memberNumber","productName","productDescription","productPicturelink","productPrice","productQuantity","deliveryPlace","productState") VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);',
                   (proNum, memberNum, j["name"], j["description"], j["link"], j["price"], j["quantity"], j["place"], True))
    conn.commit()


def orderCart(proNum, id, quantity, cursor, conn):
    # 從ID找用戶代碼
    proNum = int(proNum)
    cursor.execute(
        "SELECT \"memberNumber\" From member WHERE \"lineID\" = '%s'" % str(id))
    query = cursor.fetchall()
    print(query)
    memberNum = query[0][0]
    # 確認商品是否還在
    cursor.execute(
        "SELECT \"productState\" From product WHERE \"productNumber\" = '%s'" % proNum)
    query = cursor.fetchall()
    if query[0][0] == False:
        return False
    # 製造流水號
    cursor.execute('SELECT MAX("serialNumber") FROM "orderCart"')
    query = cursor.fetchall()
    maxnum = query[0][0]
    if maxnum == None:
        maxnum = 0
    serialNumber = maxnum+1
    # 找商品名稱
    cursor.execute(
        "SELECT \"productName\" From product WHERE \"productNumber\" = '%s'" % proNum)
    query = cursor.fetchall()
    name = query[0][0]

    cursor.execute('INSERT INTO "orderCart" VALUES(%s,%s,%s,%s,%s,%s);',
                   (serialNumber, True, memberNum, proNum, quantity, name))
    cursor.execute(
        'Update product SET "productQuantity" = "productQuantity"-1 WHERE "productNumber" = %d' % proNum)
    cursor.execute(
        "SELECT \"productQuantity\" From product WHERE \"productNumber\" = '%s'" % proNum)
    query = cursor.fetchall()
    if query[0][0] == 0:
        cursor.execute(
            'Update product SET "productState" = false WHERE "productNumber" = %d' % proNum)
    conn.commit()


# 查看購物車
def checkCart(id, cursor):
    # 從ID找用戶代碼
    cursor.execute(
        "SELECT \"memberNumber\" From member WHERE \"lineID\" = '%s'" % str(id))
    query = cursor.fetchall()
    memberNum = query[0][0]
    # 印出購物車
    cursor.execute(
        'SELECT *From "orderCart" WHERE "memberNumber" = \'%s\'' % memberNum)
    query = cursor.fetchall()
    lst = []
    for i in query:
        if i[1] == True:
            lst.append(i)
    return lst

# 下單


def orderCartProduct(id, cursor, conn):
    # 從ID找用戶代碼
    cursor.execute(
        "SELECT \"memberNumber\" From member WHERE \"lineID\" = '%s'" % str(id))
    query = cursor.fetchall()
    memberNum = query[0][0]
    # 找到要調的資料
    lst_cart = checkCart(id, cursor)
    # print(lst_cart)
    lst_productNumber = []
    lst_productName = []
    for i in lst_cart:
        lst_productNumber.append(i[3])
        lst_productName.append(i[5])
    # print(lst_productNumber,lst_productName)
    # print(lst)
    # 製造流水號
    cursor.execute('SELECT MAX("orderNumber") FROM "orderInfo"')
    query = cursor.fetchall()
    maxnum = query[0][0]
    if maxnum == None:
        maxnum = 0
    orderNum = maxnum+1
    # print(orderNum)
    # 時間
    nowtime = time.ctime()
    orderTime = nowtime.split(' ')[3]
    orderDate = nowtime.split(
        ' ')[1]+'-'+nowtime.split(' ')[2]+'-'+nowtime.split(' ')[4]

    # 數量
    productQuantity = 0
    for i in lst_cart:
        productQuantity += i[4]
    # 找賣家是誰
    lst = []
    lst2 = []
    for i in lst_cart:
        proNum = i[3]
        cursor.execute(
            'SELECT "memberNumber" FROM "product" WHERE "productNumber" = \'%s\'' % proNum)
        query = cursor.fetchall()
        # print(query[0][0])
        lst2.append(query[0][0])
        print(lst2)
    # 一一丟資料
    cursor.execute(
        'SELECT "memberNumber" FROM member WHERE "lineID" = \'%s\'' % id)
    query = cursor.fetchall()
    memberNum = int(query[0][0])
    printlist = []
    for i in range(len(lst_cart)):
        cursor.execute('INSERT INTO "orderInfo" VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);', (orderNum, orderTime,
                       productQuantity, None, True, orderDate, lst2[i], lst_productNumber[i], memberNum, lst_productName[i]))
        print('happy')
        printlist.append([orderNum, orderTime, productQuantity, orderDate,
                         lst2[i], lst_productNumber[i], memberNum, lst_productName[i]])
        orderNum += 1
    # 清空購物車
    for i in lst_productNumber:
        cursor.execute(
            'UPDATE "orderCart" SET "productState" = false WHERE "productNumber" = %s' % int(i))
    conn.commit()
    return printlist


def get_order_cart_information():
    productNameList = []
    productQuantityList = []
    totalMoneyList = []
    index = []

    return productNameList, productQuantityList, totalMoneyList, index
