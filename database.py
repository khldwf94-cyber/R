import sqlite3

def init_db():
    conn = sqlite3.connect('n7l_store.db')
    cursor = conn.cursor()
    
    # جدول الطلبات: يحفظ طلبات المستخدمين
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        username TEXT,
                        full_name TEXT,
                        product_name TEXT,
                        status TEXT)''')
    
    # جدول المشترين المعتمدين: للحماية
    cursor.execute('''CREATE TABLE IF NOT EXISTS verified_users (
                        user_id INTEGER PRIMARY KEY,
                        is_buyer BOOLEAN)''')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
