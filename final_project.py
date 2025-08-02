import time
from datetime import datetime
from gpiozero import LED, Buzzer, DistanceSensor, Servo
import random
import sqlite3
from Adafruit_IO import Client, Feed, RequestError

# Adafruit IO
ADAFRUIT_IO_USERNAME = 'Your user name'
ADAFRUIT_IO_KEY = 'Your key'
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Feed
try:
    alarm_feed = aio.feeds('alarm-feed')
except RequestError:
    feed = Feed(name='alarm-feed')
    alarm_feed = aio.create_feed(feed)

# GPIO 
led = LED(17)
buzzer = Buzzer(18)
sensor = DistanceSensor(echo=24, trigger=23)
servo = Servo(3)

# SQLite
def init_db():
    conn = sqlite3.connect('passwords.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Passwords (
            date TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_password_to_db(date_str, password):
    conn = sqlite3.connect('passwords.db')
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO Passwords (date, password) VALUES (?, ?)", (date_str, password))
    conn.commit()
    conn.close()

def get_password_for_today():
    today = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect('passwords.db')
    cur = conn.cursor()
    cur.execute("SELECT password FROM Passwords WHERE date = ?", (today,))
    result = cur.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        password = ''.join(str(random.randint(0, 9)) for _ in range(6))
        save_password_to_db(today, password)
        print(f"Mật khẩu hôm nay ({today}): {password}")
        return password

def is_night_time():
    now = datetime.now().time()
    # Here set 00:00 - 24:00 for the sake of example. Realistically set from 22:00 - 04:00.
    return now >= datetime.strptime("00:00", "%H:%M").time() or now <= datetime.strptime("24:00", "%H:%M").time()


init_db()
current_password = get_password_for_today()
print("S.H.I.E.L.D has been activated...")

# Main loop
try:
    while True:
        # Create new password
        new_password = get_password_for_today()
        if new_password != current_password:
            current_password = new_password

        # Detecting
        if is_night_time() and sensor.distance < 0.5:
            print("Someone is passing by! Password required...")
            led.on()
            time.sleep(10)

            try:
                data = aio.receive(alarm_feed.key)
                user_input = data.value.strip()
            except RequestError:
                print("Can't request data from Adafruit")
                user_input = ''

            if user_input == current_password:
                print("Right password! Welcome in!")
                led.off()
                exit()
            else:
                print("Wrong password! Intruder Alert!")
                buzzer.on()
                time.sleep(5)
                buzzer.off()
                led.off()
                exit()

        time.sleep(1)

except KeyboardInterrupt:
    print("\n System stops.")
