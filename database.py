import sqlite3

def init_db():
    # هذا بيسوي ملف قاعدة بيانات مخفي عندك في السيرفر
    conn = sqlite3.connect('n7l_store.db')
    cursor = conn.cursor()
    
    # جدول المستخدمين
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (user_id INTEGER PRIMARY KEY, username TEXT, is_buyer INTEGER DEFAULT 0, is_banned INTEGER DEFAULT 0)''')
    
    # جدول الطلبات
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders 
                      (order_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, product_name TEXT, status TEXT)''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
