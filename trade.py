def updateDictionary(text):
    lst = text.split(";")
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
    # print(query)
    memberNum = query[0][0]
    cursor.execute('SELECT MAX("productNumber") FROM product')
    query = cursor.fetchall()
    maxnum = query[0][0]
    # print(maxnum)
    if maxnum == None:
        maxnum = 0
    proNum = maxnum+1
    # print(proNum)
    cursor.execute('INSERT INTO product("productNumber","memberNumber","productName","productDescription","productPicturelink","productPrice","productQuantity","deliveryPlace") VALUES(%s,%s,%s,%s,%s,%s,%s,%s);',
                   (proNum, memberNum, j["name"], j["description"], j["link"], j["price"], j["quantity"], j["place"]))
    conn.commit()
