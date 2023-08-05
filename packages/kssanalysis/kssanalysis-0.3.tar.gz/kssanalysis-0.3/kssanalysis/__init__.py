"""
pyexample.

An example python library.
"""

__version__ = "0.1"
__author__ = '''Kailash Nath Yadav  Sudhanshu Nautiyal'''


def word(s):
    b=s.split()
    if len(b)==1:
        x=0
        y=0
        f=open("POSITIVE.txt",'r',encoding = 'cp1252')
        g=open("NEGATIVE.txt",'r',encoding = 'cp1252')
        a=f.read().split(",")
        c=g.read().split(",")
        if b[0] in a:
            x=x+1
        elif b[0] in c:
            y=y+1
    try:
        if x==y:
            print("IT IS NEUTRAL WORD")
        elif x>y:
            print("IT IS POSITIVE WORD")
        else:
            print("IT IS NEGATIVE WORD")
        print("Am I right...??")
        k=input()
        if k!="yes":
            v=input("Is it positive or negative..?? ")
            if v=="positive":
                with open("POSITIVE.txt",'a+',encoding = 'cp1252') as f:
                    m=","+s
                    f.write(m)
                    print("I will remember it if u don't belive my smartness u can check it again")
            elif v=="negative":
                with open("NEGATIVE.txt",'a+',encoding = 'cp1252') as g:
                    n=","+s
                    g.write(n)
                    print("I will remember it if u don't belive my smartness u can check it again")
            else:
                print("OK our team is working on neutral")
        else:
            print('I know, I am always right')
    except Exception as e:
        print("IT IS NOT A WORD")
