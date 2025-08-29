import mysql.connector as ms
from datetime import date 
check=False
a="y"
while a=="y" or a=="Y":
    pd=input("ENTER YOUR PASSWORD:")
    try:
        cnn=ms.connect(host='localhost',user='root',password=pd)
        cur=cnn.cursor()
        if cnn.is_connected():
            print("================================")
            print("******* WELCOME TO LIBRARY *****")
            print("================================")
            cur.execute("show databases")
            dbs=cur.fetchall()
            if ('library',) not in dbs:
                cur.execute("create database library")
            cnn=ms.connect(host='localhost',user='root',password='root',database='library')
            cur=cnn.cursor()
            check=True
            break
        else:
            print("Failed to connect")
    except ms.Error:
        print("YOU HAVE ENTERED WRONG PASSWORD!!")
        a=input("WANT TO TRY AGAIN(Y/N)")
def isinclass(c):
    cur.execute(" show tables")
    d=cur.fetchall()
    if (c,) in d:
        return True
    else:
        return False
if check:
    if isinclass("books")==False:
        cur.execute("create table books(Bno int primary key,Bname varchar(30) not null,Status varchar(20) not null,Author varchar(20) not null,Publisher varchar(30),Price float(10,2),Student_name varchar(30),sroll int,class char(3))")
if check:
    if isinclass("std_his")==False:
        cur.execute("Create table std_his (sroll int not null,bno int not null,issue date ,submit date , class varchar(8) not null)")
def givename(rn):
    cur.execute("select sname from "+c+" where sroll=%s",(rn,))
    d=cur.fetchall()
    return d[0][0]  
def instd(sroll):
    cur.execute("select sroll from "+c)
    d=cur.fetchall()
    if (sroll,) in d:
        return True
    else:
        return False
def isinbook(bno):
    cur.execute('select Bno from books')
    d=cur.fetchall()
    if (bno,) in d:  
        return True
    else:
        return False
def addclass():
    ans="y"
    while ans=="Y" or ans=="y":
        c=input("ENTER CLASS:")
        if isinclass(c)==False:
            cur.execute('create table '+c+' (sroll int primary key, sname varchar(30) not null, Bno int , status varchar(15) not null, issue date,Foreign key(Bno) references books(Bno))')
            print("CLASS CREATED!!")
        else:
            print("CLASS ALREADY EXSIST")
        ans=input("WANT TO ADD MORE(Y/N)")
def is_issued(bno):
    cur.execute('select Status from books where bno=%s',(bno,))
    d=cur.fetchall()
    if d[0][0]=="ISSUED":
        return True
    else:
        return False
def delclass():
    ans='y'
    while ans=="y" or ans=='Y':
        c=input("ENTER CLASS:")
        if isinclass(c):
            a=input("ARE YOU SURE WANT TO DELETE THIS CLASS(Y/N)")
            if a=="y" or a=="Y":
                cur.execute('drop table '+c) 
                print('Class Deleted!')
        else:
            print("Class Not found")
        ans=input("WANT TO CONTINUE (Y/N)")
def showclasses():
    cur.execute('show tables')
    d=cur.fetchall()
    print("+--------------------+")
    print("|","%5s"%"Sno","|","%10s"%"CLASSES","|")
    print("+--------------------+")
    c=1
    for i in d:
        if 'books' not in i and "std_his" not in i:
            print("|","%5s"%c,"|","%10s"%i[0].upper(),"|")
            c+=1
    print("+--------------------+")
def addbook():
    ans='y'
    while ans=='y' or ans=='Y':
        bno=int(input("ENTER BOOK NUMBER:"))
        if isinbook(bno)==False:
            bname=input("Enter BOOK NAME:")
            status='NOT ISSUED'
            auth=input("ENTER AUTHOR:")
            pub=input("ENTER PUBLISHER:")
            p=float(input("ENTER PRICE:"))
            cur.execute("insert into books(bno,bname,status,author,publisher,price) values(%s,%s,%s,%s,%s,%s)",(bno,bname,status,auth,pub,p))
            cnn.commit()
            print("BOOK ADDED!")
        else:
            print("BOOK IS ALREADY EXIST")
        ans=input("WANT TO ADD MORE(Y/N)")
def issuebook():
    ans='y'
    while ans=='y' or ans=='Y':
        rn=int(input("ENTER ROLL NUMBER:"))
        if instd(rn):
            if anyissue(rn)==False:
                bno=int(input("ENTER BOOK NUMBER:"))
                if isinbook(bno):
                    if is_issued(bno)==False:
                        cur.execute('Update '+c+' set Bno=%s,Status=%s,issue=%s where sroll=%s',(bno,'ISSUED',date.today(),rn))
                        cur.execute('Update books set Status=%s,Student_name=%s,sroll=%s,class=%s where Bno=%s',('ISSUED',givename(rn),rn,c,bno))
                        cur.execute("insert into std_his(sroll,bno,issue,class) values(%s,%s,%s,%s)",(rn,bno,date.today(),c))
                        cnn.commit()
                    else:
                        print("BOOK IS ALREADY ISSUED")
                else:
                    print("BOOK IS NOT ADDED IS LIBRARAY")
            else:
                print("ONE BOOK IS ALREADY ISSUED TO THIS STUDENT")
        else:
            print("STUDENT NOT FOUND")
        ans=input("WANT TO ADD MORE(Y/N)")
def submitbook():
    ans="y"
    while ans=="y" or ans=="Y":
        bno=int(input("ENTER BOOK NUMBER:"))  
        if isinbook(bno):
            if is_issued(bno):
                cur.execute('select sroll,sname from 12a where bno=%s',(bno,))
                for i in cur:
                    print("ROLL NUMBER:",i[0])
                    print("STUDENT NAME:",i[1])
                    rn=i[0]
                cur.execute('Update '+c+' set Bno=NULL,Status=%s,issue=NULL where sroll=%s',('NOT ISSUED',rn))
                cur.execute('Update books set Status=%s,Student_name=NULL,sroll=NULL,class=NULL where Bno=%s',('NOT ISSUED',bno))
                cur.execute("Update std_his set submit=%s where sroll=%s and class=%s and bno=%s and submit is null",(date.today(),i[0],c,bno))
                cnn.commit()
            else:
                print("ALREADY SUBMITED!")
        else:
            print("NO SUCH BOOK!")
        ans=input("WANT TO SUBMIT MORE BOOKS(Y/N)")
def bookdetails():
    cur.execute('select * from books')
    d=cur.fetchall()
    print("+----------------------------------------------------------------------------------------------------------------------------------------------------+")
    print("|","%11s"%'BOOK NUMBER',"|","%20s"%"BOOK NAME","|","%15s"%"STATUS","|","%20s"%"AUTHOR","|","%15s"%"PUBLISHER","|","%10s"%"PRICE","|","%15s"%"STUDENT NAME","|","%11s"%"ROLL NUMBER","|","%5s"%"CLASS","|")
    print("+----------------------------------------------------------------------------------------------------------------------------------------------------+")
    for i in d:
        print("|","%11s"%i[0],"|","%20s"%i[1],"|","%15s"%i[2],"|","%20s"%i[3],"|","%15s"%i[4],"|","%10s"%i[5],"|",'%15s'%i[6],"|","%11s"%i[7],"|","%5s"%i[8],"|")
    print("+----------------------------------------------------------------------------------------------------------------------------------------------------+")
def addstd():
    ans="y"
    while ans=="y" or ans=="Y":
        sroll=int(input("ENTER ROLL NUMBER:"))
        if instd(sroll):
            print("STUDENT ALREADY EXIST!")
        else:
            name=input("ENTER NAME:")
            cur.execute("insert into "+c+'(sroll,sname,status) values(%s,%s,%s)',(sroll,name,'NOT ISSUED'))
            cnn.commit()
        ans=input("WANT TO ADD MORE(Y/N)")
def showstd():
    cur.execute("select * from "+c)
    print("%11s"%'ROLL NUMBER',"%30s"%"STUDENT NAME","%20s"%"BOOK NUMBER","%20s"%"STATUS","%20s"%"ISSUE DATE")
    for i in cur:
        print("%11s"%i[0],"%30s"%i[1],"%20s"%i[2],"%20s"%i[3],"%20s"%i[4])
def delstd():
    sroll=int(input("ENTER ROLL NUMBER:"))
    if instd(sroll):
        print("STUDENT NAME:",givename(sroll))
        cask=input("ARE YOU SURE WANT TO DELETE THIS STUDENT(Y/N)")
        if cask=="Y" or cask=="y":
            cur.execute("delete from "+c+" where sroll=%s",(sroll,))
            cnn.commit()
            print("STUDENT DELETED!")
    else:
        print("STUDENT NOT FOUND!")
def delbook():
    bno=int(input("ENTER BOOK NUMBER:"))
    if isinbook(bno) and is_issued(bno)==False:
        cask=input("ARE YOU SURE WANT TO DELETE THIS BOOK(Y/N)")
        if cask=="y" or cask=="Y":
            cur.execute("delete from books where Bno=%s",(bno,))
            cnn.commit()
    else:
        print("BOOK NOT FOUND OR ISSUED TO SOMEONE")
        print("NOTE: YOU CAN NOT DELETE ANY BOOK IF IT IS ISSUED!")
def onegoissue():
    cur.execute("select sroll from "+c+" where status=%s order by sroll asc",("NOT ISSUED",))
    d=cur.fetchall()
    f=0
    print("USE 0 TO SKIP ANY STUDENT")
    for i in d:
        f=1
        print("*********************************************************")
        print("STUDENT ROLL :",i[0])
        bno=int(input("Enter Book Number:"))
        if bno!=0:
            if anyissue(i[0])==False:
                if isinbook(bno) and is_issued(bno)==False:
                    cur.execute('Update '+c+' set Bno=%s,Status=%s,issue=%s where sroll=%s',(bno,'ISSUED',date.today(),i[0]))
                    cur.execute('Update books set Status=%s,Student_name=%s,sroll=%s,class=%s where Bno=%s',('ISSUED',givename(i[0]),i[0],c,bno))
                    cur.execute("insert into std_his(sroll,bno,issue,class) values(%s,%s,%s,%s)",(i[0],bno,date.today(),c))
                    cnn.commit()
                    print("BOOK ISSUED!")
                else:
                    print("EITHER BOOK IS ISSUED OR NOT IN THE LIBRARAY!")
                    break
                print("*********************************************************")
            else:
                print("ONE BOOK IS ALREADY ISSUED")
        if f==0:
            print("BOOK IS ISSUED TO ALL STUDENTS ALREADY!")
def avlbooks():
    cur.execute("select * from books where status=%s",("NOT ISSUED",))
    d=cur.fetchall()
    print("+----------------------------------------------------------------------------------------------------------------------------------------------------+")
    print("|","%11s"%"BOOK NUMBER","|","%20s"%"BOOK NAME","|","%15s"%"STATUS","|","%20s"%"AUTHOR","|","%15s"%"PUBLISHER","|","%10s"%"PRICE","|","%15s"%"STUDENT NAME","|","%11s"%"ROLL NUMBER","|","%5s"%"CLASS","|")
    print("+----------------------------------------------------------------------------------------------------------------------------------------------------+")
    for i in d:
        print("|","%11s"%i[0],"|","%20s"%i[1],"|","%15s"%i[2],"|","%20s"%i[3],"|","%15s"%i[4],"|","%10s"%i[5],"|",'%15s'%i[6],"|","%11s"%i[7],"|","%5s"%i[8],"|")
    print("+----------------------------------------------------------------------------------------------------------------------------------------------------+")
def onegosubmit():
    cur.execute("select sroll,bno from "+c+" where status=%s",("ISSUED",))
    d=cur.fetchall()
    print("USE (P/p) FOR SKIP AND (S/s) FOR SUBMIT")
    f=0
    for i in d:
        f=1
        print("*********************************************")
        print("STUDENT ROLL NUMBER:",i[0])
        print("BOOK NUMBER:",i[1])
        ans=input("ENTER CHOICE:")
        if ans=="s" or ans=="S":
            cur.execute('Update '+c+' set Bno=NULL,Status=%s,issue=NULL where sroll=%s',('NOT ISSUED',i[0]))
            cur.execute('Update books set Status=%s,Student_name=NULL,sroll=NULL,class=NULL where Bno=%s',('NOT ISSUED',i[1]))
            cur.execute("Update std_his set submit=%s where sroll=%s and class=%s and bno=%s and submit is null",(date.today(),i[0],c,i[1]))
            cnn.commit()
            print("BOOK SUBMITED!")
            print("*********************************************")
    if f==0:
        print("NO BOOK ISSUED TO ANY STUDENT THIS CLASS!")
def anyissue(rn):
    cur.execute("select status from "+c+" where sroll=%s",(rn,))
    d=cur.fetchall()
    if d[0][0]=="ISSUED":
        return True
    else:
        return False
def searchbooks():
    cur.execute("select * from books")
    d=cur.fetchall()
    print("+=================================+")
    print("| 1=TO SEARCH BOOK BY BNO         |")
    print("| 2=TO SEARCH BOOK BY AUTHOR      |")
    print("| 3=TO SEARCH BOOK BY PRICE       |")
    print("| 4=TO SEARCH BOOK BY PUBLISHER   |")
    print("| 5=TO SEARCH BOOK IN PRICE RANGE |")
    print("+=================================+")
    s=int(input("ENTER CHOICE:"))
    cur.execute("select * from books")
    d=cur.fetchall()
    if s==1:
        bno=int(input("ENTER BOOK NUMBER:"))
        print("+----------------------------------------------------------------------------------------------------------------------------------------------------+")
        print("|","%11s"%'BOOK NUMBER',"|","%20s"%"BOOK NAME","|","%15s"%"STATUS","|","%20s"%"AUTHOR","|","%15s"%"PUBLISHER","|","%10s"%"PRICE","|","%15s"%"STUDENT NAME","|","%11s"%"ROLL NUMBER","|","%5s"%"CLASS","|")
        print("+----------------------------------------------------------------------------------------------------------------------------------------------------+")
        for i in d:
            if i[0]==bno:
                print("|","%11s"%i[0],"|","%20s"%i[1],"|","%15s"%i[2],"|","%20s"%i[3],"|","%15s"%i[4],"|","%10s"%i[5],"|",'%15s'%i[6],"|","%11s"%i[7],"|","%5s"%i[8],"|")
                print("+----------------------------------------------------------------------------------------------------------------------------------------------------+")
                break
        else:
            print("BOOK NOT FOUND")
    elif s==2:
        a=input("ENTER AUTHOR NAME:")
        print("+------------------------------------------------------------------------------------------------------------------------------------+")
        print("|","%15s"%'BOOK NUMBER',"|","%20s"%"BOOK NAME","|","%20s"%"STATUS","|","%20s"%"AUTHOR","|","%20s"%"PUBLISHER","|","%20s"%"PRICE","|")
        print("+------------------------------------------------------------------------------------------------------------------------------------+")
        f=0
        for i in d:
            if i[3].lower().strip()==a.lower().strip():
                f=1
                print("|","%15s"%i[0],"|","%20s"%i[1],"|","%20s"%i[2],"|","%20s"%i[3],"|","%20s"%i[4],"|","%20s"%i[5],"|")
        print("+------------------------------------------------------------------------------------------------------------------------------------+")
        if f==0:
            print("BOOK NOT FOUND")
    elif s==3:
        p=float(input("ENTER PRICE:"))
        print("+------------------------------------------------------------------------------------------------------------------------------------+")
        print("|","%15s"%'BOOK NUMBER',"|","%20s"%"BOOK NAME","|","%20s"%"STATUS","|","%20s"%"AUTHOR","|","%20s"%"PUBLISHER","|","%20s"%"PRICE","|")
        print("+------------------------------------------------------------------------------------------------------------------------------------+")
        f=0
        for i in d:
            if i[5]==p:
                f=1
                print("|","%15s"%i[0],"|","%20s"%i[1],"|","%20s"%i[2],"|","%20s"%i[3],"|","%20s"%i[4],"|","%20s"%i[5],"|")
        print("+------------------------------------------------------------------------------------------------------------------------------------+")
        if f==0:
            print("BOOKS NOT FOUND")
    elif s==5:
        lp=float(input("ENTER LOWER PRICE:"))
        up=float(input("ENTER UPPER PRICE:"))
        print("+------------------------------------------------------------------------------------------------------------------------------------+")
        print("|","%15s"%'BOOK NUMBER',"|","%20s"%"BOOK NAME","|","%20s"%"STATUS","|","%20s"%"AUTHOR","|","%20s"%"PUBLISHER","|","%20s"%"PRICE","|")
        print("+------------------------------------------------------------------------------------------------------------------------------------+")
        f=0
        for i in d:
            if i[5]>=lp and i[5]<=up:
                f=1
                print("|","%15s"%i[0],"|","%20s"%i[1],"|","%20s"%i[2],"|","%20s"%i[3],"|","%20s"%i[4],"|","%20s"%i[5],"|")
        print("+------------------------------------------------------------------------------------------------------------------------------------+")
        if f==0:
            print("BOOKS NOT FOUND")
    elif s==4:
        a=input("ENTER PUBLISHER")
        print("+------------------------------------------------------------------------------------------------------------------------------------+")
        print("|","%15s"%'BOOK NUMBER',"|","%20s"%"BOOK NAME","|","%20s"%"STATUS","|","%20s"%"AUTHOR","|","%20s"%"PUBLISHER","|","%20s"%"PRICE","|")
        print("+------------------------------------------------------------------------------------------------------------------------------------+")
        f=0
        for i in d:
            if i[4].lower().strip()==a.lower().strip():
                f=1
                print("|","%15s"%i[0],"|","%20s"%i[1],"|","%20s"%i[2],"|","%20s"%i[3],"|","%20s"%i[4],"|","%20s"%i[5],"|")
        print("+------------------------------------------------------------------------------------------------------------------------------------+")
        if f==0:
            print("BOOK NOT FOUND")
def stdhis():
    sroll=int(input("ENTER ROLL NUMBER:"))
    if instd(sroll):
        cur.execute("select * from std_his where sroll=%s and class=%s",(sroll,c))
        d=cur.fetchall()
        print("*"*43)
        print("STUDENT ROLL NUMBER :",sroll)
        print("CLASS :",c.upper())
        print("STUDENT NAME :",givename(sroll))
        print()
        print("%15s"%"BOOK NUMBER","%13s"%"ISSUE DATE","%13s"%"SUBMIT DATE")
        for i in d:
            print("%15s"%i[1],"%13s"%i[2],"%13s"%i[3])
        print("*"*43)
    else:
        print("STUDENT NOT FOUND!")
def stdhisall():
    print("*"*67)
    cur.execute("select * from std_his ")
    d=cur.fetchall()
    print("%11s"%"ROLL NUMBER","%15s"%"BOOK NUMBER","%13s"%"ISSUE DATE","%13s"%"SUBMIT DATE","%10s"%"CLASS")
    for i in d:
        print("%11s"%i[0],"%15s"%i[1],"%13s"%i[2],"%13s"%i[3],"%10s"%i[4].upper())
    print("*"*67)
if check:     
    while True:
        print()
        print("+------------------------------+")
        print("| 1=TO SELECT CLASS            |")
        print("| 2=TO SHOW ALL CLASSES        |")
        print("| 3=TO SHOW ALL BOOK DETAILS   |")
        print("| 4=TO ADD A BOOK              |")
        print("| 5=TO DELETE A BOOK           |")
        print("| 6=TO SEARCH A BOOK           |")
        print("| 7=TO ADD A CLASS             |")
        print("| 8=TO DELETE A CLASS          |")
        print("| 9=TO SHOW AVAILABLE BOOKS    |")
        print("| 10=TO HISTROY OF ALL STUDENTS|")
        print("| 0=EXIT                       |")
        print("+------------------------------+")
        ans=""
        while type(ans)!=int:
            try:
                ans=int(input("ENTER CHOICE:"))
            except ValueError:
                print("===> PLEASE ENTER CORRECT DATATYPE !")                  
        print()
        if ans==1:
            c=input("ENTER YOUR CLASS:")
            c=c.lower()
            if isinclass(c):
                print("===============================================================================")
                print("**************************{ WELCOME TO CLASS "+c.upper()+" }*****************************")
                print("===============================================================================")
                while True :
                    print()
                    print("+----------------------------------+")
                    print("| 1=TO ISSUE A BOOK                |")
                    print("| 2=TO SUBMIT A BOOK               |")
                    print("| 3=TO ADD A STUDENT               |")
                    print("| 4=TO SHOW ALL STUDENTS           |")
                    print("| 5=TO DELETE A STUDENT            |")
                    print("| 6=TO ISSUE BOOK FOR WHOLE CLASS  |")
                    print("| 7=TO SUBMIT BOOK FOR WHOLE CLASS |")
                    print("| 8=TO SHOW HISTROY OF A STUDENT   |")
                    print("| 0=BACK                           |")
                    print("+----------------------------------+")
                    print()
                    ans2=''
                    while type(ans2)!=int:
                        try:
                            ans2=int(input("ENTER CHOICE:"))
                        except ValueError:
                            print("===> PLEASE ENTER CORRECT DATATYPE !")   
                    if ans2==1:
                        issuebook()
                    elif ans2==2:           
                        submitbook()
                    elif ans2==3:            
                        addstd()
                    elif ans2==4:           
                        showstd()
                    elif ans2==5:
                        delstd()
                    elif ans2==6:
                        onegoissue()
                    elif ans2==7:
                        onegosubmit()
                    elif ans2==8:
                        stdhis()
                    elif ans2==0:
                        break
            else:
                print()
                print("----->",c,"CLASS NOT FOUND IN LIBRARAY")
        elif ans==2:
            showclasses()
        elif ans==3:
            bookdetails()
        elif ans==4:
            addbook()
        elif ans==5:
            delbook()
        elif ans==6:
            searchbooks()
        elif ans==7:
            addclass()
        elif ans==8:
            delclass()
        elif ans==9:
            avlbooks()
        elif ans==10:
            stdhisall()
        elif ans==0:
            break