import sqlite3, hashlib, itertools, getpass, os, time, pty, smtplib
conn = sqlite3.connect("POS.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users (username text, password text, usertype text)")
c.execute("CREATE TABLE IF NOT EXISTS notes (owner text, title text, content text)")
#c.execute("INSERT INTO users VALUES ('admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'admin')") Run On First Use
conn.commit()
username = input("Enter Username: ")
password = getpass.getpass(prompt='Enter Password: ').encode()
password = hashlib.sha256(password).hexdigest()
c.execute("SELECT * FROM users WHERE username = '"+username+"' AND password = '"+password+"'")
data = c.fetchall()
if data != []:
    if data[0][2] == "admin":
        print(time.strftime('%d/%m/%Y %H:%M:%S'))
        while True:
            command = input(data[0][0]+"@POS:~# ")
            if command == "clear":
                os.system("clear")
            elif command == "404":
                print("W3LC0M3 T0 H4Ck3R M0D3!")
                print(time.strftime('%d/%m/%Y %H:%M:%S'))
                while True:
                    hcommand = input(data[0][0]+"@H4Ck3R_M0D3:~# ")
                    if hcommand == "hash":
                        text = input("Enter Text To Hash: ")
                        hashtype = input("What Hash Type Do You Want [md5|sha256] ")
                        if hashtype != "sha256" and hashtype != "md5":
                            print("Please Only Select sha256 or md5")
                        if hashtype == "md5":
                            print("Hash: "+hashlib.md5(text.encode()).hexdigest())
                        elif hashtype == "sha256":
                            print("Hash: "+hashlib.sha256(text.encode()).hexdigest())
                    elif hcommand == "exit":
                        break
                    elif hcommand == "clear":
                        os.system("clear")
                    elif hcommand == "help":
                        print("hash, exit, clear, help")
                    else:
                        if hcommand != "":
                            print("Command Not Found: \""+hcommand+"\"")
            elif command == "sql":
                print("Type \"exit\" To Stop SQL")
                sqlquery = input("Enter SQL Query: ")
                while sqlquery != "exit":
                    c.execute(sqlquery)
                    sqldata = c.fetchall()
                    for i in sqldata:
                        print(i)
                    conn.commit()
                    sqlquery = input("Enter SQL Query: ")
            elif command == "shell":
                pty.spawn("/bin/bash")
            elif command == "useradd":
                addusername = input("Enter Username: ")
                c.execute("SELECT * FROM users WHERE username ='"+addusername+"'")
                data = c.fetchall()
                if data == []:
                    addpassword = getpass.getpass(prompt='Enter Password: ').encode()
                    addpassword = hashlib.sha256(addpassword).hexdigest()
                    addusertype = input("Do You Want The User To Be An Admin [y/N] ")
                    if addusertype == "y" or addusertype == "Y" or addusertype == "yes" or addusertype == "Yes":
                        print("Adding Admin")
                        c.execute("INSERT INTO users VALUES ('"+addusername+"', '"+addpassword+"', 'admin')")
                        conn.commit()
                    else:
                        print("Adding User")
                        c.execute("INSERT INTO users VALUES ('"+addusername+"', '"+addpassword+"', 'user')")
                        conn.commit()
                else:
                    print("Username Is Already In Use")
            elif command == "userdel":
                delusername = input("Enter Username To Delete: ")
                if delusername != "":
                    c.execute("SELECT * FROM users WHERE username ='"+delusername+"'")
                    deldata = c.fetchall()
                    if deldata != []:
                        delwarning = input("Do You Want To Delete User "+delusername+" [y/N] ")
                        if delwarning == "y" or delwarning == "Y" or delwarning == "yes" or delwarning == "Yes":
                            c.execute("DELETE FROM users WHERE username = '"+delusername+"'")
                            c.execute("DELETE FROM notes WHERE owner = '"+delusername+"'")
                            conn.commit()
            elif command == "users":
                c.execute("SELECT * FROM users")
                usersdata = c.fetchall()
                for i in usersdata:
                    print(i[0]+", "+i[2])
            elif command == "chpasswd":
                chpasswdnew = getpass.getpass(prompt="Enter The New Password: ")
                chpasswdhashed = hashlib.sha256(chpasswdnew.encode()).hexdigest()
                c.execute("DELETE FROM users WHERE username = '"+data[0][0]+"'")
                c.execute("INSERT INTO users VALUES ('"+data[0][0]+"', '"+chpasswdhashed+"', '"+data[0][2]+"')")
                conn.commit()
                print("Password Changed")
            elif command == "noteadd":
                noteaddtitle = input("Enter Note Title: ")
                c.execute("SELECT * FROM notes WHERE title = '"+noteaddtitle+"' AND owner = '"+data[0][0]+"'")
                noteadddata = c.fetchall()
                if noteadddata == []:
                    noteaddcontent = input("Enter Note Content: ")
                    if noteaddcontent != "":
                        c.execute("INSERT INTO notes VALUES ('"+data[0][0]+"', '"+noteaddtitle+"', '"+noteaddcontent+"')")
                        conn.commit()
                        print("Note \""+noteaddtitle+"\" Created")
                    else:
                        print("Can't Create A Empty Note")
                else:
                    print("Note Already Exists")
                    
            elif command == "notedel":
                notedeltitle = input("Enter Title Of Note To Delete: ")
                c.execute("SELECT * FROM notes WHERE owner = '"+data[0][0]+"' AND title = '"+notedeltitle+"'")
                notedeldata = c.fetchall()
                if notedeldata != []:
                    c.execute("DELETE FROM notes WHERE owner = '"+data[0][0]+"' AND title = '"+notedeltitle+"'")
                    conn.commit()
                    print("Note \""+notedeltitle+"\" Deleted")
                else:
                    print("Note Doesn't Exists")
            elif command == "notes":
                c.execute("SELECT * FROM notes WHERE owner = '"+data[0][0]+"'")
                notesdata = c.fetchall()
                for i in notesdata:
                    print("Title: "+i[1]+"\nContent:\n"+i[2])
            elif command == "email":
                email_mode = input('Do You Want To Write Massage Or Send Text File Content? [m/f] ')
                if email_mode == 'm' or email_mode == 'M':
                    sender = input('Enter Your Gmail Address (You Have To Allow Less Secure Apps!): ')
                    password = getpass.getpass(prompt='Enter Password To Your Email: ')
                    recevier = input('Enter Email Address For Receiver: ')
                    subject = input('Enter Subject: ')
                    body = input('Enter Body: ')
                    message = '''\
                    From: %s
                    To: %s
                    Subject: %s
                    
                    %s
                    ''' % (sender,recevier,subject,body)
                    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
                    server.login(sender,password)
                    server.sendmail(sender,recevier,message)
                    server.close()
                elif email_mode == 'f' or email_mode == 'F':
                    filename = input('Enter File: ')
                    sender = input('Enter Your Gmail Address (You Have To Allow Less Secure Apps!): ')
                    password = getpass.getpass(prompt='Enter Password To Your Email: ')
                    recevier = input('Enter Email Address For Receiver: ')
                    subject = input('Enter Subject: ')
                    filecontent = open(filename)
                    message = '''\
                    From: %s
                    To: %s
                    Subject: %s
                    %s
                    ''' % (sender,recevier,subject,filecontent.read())
                    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
                    server.login(sender,password)
                    server.sendmail(sender,recevier,message)
                    server.close()
            elif command == "exit":
                exit()
            elif command == "whoami":
                print("Username:",data[0][0],"\nUser Type:",data[0][2])
            elif command == "help":
                print("clear, 404, sql, shell, useradd, userdel, users, noteadd, notedel, notes, email, exit, whoami, help")
            else:
                if command != "":
                    print("Command Not Found: \""+command+"\"")
    elif data[0][2] == "user":
        print(time.strftime('%d/%m/%Y %H:%M:%S'))
        while True:
            command = input(data[0][0]+"@POS:~$ ")
            if command == "clear":
                os.system("clear")
            elif command == "chpasswd":
                chpasswdnew = getpass.getpass(promt="Enter The New Password: ")
                chpasswdhashed = hashlib.sha256(chpasswdnew.encode()).hexdigest()
                c.execute("DELETE * FROM users WHERE username = '"+data[0][0]+"'")
                c.execute("INSERT INTO users VALUES ('"+data[0][0]+"', '"+chpasswdhashed+"', '"+data[0][2]+"')")
                conn.commit()
                print("Password Changed")
            elif command == "noteadd":
                noteaddtitle = input("Enter Note Title: ")
                c.execute("SELECT * FROM notes WHERE title = '"+noteaddtitle+"' AND owner = '"+data[0][0]+"'")
                noteadddata = c.fetchall()
                if noteadddata == []:
                    noteaddcontent = input("Enter Note Content: ")
                    if noteaddcontent != "":
                        c.execute("INSERT INTO notes VALUES ('"+data[0][0]+"', '"+noteaddtitle+"', '"+noteaddcontent+"')")
                        conn.commit()
                        print("Note \""+noteaddtitle+"\" Created")
                    else:
                        print("Can't Create A Empty Note")
                else:
                    print("Note Already Exists")
            elif command == "notedel":
                notedeltitle = input("Enter Title Of Note To Delete: ")
                c.execute("SELECT * FROM notes WHERE owner = '"+data[0][0]+"' AND title = '"+notedeltitle+"'")
                notedeldata = c.fetchall()
                if notedeldata != []:
                    c.execute("DELETE FROM notes WHERE owner = '"+data[0][0]+"' AND title = '"+notedeltitle+"'")
                    conn.commit()
                    print("Note \""+notedeltitle+"\" Deleted")
                else:
                    print("Note Doesn't Exists")
            elif command == "notes":
                c.execute("SELECT * FROM notes WHERE owner = '"+data[0][0]+"'")
                notesdata = c.fetchall()
                for i in notesdata:
                    print("Title: "+i[1]+"\nContent:\n"+i[2])
            elif command == "email":
                mode = input('Do You Want To Write Massage Or Send Text File Content? [m/f] ')
                if email_mode == 'm' or email_mode == 'M':
                    sender = input('Enter Your Gmail Address (You Have To Allow Less Secure Apps!): ')
                    password = getpass.getpass(prompt='Enter Password To Your Email: ')
                    recevier = input('Enter Email Address For Receiver: ')
                    subject = input('Enter Subject: ')
                    body = input('Enter Body: ')
                    message = '''\
                    From: %s
                    To: %s
                    Subject: %s
                    
                    %s
                    ''' % (sender,recevier,subject,body)
                    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
                    server.login(sender,password)
                    server.sendmail(sender,recevier,message)
                    server.close()
                elif email_mode == 'f' or email_mode == 'F':
                    filename = input('Enter File: ')
                    sender = input('Enter Your Gmail Address (You Have To Allow Less Secure Apps!): ')
                    password = getpass.getpass(prompt='Enter Password To Your Email: ')
                    recevier = input('Enter Email Address For Receiver: ')
                    subject = input('Enter Subject: ')
                    filecontent = open(filename)
                    message = '''\
                    From: %s
                    To: %s
                    Subject: %s
                    %s
                    ''' % (sender,recevier,subject,filecontent.read())
                    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
                    server.login(sender,password)
                    server.sendmail(sender,recevier,message)
                    server.close()
            elif command == "exit":
                exit()
            elif command == "whoami":
                print("Username:",data[0][0],"\nUser Type:",data[0][2])
            elif command == "help":
                print("clear, noteadd, notedel, notes, email, exit, whoami, help")
            else:
                if command != "":
                    print("Command Not Found: \""+command+"\"")
    else:
        print("INVALID USER TYPE")
else:
    print("WRONG USERNAME OR PASSWORD")
