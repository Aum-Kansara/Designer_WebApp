import sqlite3
# Open Database
conn = sqlite3.connect('users.db')
# Creation
# conn.execute('''CREATE TABLE Users 
#        (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
#        FNAME           TEXT    NOT NULL, 
#        LNAME           TEXT    NOT NULL, 
#        EMAIL           TEXT    NOT NULL, 
#        PASS           TEXT    NOT NULL);''')

# print("Created")
# print(conn.execute("select * from users").fetchall())


# order -> userid,type_of_order,img_path,date,time,delivery_date,payment_status
# Creation
# conn.execute('''CREATE TABLE orders 
#        (ORDER_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
#        userid         INT     NOT NULL, 
#        type_of_order  TEXT    NOT NULL,
#        img_path        TEXT    NOT NULL, 
#        date           TEXT    NOT NULL, 
#        time           TEXT    NOT NULL,
#        delivery_date  TEXT            ,
#        payment_status TEXT    NOT NULL);''')

# print("Created")


# Deletion
# order_id=1
# cur = conn.cursor()
# cur.execute('DELETE FROM orders WHERE order_id=?', (order_id,))
# conn.commit()
# print("Row Deleted")
# conn.close()

# Updation
# order_id=14
# conn.execute(f"UPDATE orders set delivery_date = ? where ORDER_ID = ?",('2023-01-23',order_id))
# conn.commit()
# print("Updated Delivery Date")

# Drop Table
# conn.execute('drop table orders')
# print("Table Dropped")



# print Data
# print(conn.execute('select * from orders').fetchall())
conn.close()