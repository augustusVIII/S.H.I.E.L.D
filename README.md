# S.H.I.E.L.D
S.H.I.E.L.D is a security-based project that is created by 3 high-school students using Raspberry Pi.  
It represent a security door, if user type in the right password then the door will open.  

## How to use

- Connect all devices like in the circuit image HERE.
- Install: gpiozero, sqlite3, Adafruit_IO.
- Run the python programm. If it is a new day, it will create a new password.
- User need to type in the password inside the adafruit dashboard.
- Type the password, press Enter to enter.
- Right password --> Servo spin for 2 second, program stop, LED off.
- Wrong password --> Buzzer buzz for 5 second, program stop.

## Files  

- final_project.py: main code.  
- password_log.py: read password database.  
