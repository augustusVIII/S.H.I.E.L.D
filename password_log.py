import sqlite3

def review_passwords():
    conn = sqlite3.connect('passwords.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Passwords ORDER BY date DESC")
    rows = cur.fetchall()
    print("\n📜 Lịch sử mật khẩu:")
    for row in rows:
        print(f"{row[0]} --> {row[1]}")
    conn.close()
    print()

if __name__ == '__main__':
    review_passwords()
