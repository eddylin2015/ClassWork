
import random  # 亂數
import math  # math 內置數學函數
import numpy as np  # 數字矩陣
import sympy as sp  # sympy 簡易別名 sp
from sympy.parsing.sympy_parser import parse_expr  # 文字字串, 解釋成, Sympy 運算式
from sympy.plotting import plot  # 繪圖表
import json  # JSON 結構化資料
import datetime
from sympy.solvers.inequalities import solve_univariate_inequality
from sympy.solvers.inequalities import reduce_rational_inequalities
from sympy import lambdify
from matplotlib.figure import Figure
import re
import esutils as lib
import os

"""
基本數據結構
TE 單條題目記錄: St題目, Val電腦答案, Ans作答,OK檢查1/0, Tip提示
NTE 多條題目.
NTE=[]; NTE.append(GetTE(Qid,St,Val))
for TE in NTE:  pass
"""

def GetKey(QIID="None"):
    return r"%s.%s"% (datetime.datetime.now().isoformat().replace(":","_"),random.random())

def GetTE(Qid, St, Val, Tx=0):
    ''' 單條題目記錄: St題目, Val電腦答案, Ans作答,OK檢查1/0, Tip提示'''
    TE = {}
    #TE["Key"] =r"%s.%s"% (datetime.datetime.now().isoformat().replace(":","_"),random.random())
    TE["Id"] = Qid
    TE["Tx"] = Tx
    TE["St"] = St
    TE["Val"] = Val
    TE["Ans"] = ""
    TE["OK"] = 0
    TE["Minute"]= datetime.datetime.now().strftime("%M:%S")   #"%m-%d-%Y %H:%M:%S")    
    TE["Tip"] = ""
    TE["PotImg"]=None
    return TE

def GetQList():
    return  [
        "PF101.4.有理數運算",          
        "PF102.6.整數指數冪運算",
        "PF103.4.一元一次方程",
        "PF104.4.整式的加減法練習",    
        "PF105.4.二元一次方程","PF106.4.一元一次不等式",
        "PF107.4.一元一次不等式組",    
        "PF108.4.整式的乘法練習","PF201.4.根式的運算",
        "PF202.4.整式的乘法公式",
        "PF203.4.因式分解提公因式",
        "PF204.4.分式的乘除",
        "PF205.4.分式的加減",         
        "PF206.4.分式方程",
        "PF207.4.一次函數圖像的性質",
        "PF291.4.一元二次方程式十字相乘法求因式",
        "PF292.4.一元二次方程式求解",
        "PF293.4.整式的乘法練習",  
        "PF301.4.一元二次方程式",
        "PF302.4.解可化為一元二次方程的分式方程",
        "PF303.4.解二元二次方程組",
        "PF304.4.二次函數圖像的性質",
        "PF305.4.解直角三角形"]

"""
算式
"""
def Get_Expr(QIID,QAMT,Tx=-1):
    NTE=None
    if QIID=="PF101":    NTE=Get_PF101_Expr(QAMT,Tx)
    elif QIID=="PF102" : NTE=Get_PF102_Expr(QAMT,Tx)
    elif QIID=="PF103" : NTE=Get_PF103_Expr(QAMT,Tx)
    elif QIID=="PF104" : NTE=Get_PF104_Expr(QAMT,Tx)
    elif QIID=="PF105" : NTE=Get_PF105_Expr(QAMT,Tx)
    elif QIID=="PF106" : NTE=Get_PF106_Expr(QAMT,Tx)
    elif QIID=="PF107" : NTE=Get_PF107_Expr(QAMT,Tx)
    elif QIID=="PF108" : NTE=Get_PF108_Expr(QAMT,Tx)
    elif QIID=="PF201" : NTE=Get_PF201_Expr(QAMT,Tx)
    elif QIID=="PF202" : NTE=Get_PF202_Expr(QAMT,Tx)
    elif QIID=="PF203" : NTE=Get_PF203_Expr(QAMT,Tx)
    elif QIID=="PF204" : NTE=Get_PF204_Expr(QAMT,Tx)
    elif QIID=="PF205" : NTE=Get_PF205_Expr(QAMT,Tx)
    elif QIID=="PF206" : NTE=Get_PF206_Expr(QAMT,Tx)
    elif QIID=="PF207" : NTE=Get_PF207_Expr(QAMT,Tx)
    elif QIID=="PF291" : NTE=Get_PF291_Expr(QAMT,Tx)
    elif QIID=="PF292" : NTE=Get_PF292_Expr(QAMT,Tx)
    elif QIID=="PF293" : NTE=Get_PF293_Expr(QAMT,Tx)
    elif QIID=="PF301" : NTE=Get_PF301_Expr(QAMT,Tx)
    elif QIID=="PF302" : NTE=Get_PF302_Expr(QAMT,Tx)
    elif QIID=="PF303" : NTE=Get_PF303_Expr(QAMT,Tx)
    elif QIID=="PF304" : NTE=Get_PF304_Expr(QAMT,Tx)
    elif QIID=="PF305" : NTE=Get_PF305_Expr(QAMT,Tx)
    else:
        return None
    return NTE

def Post_Expr_UpdateAns(ReqForm,NTE):
    for key in ReqForm.keys():
        if key=="SID": continue
        for value in ReqForm.getlist(key):
            for TE in NTE:
                if int(key)>=1000:
                    if int(TE["Id"])==int(key)-1000:
                        TE["Minute"]=value

                elif int(TE["Id"])==int(key):
                    if TE["Ans"] != "" :  
                        TE["Ans"]=TE["Ans"]+";"+ value 
                    else:
                        TE["Ans"]=value

def Post_Expr_CheckAns(QIID,NTE):
    if QIID=="PF104" : Post_PF104_Expr(NTE)
    elif QIID=="PF105" : Post_PF105_Expr(NTE)
    elif QIID=="PF106" : Post_PF106_Expr(NTE)
    elif QIID=="PF107" : Post_PF107_Expr(NTE)
    elif QIID=="PF108" : Post_PF108_Expr(NTE)
    elif QIID=="PF201" : Post_PF201_Expr(NTE)
    elif QIID=="PF202" : Post_PF202_Expr(NTE)
    elif QIID=="PF203" : Post_PF203_Expr(NTE)
    elif QIID=="PF204" : Post_PF204_Expr(NTE)
    elif QIID=="PF205" : Post_PF205_Expr(NTE)
    elif QIID=="PF206" : Post_PF206_Expr(NTE)
    elif QIID=="PF207" : Post_PF207_Expr(NTE)
    elif QIID=="PF291" : Post_PF291_Expr(NTE)
    elif QIID=="PF292" : Post_PF292_Expr(NTE)
    elif QIID=="PF293" : Post_PF293_Expr(NTE)
    elif QIID=="PF301" : Post_PF301_Expr(NTE)
    elif QIID=="PF302" : Post_PF302_Expr(NTE)
    elif QIID=="PF303" : Post_PF303_Expr(NTE)
    elif QIID=="PF304" : Post_PF304_Expr(NTE)
    elif QIID=="PF305" : Post_PF305_Expr(NTE)  
    else:
        for TE in NTE:
            if QIID=="PF101" :   Put_PF101_Expr(TE)
            elif QIID=="PF102" : Put_PF102_Expr(TE)
            elif QIID=="PF103" : Put_PF103_Expr(TE)


"""
PF101有理數運算
"""


def Put_PF101_Expr(TE):
    ''' 檢查作答結果,比對Val == Ans, 對錯OK=[0/1] '''
    ans = lib.Text2St(TE["Ans"])
    Val = TE["Val"]
    try:
        if parse_expr(ans) == Val:  # 比對答案:
            TE["OK"] = 1; return True
    except:
        pass
    return False

def Get_PF101_Expr(QN,Tx=-1):
    TxFlag=Tx==-1
    sample_list0 = list(range(-39, 29))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-39, 29))
    sample_list1.remove(0)              # list1 為 非零數列
    NTE = []
    for Qid in range(0, QN):
        if TxFlag:Tx = 0 if Qid < (QN//2) else 1  # Tx -半題型1 ,-半題型 2
        if Tx == 1:
            a = random.choice(sample_list1)  # 亂數a,b,c, 不為零
            b = random.choice(sample_list1)
            c = random.choice(sample_list1)
            if a == b:
                b = math.copysign(
                    abs(b)+random.choice(range(1, 5)), b)   # a != b
            qiz = sp.Add(sp.Rational(b, a), sp.Rational(c, a), evaluate=False)
            St = sp.latex(qiz)  # 題目
            Val = sp.simplify(qiz)  # 簡化算式,得出標準答案

        else:
            a = random.choice(sample_list0)  # 亂數a,b,c
            b = random.choice(sample_list0)
            c = random.choice(sample_list0)
            qiz = sp.Add(sp.S(a), b, c, evaluate=False)
            St = sp.latex(qiz)  # 題目
            Val = sp.simplify(qiz)  # sympy.simplify簡化算式,得出標準答案


        TE = GetTE(Qid, St, Val, Tx)
        TE["Tip"] = "用分數表逹值: -(a/b)"
        NTE.append(TE)
    return NTE


"""
PF102整數指數冪運算
"""


def Put_PF102_Expr(TE):
    Val = TE["Val"]
    ans = TE["Ans"]
    if ans.strip() == "": ans = "-3.1415926"
    try:
        if parse_expr(ans) == Val:
            TE["OK"] = 1
            return True
    except:
        pass
    return False


def Get_PF102_Expr(QN,Tx=-1):
    TxFlag=Tx==-1
    a,b,c,x,y,z=sp.symbols("a,b,c,x,y,z")
    NTE=[]
    for Qid in range(0,QN):
        if TxFlag: Tx=int(Qid % 6)
        if Tx==1:
            a1=sp.S(random.choice([-5,-4,-3,-2,-1,2,3,4,5]))
            b1=random.choice([-3,-2,-1,2,3])
            c1=random.choice([-3,-2,-1,2,3])
            St=sp.Mul(a1**b1 , a1**c1, evaluate=False)
            Val=sp.simplify(St)
            St=r" {%s}^{%s} \cdot  {%s}^{%s} " % (a1,b1,a1,c1) #Latex    
        elif Tx==2:
            b1=random.choice([-3,-2,-1,2,3])
            c1=random.choice([-3,-2,-1,2,3])
            op=random.choice(["Mul","Div"])
            if op=="Div":
                St=a**b1 / a**c1
                Val=sp.simplify(St)
                St=r" a^{%s} \div  a^{%s} " % (b1,c1) #Latex   \times
            else:
                St=sp.Mul(a**b1 , a**c1, evaluate=False)
                Val=sp.simplify(St)
                St=r" a^{%s} \cdot  a^{%s} " % (b1,c1) #Latex 

        elif Tx==3:
            b1=random.choice([-3,-2,-1,2,3])
            c1=random.choice([-3,-2,-1,2,3])
            St=sp.Pow(sp.Mul(b1*a,evaluate=False) , c1, evaluate=False)
            Val=sp.simplify(St)
            St=r" ({%s}*a)^{%s} " % (b1,c1) #Latex 
            #St=sp.latex(St)

        elif Tx==4:
            b1=random.choice([-3,-2,-1,2,3])
            c1=random.choice([-3,-2,-1,2,3])
            n1=random.choice([-3,-2,-1,2,3])
            op=random.choice(["Mul","Div"])
            St1=sp.Pow(sp.Mul(a**b1 , b**c1, evaluate=False),n1, evaluate=False)
            Val=sp.simplify(St1)
            St=r" (a^{%s} \cdot  b^{%s})^{%s} " % (b1,c1,n1) #Latex 

        elif Tx==5:
            b1=random.choice([-3,-2,-1,2,3])
            c1=random.choice([-3,-2,-1,2,3])
            n1=random.choice([-3,-2,-1,2,3])
            St1=sp.Pow(sp.Mul(a**b1 , b**c1, evaluate=False),n1, evaluate=False)
            St11=r" (a^{%s} \cdot  b^{%s})^{%s} " % (b1,c1,n1) #Latex 
            b1=random.choice([-3,-2,-1,2,3])
            c1=random.choice([-3,-2,-1,2,3])
            n1=random.choice([-3,-2,-1,2,3])
            St2=sp.Pow(sp.Mul(a**b1 , b**c1, evaluate=False),n1, evaluate=False)
            St22=r" (a^{%s} \cdot  b^{%s})^{%s} " % (b1,c1,n1) #Latex 
            op=random.choice(["cdot","div"])
            if op=="div":
                St=St1 / St2
                Val=sp.simplify(St)
                #St=r" {%s} \div  {%s} " % (sp.latex(St1),sp.latex(St2)) #Latex   \times
            else:
                St=sp.Mul(St1 , St2, evaluate=False)
                Val=sp.simplify(St)
            St=r" {%s} \%s  {%s} " % (St11,op,St22) #Latex   \times
        else:
            a1=sp.S(random.choice([-5,-4,-3,-2,-1,1,2,3,4,5]))
            b1=random.choice([-9,-8,-7,-6,-5,-4,-3,-2,2,3,4,5,6,7,8,9])
            c1=random.choice([-3,-2,-1,2,3])
            St=r" {\large (%s)}^{%s} " % (sp.latex(sp.Rational(a1,b1)),c1) #Latex 
            expr=sp.Pow(sp.Rational(a1,b1), c1 ,evaluate=False)
            Val=sp.simplify(expr) #標準答案 
        #運算方法1:
        #運算方法2:
        #Val=(a / sp.S(b))** c
        TE=GetTE(Qid,St,Val,Tx)
        NTE.append(TE)    
    return NTE


"""
PF103一元一次方程
"""

def Post_PF103_Expr(NTE):
    for TE in NTE: Put_PF103_Expr(TE)

def Put_PF103_Expr(TE):
    Val=TE["Val"]
    ans=TE["Ans"] if TE["Ans"] != "" else "3.14159"
    ans = lib.Text2St(ans)
    try:
        if parse_expr(ans) == Val[0]:  # 比對答案:
            TE["OK"] = 1
            return True
    except:
        pass
    return False

def Get_PF103_Expr(QN,Tx=-1):
    TxFlag=Tx==-1
    x=sp.symbols('x')
    NTE=[]
    for Qid in range(0,QN):
        if TxFlag:Tx=int(Qid % 4)
        if Tx==1:
            # 2:  ax+b=cx+d a,b,c,d均為-99至99的整数,
            a=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            b=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            c=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            d=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            expre=sp.Eq(a*x+b,c*x+d,evaluate=False)
            St=sp.latex(expre)
            Val=sp.solve(expre)
        elif Tx==2:
            #3： m(a+bx) + n(c+dx) = p(e+fx) 所有字母均為-9至9整数
            a=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            b=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            c=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            d=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            e=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            f=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            m=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            n=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            expre=sp.Eq(m*(a+b*x)+n*(c+d*x),p*(e+f*x),evaluate=False)
            St=r" %s *(%s+%s*x)+%s*(%s+%s*x)= %s* (%s+%s*x) "%(m,a,b,n,c,d,p,e,f)
            Val=sp.solve(expre)
        elif Tx==3:
            #4： (ax+b)/m + (cx+d)/n = (ex+f)/p 字母a,b,c,d,e,f均為-9至9整数;m,n,f均為1至9的整數
            a=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            b=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            c=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            d=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            e=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            f=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            m=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            n=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            expre=sp.Eq((a+b*x)/m+(c+d*x)/n,(e+f*x)/p,evaluate=False)
            St=r" \frac{%s+%s*x}{%s}+\frac{%s+%s*x}{%s}=\frac{%s+%s*x}{%s} "%(a,b,m,c,d,n,e,f,p)
            Val=sp.solve(expre)
        else:
            a = 1 
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            b=p+q
            c=p*q
            express_str=f" {a}*x + {b} "                    # f(x)= ax + b
            QizStat=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            fx=sp.Eq( QizStat, c )                           #sympy.Eq 方程式 f(x)=c ,
            St=sp.latex(fx)                                  #題目 latex 數學格式
            Val=sp.solve(fx)                                 #sympy.solve求根,得出標準答案
        TE=GetTE(Qid,St,Val,Tx)
        TE["Tip"] = "請填x的值"
        NTE.append(TE)
    return NTE


"""
PF104整式的加減法練習
"""


def Post_PF104_Expr(NTE):
    x = sp.Symbol('x')
    for TE in NTE:
        Val = TE["Val"]
        ans = TE["Ans"]
        if ans.strip() == "": ans = "3.1415"
        ans = lib.Text2St(ans)
        try:

            if parse_expr(ans).subs({x: 7}) == Val.subs({x: 7}):  # 比對答案:
                TE["OK"] = 1
            else:  # 不則
                TE["OK"] = 0
        except:
            pass


def Get_PF104_Expr(QN,Tx=-1):
    TxFlag=Tx==-1    
    x,y,z=sp.symbols('x,y,z')
    NTE=[]
    for Qid in range(0,QN):
        if TxFlag:Tx=int(Qid % 2)
        if Tx==1:
            #( mx2+px)+(nx2+qx) = ax2 + bx  |p|,|q| < 16 整数
            #   p, q = 16以内随机±整数
            #   a=m+n,    b=p∙q 
            m=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            n=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            expr1=m*x**2+p*x
            expr2=n*x**2+q*x
            op=random.choice(["-","-","+"])
            if op=="-":
                Val=expr1-expr2
            else:
                Val=expr1+expr2
            St=r"(%s) %s (%s)"%(sp.latex(expr1),op,sp.latex(expr2))
            
        else:
            a = 1 
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            b=p+q
            c=p*q
            express_str=f"{a}*x + {b}*x + {c}  "       #題型 express_str ax+bx+c
            St=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression
            Val=sp.simplify(St)
            St=sp.latex(St)
        TE=GetTE(Qid,St,Val,Tx)        
        NTE.append(TE)    
    return NTE

  


"""
PF105二元一次方程
"""


def Post_PF105_Expr(NTE):
    x, y, z = sp.symbols('x,y,z')
    for TE in NTE:
        ans = TE["Ans"]
        Val = TE["Val"]
        ans = ans.split(";")
        ans1 = ans[0]
        ans2 = ans[1] if len(ans) > 1 else "3.1415"
        if ans1.strip() == "":
            ans1 = "3.1415"
        if ans2.strip() == "":
            ans2 = "3.1415"
        try:
            ans = {x: parse_expr(ans1), y: parse_expr(ans2)}
            if ans == Val:  # 比對答案:
                TE["OK"] = 1
            else:  # 不則
                TE["OK"] = 0
        except:
            pass
        TE["Val"] = r"\( {} \)".format(sp.latex(Val))


def Get_PF105_Expr(QN,Tx=-1):
    TxFlag=Tx==-1    
    x, y, z = sp.symbols('x,y,z')
    NTE = []
    for Qid in range(0, QN):
        a = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        b = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        c = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        d = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        m = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        n = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        eq1 = sp.Eq(a*x+b*y, m)
        eq2 = sp.Eq(c*x+d*y, n)
        St = [eq1, eq2]
        Val = (sp.solve([eq1, eq2], [x, y]))
        TE = GetTE(Qid, sp.latex(St), Val)
        TE["Tip"] = "求x ,y ?"
        if Val == []:
            pass
        else:
            NTE.append(TE)
    return NTE


"""
PF106一元一次不等式
"""


def Post_PF106_Expr(NTE):
    x = sp.Symbol('x')
    for TE in NTE:
        Val = TE["Val"]
        ans = TE["Ans"]
        if ans == "":
            continue
        try:
            if sp.solve(ans) == Val:  # 比對答案:
                TE["OK"] = 1
            else:  # 不則
                TE["OK"] = 0
        except:
            pass


def Get_PF106_Expr(QN,Tx=-1):
    TxFlag=Tx==-1   


    x=sp.symbols('x')
    NTE=[]
    for Qid in range(0,QN):
        if TxFlag:Tx=Qid % 4
        if Tx==1:
            #ax+b<cx+d a,b,c,d均為-99至99的整数,
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            a=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            b=p+q
            c=p*q
            d=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            op=random.choice([">=",">","<=","<"])
            express_str=f" {a}*x + {b} {op} {c}*x+{d}"       # f(x)= ax + b > c
            fx=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            St=fx
            Val=solve_univariate_inequality(fx,x)      #solve_univariate_inequality 解不等式   
        elif Tx==2:
            #m(a+bx)+n(c+dx)<p(e+fx)  所有字母均為-9至9整数            
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            a=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            b=p+q
            c=p*q
            d=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            e=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            f=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            m=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            n=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            op=random.choice([">=",">","<=","<"])
            express_str=f" {m}*({a}*x + {b})+{n}*({c}*x+{d}) {op} {p}*({f}*x+{e})  "       # f(x)= ax + b > c
            fx=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            St=fx
            Val=solve_univariate_inequality(fx,x)      #solve_univariate_inequality 解不等式   
        elif Tx==3:
            #(a+bx)/m+(c+dx)/n<(e+fx)/p  所有字母均為-9至9整数
            
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            a=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            b=p+q
            c=p*q
            d=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            e=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            f=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            m=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            n=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            op=random.choice([">=",">","<=","<"])
            express_str=f" ({a}*x+ {b})/{m} +({c}*x+{d})/{n} {op} ({f}*x+{e})/{p}  "       # f(x)= ax + b > c
            fx=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            St=fx
            Val=solve_univariate_inequality(fx,x)      #solve_univariate_inequality 解不等式   
        else:
            a = 1 
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            b=p+q
            c=p*q
            op=random.choice([">=",">","<=","<"])
            St=a*x +b
            if op==">=":
                St= St >= c
            elif op==">":
                St= St > c
            elif op=="<=":
                St= St <= c
            elif op=="<":
                St= St < c
            Val=solve_univariate_inequality(St,x)      #solve_univariate_inequality 解不等式   
        
        TE = GetTE(Qid, sp.latex(St), Val,Tx)
        NTE.append(TE)
    return NTE


"""
PF107一元一次不等式組
"""


def Post_PF107_Expr(NTE,i=-1):
    x = sp.symbols('x')
    for idx,TE in enumerate(NTE):
        if i==-1 or i==idx:
            pass
        else:
            continue
        Val = TE["Val"]
        Flag = False
        ans = TE["Ans"]
        ans = re.sub(r"[<][ ]*x[ ]*[<]", r"<x & x<", ans)
        ans = re.sub(r"[>][ ]*x[ ]*[>]", r">x & x>", ans)        
        if ans == "": ans = "(-oo < x) & (x < oo)"
        a1 = ans.split("|")
        a2 = ans.split("&")
        try:
            if len(a1) > 1:
                a_ = []
                for aa_ in a1:
                    a_.append(sp.solve(aa_))
                Flag = (a_[0] | a_[1]) == Val
            elif len(a2) > 1:
                a_ = []
                for aa_ in a2:
                    a_.append(sp.parse_expr(aa_))
                Flag = reduce_rational_inequalities([[a_[0], a_[1]]], x) == Val
            elif ans == '0':
                if str(Val) == "False":
                    Flag = True
            else:
                Flag = sp.solve(ans) == Val
            if Flag:  # 比對答案:
                TE["OK"] = 1
            else:  # 不則
                TE["OK"] = 0
        except:
            pass

def Get_PF107_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       
    x=sp.symbols('x')
    NTE=[]
    for Qid in range(0,QN):
        if TxFlag:Tx=Qid % 4
        if Tx==1:
            op1=random.choice([">","<"])
            op2=random.choice([">","<"])
            a = random.choice([-5,-4,-3,-2,-1,1,2,3,4,5]) 
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            b=p+q
            c =p*q
            d=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            e=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            f=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            g=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            h=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            
            express_str=f" {a}* x+ {b}  {op1} {c}* x+ {d} "                    # f(x)= ax + b
            fx1=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            express_str=f" {e}* x+ {f}   {op2} {g}* x+ {h} "                    # f(x)= ax + b
            fx2=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            #St=[sp.latex(fx1),sp.latex(fx2)]               #題目
            St=r"\left\{\begin{array}\\ %s  \\  %s  \\  \end{array}\right."%(sp.latex(fx1),sp.latex(fx2))  
            Val1=solve_univariate_inequality(fx1,x)         
            Val2=solve_univariate_inequality(fx2,x)  
            #Val= reduce_rational_inequalities([[fx1],[fx2]],x) # or
            Val= reduce_rational_inequalities([[fx1,fx2]],x)   # and
            #Val= Val1 & Val2

        elif Tx==2:
            op1=random.choice([">","<"])
            op2=random.choice([">","<"])
            a = random.choice([-5,-4,-3,-2,-1,1,2,3,4,5]) 
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            b=p+q
            c =p*q
            d=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            e=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            f=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            g=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            h=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            i=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            j=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            k=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            l=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            m=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            n=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            r=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            s=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])            
            express_str=f" {m}* ({a}* x+ {b})+{n}* ({c}* x+ {d})   {op1} {p}*({f}* x+ {e}) "                    # f(x)= ax + b
            fx1=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            express_str=f" ({g}* x+ {h})/{q}+ ({i}* x+ {j})/{r}  {op2} ({k}* x+ {l})/{s} "                    # f(x)= ax + b
            fx2=parse_expr(express_str, evaluate=False) #字串解釋為可運算式子 expression 
            #St=[sp.latex(fx1),sp.latex(fx2)]               #題目
            St=r"\left\{\begin{array}\\ %s  \\  %s  \\  \end{array}\right."%(sp.latex(fx1),sp.latex(fx2))  
            Val1=solve_univariate_inequality(fx1,x)         
            Val2=solve_univariate_inequality(fx2,x)  
            #Val= reduce_rational_inequalities([[fx1],[fx2]],x) # or
            Val= reduce_rational_inequalities([[fx1,fx2]],x)   # and
            #Val= Val1 & Val2
        elif Tx==3:
            op1=random.choice([">","<"])
            op2=random.choice([">","<"])
            a = random.choice([-5,-4,-3,-2,-1,1,2,3,4,5]) 
            b=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            c=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            d=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            e=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            m=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            n=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            if m==n: n=int(math.copysign(abs(n)+5,m))
            if m>n:
                temp=n
                n=m
                m=temp
            expr1=R"\frac{%s * x + (%s)}{%s}"%(a,b,c)
            if op1==">":
                express_str=f"{n} > {expr1}  > {m} "                    # f(x)= ax + b
                fx1=parse_expr(f"{n} > ({a}* x+ {b})/{c}", evaluate=False) #字串解釋為可運算式子 expression 
                fx2=parse_expr(f"({a}* x+ {b})/{c} > {m}" , evaluate=False) #字串解釋為可運算式子 expression 
            else:
                express_str=f"{m} < {expr1}  < {n} "                    # f(x)= ax + b
                fx1=parse_expr(f"{m} < ({a}* x + {b})/{c}", evaluate=False) #字串解釋為可運算式子 expression 
                fx2=parse_expr(f"({a}* x + {b})/{c} < {n}" , evaluate=False) #字串解釋為可運算式子 expression 
            #St=[sp.latex(fx1),sp.latex(fx2)]               #題目
            St=express_str
            Val1=solve_univariate_inequality(fx1,x)         
            Val2=solve_univariate_inequality(fx2,x)  
            #Val= reduce_rational_inequalities([[fx1],[fx2]],x) # or
            Val= reduce_rational_inequalities([[fx1,fx2]],x)   # and
            #Val= Val1 & Val2            
        else:
            op1=random.choice([">","<"])
            op2=random.choice([">","<"])
            p=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            q=random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
            fx1= x > p if op1==">" else x < p
            fx2=  x > q if op2==">" else x < q
            #St=[sp.latex(fx1),sp.latex(fx2)]               #題目
            St=r"\left\{\begin{array}\\ %s  \\  %s  \\  \end{array}\right."%(sp.latex(fx1),sp.latex(fx2))  
            Val= reduce_rational_inequalities([[fx1,fx2]],x)   # and
        TE = GetTE(Qid, St, Val, Tx)
        TE["Tip"] = "請作答 空集輸入 0; 等於某值  Ne(x,0) "
        NTE.append(TE)
    return NTE


"""
PF108整式的乘法練習
"""


def Post_PF108_Expr(NTE):
    x = sp.Symbol('x')
    for TE in NTE:
        Val = TE["Val"]
        ans = TE["Ans"]
        if ans.strip() == "": ans = "3.1415926"
        ans = lib.Text2St(ans)
        try:
            if parse_expr(ans).subs({x: 7}) == Val.subs({x: 7}):  # 比對答案:
                TE["OK"] = 1
            else:  # 不則
                TE["OK"] = 0
        except:
            pass


def Get_PF108_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       
    NTE = []
    for Qid in range(0, QN):
        a = 1
        p = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        q = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        b = p+q
        c = p*q
        express_str = f"(x +({a}))* ( x + ({b}))  "  # 題型 express_str ax+bx+c
        St = parse_expr(express_str, evaluate=False)  # 字串解釋為可運算式子 expression
        Val = sp.expand(St)
        TE = GetTE(Qid, sp.latex(St), Val, Tx)
        NTE.append(TE)
    return NTE


"""
PF201根式的運算
"""


def Post_PF201_Expr(NTE):
    x=sp.Symbol('x')
    for TE in NTE:
        Val=TE["Val"]
        ans=TE["Ans"]
        if ans.strip() == "": ans = "3.1415926"
        ans=lib.Text2St(ans)
        try:
            if parse_expr(ans).subs({x:7})==Val.subs({x:7}):                   #比對答案:
                TE["OK"]=1
            else:                                      #不則
                TE["OK"]=0
        except:
            pass

def Get_PF201_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       
    sample_list0= list(range(-39,29))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1= list(range(8,20))    #sample_list1.remove(0)    # 非零數列
    b_li=list(range(1,18))
    b_li.remove(4)
    b_li.remove(9)
    b_li.remove(16)
    
    NTE=[]
    for Qid in range(0,QN):
        if TxFlag:Tx=Qid%4
        if Tx==1:
            a=random.choice(range(2,18))
            b=random.choice(b_li)
            c=random.choice(range(2,15))
            d=random.choice(range(2,15))
            m=c*c*b
            n=d*d*b
            St=r"\sqrt{%s} + \sqrt{%s} "% (m,n)
            Val=sp.sqrt(m)+sp.sqrt(n)
        elif Tx==2:
            a=random.choice(range(1,11))
            b=random.choice(b_li)
            c=random.choice(range(1,10))
            d=random.choice(range(1,10))
            e=random.choice([-1,-1,1])
            m=c*c*b
            n=d*d*b
            if e==-1:
                St=r"\sqrt{%s} \times {(\sqrt{%s})}^{%s} "% (m,n,e)
            else:
                St=r"\sqrt{%s} \times {\sqrt{%s}} "% (m,n)
            Val=sp.sqrt(m)*sp.sqrt(n)**e
        elif Tx==3:
            a=random.choice(range(1,11))
            c=random.choice(range(1,10))
            b=random.choice(b_li)
            d=random.choice(b_li)
            l=random.choice(range(1,10))
            e=random.choice([-1,1])
            m=a*a*b
            n=c*c*d
            if m==n: e=1
            if e==-1:
                St=r"\frac{\sqrt{%s}}{  \sqrt{%s} - (\sqrt{%s})} "% (l,m,n)
            else:
                St=r"\frac{\sqrt{%s}}{  \sqrt{%s} + (\sqrt{%s})} "% (l,m,n)
            Val=sp.sqrt(l) /( sp.sqrt(m) +e* sp.sqrt(n))
            Val=sp.simplify(Val)

            
        else:
            a=random.choice(range(2,18))
            b=random.choice(b_li)
            m=a*a*b
            St=r"\sqrt{%s}"% m
            Val=sp.sqrt(m)    
        TE = GetTE(Qid, St, Val, Tx)
        TE["Tip"]='請作答sqrt(2) 可寫 J(2 ):'
        NTE.append(TE)
    return NTE


"""
PF202整式的乘法公式平方差
"""


def Post_PF202_Expr(NTE):
    x=sp.Symbol('x')
    for TE in NTE:
        Val=TE["Val"]
        ans=TE["Ans"]
        ans = lib.Text2St(ans)
        if ans.strip()=="":ans="3.1415"
        try:
            if parse_expr(ans).subs({x:7})==Val.subs({x:7}):                   #比對答案:
                TE["OK"]=1
            else:                                      #不則
                TE["OK"]=0
        except:
            pass


def Get_PF202_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       
    sample_list1 = list(range(-19, 19))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        if TxFlag : Tx=Qid % 2
        if Tx==0:
            a = random.choice(sample_list1)
            p = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            q = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            b = p+q
            c = p*q
            express_str = f"(x +({a})) * ( x - ({a}))  "  # 題型 express_str ax+bx+c
        elif Tx==1:
            a = random.choice(sample_list1)
            p = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            q = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            b = p+q
            c = p*q
            op=random.choice(["-","-","+"])
            express_str = f"({p}*x  {op} ({q}) *  y )**2   "  # 題型 express_str ax+bx+c
        else:
            a = random.choice(sample_list1)
            p = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            q = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            b = p+q
            c = p*q
            express_str = f"(x +({a})) * ( x - ({a}))  "  # 題型 express_str ax+bx+c
        St = parse_expr(express_str, evaluate=False)  # 字串解釋為可運算式子 expression
        Val = sp.expand(St)
        TE = GetTE(Qid, sp.latex(St), Val, Tx)
        NTE.append(TE)
    return NTE


"""
PF203因式分解提公因式
"""


def Post_PF203_Expr(NTE):
    x,y,z=sp.symbols('x,y,z')
    for TE in NTE:
        Val = TE["Val"]
        ans=TE["Ans"]
        ans=lib.Text2St(ans)
        if ans.strip()=="": ans="3.1415"
        subsV={x:7,y:11,z:17}
        try:
            if parse_expr(ans).subs(subsV)==Val.subs(subsV):                   #比對答案:
                TE["OK"]=1
        except:
            pass
        TE["Val"] = r"\( %s \)" % sp.latex(Val)


def Get_PF203_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       
    NTE = []
    for Qid in range(0, QN):
        a = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        b = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        c = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        ab = a*b
        ac = a*c
        p = random.choice([0, 1, 2, 3, 4, 5])
        q = random.choice([0, 1, 2, 3, 4, 5])
        u = random.choice([0, 1, 2, 3, 4, 5])
        v = random.choice([0, 1, 2, 3, 4, 5])
        # 題型 express_str ax+bx+c
        express_str = f"{ab} * x**{p} * y**{q}  + {ac} * x**{u}*y**{v}  "
        St = parse_expr(express_str, evaluate=False)  # 字串解釋為可運算式子 expression
        Val = sp.factor(St)
        TE = GetTE(Qid, sp.latex(St), Val, Tx)
        NTE.append(TE)
    return NTE


"""
PF204分式的乘除
"""


def Post_PF204_Expr(NTE):
    x=sp.Symbol('x')
    for TE in NTE:
        Val = TE["Val"]
    for TE in NTE:
        Val=TE["Val"]
        ans=TE["Ans"]
        ans=lib.Text2St(ans)
        try:
            if parse_expr(ans).subs({x:7})==Val.subs({x:7}):                   #比對答案:
                TE["OK"]=1
            else:                                      #不則
                TE["OK"]=0
        except:
            pass
        TE["Val"] = r"\( %s \)" % sp.latex(Val)


def Get_PF204_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       
    x, y, z, m, n = sp.symbols('x,y,z,m,n')
    op_list = ["*", "/"]
    sample_list0 = list(range(1, 17))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-39, 29))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        op = random.choice(op_list)
        a = random.choice(sample_list0)
        b = random.choice(sample_list0)
        c = random.choice(sample_list0)
        d = random.choice(sample_list0)
        p = random.choice(sample_list0)
        q = random.choice(sample_list0)
        r = random.choice(sample_list0)
        u = random.choice(sample_list0)
        v = random.choice(sample_list0)
        p1 = random.choice(sample_list0)
        q1 = random.choice(sample_list0)
        r1 = random.choice(sample_list0)
        u1 = random.choice(sample_list0)
        v1 = random.choice(sample_list0)
        fx1 = (a*x**p*y**q*z**r)/(b*m**u*n**v)
        fx2 = (d*m**u1*n**v1)/(c*x**p1*y**q1*z**r1)
        TE = GetTE(Qid, None, None, Tx)
        if op == "*":
            St = sp.Mul(fx1, fx2, evaluate=False)
            TE["St"] = sp.latex(St)
        elif op == "/":
            St = fx1/fx2
            fx1latex = sp.latex(fx1)
            fx2latex = sp.latex(fx2)
            TE["St"] = f" {fx1latex} \div {fx2latex}"
        Val = sp.simplify(St)
        TE["Val"] = Val
        NTE.append(TE)
    return NTE


"""
PF205分式的加減
"""


def Post_PF205_Expr(NTE):
    for TE in NTE:
        Val=TE["Val"]
        ans=TE["Ans"]
        ans=lib.Text2St(ans)
        try:
            if parse_expr(ans).subs({x:7})==Val.subs({x:7}):                   #比對答案:
                TE["OK"]=1
            else:                                      #不則
                TE["OK"]=0
        except:
            pass
        TE["Val"] = r"\(%s\)" % sp.latex(Val)


def Get_PF205_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    x, y, z = sp.symbols('x,y,z')
    op_list = ["+", "-"]
    sample_list0 = list(range(1, 16))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(0, 11))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        if TxFlag : Tx= 0
        op = random.choice(op_list)
        a = random.choice(sample_list0)
        b = random.choice(sample_list0)
        c = random.choice(sample_list0)
        d = random.choice(sample_list0)
        h = random.choice(sample_list1)
        k = random.choice(sample_list1)
        h1 = random.choice(sample_list1)
        k1 = random.choice(sample_list1)
        e = lib.lcm(a, b)
        f = lib.lcm(a, b) // a
        g = lib.lcm(a, b) // b
        p = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        q = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        if p+q==0: q=int(math.copysign((abs(q)+2),q))
        b = p+q
        c = p*q
        fx1 = c / (a*x**h*y**k)
        fx2 = d / (b*x**h1*y**k1)
        St = sp.S(0)
        if op == "+":
            St = sp.Add(fx1, fx2)
        if op == "-":
            St = fx1-fx2
        Val = sp.simplify(St)
        TE = GetTE(Qid, sp.latex(St), Val, Tx)
        NTE.append(TE)
    return NTE


"""
PF206分式方程
"""


def Post_PF206_Expr(NTE):
    for TE in NTE:
        x=sp.Symbol('x')
        Val=TE["Val"]
        ans=TE["Ans"]
        ans=lib.Text2St(ans)
        try:
            if parse_expr(ans).subs({x:7})==Val[0].subs({x:7}):                   #比對答案:
                TE["OK"]=1
            else:                                      #不則
                TE["OK"]=0
        except:
            pass


def Get_PF206_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    x = sp.Symbol('x')
    sample_list0 = list(range(1, 8))     # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(0, 10))
    sample_list2 = list(range(-10, 10))  # sample_list1.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        a = random.choice(sample_list0)
        a1 = random.choice(sample_list0)
        c = random.choice(sample_list1)
        c1 = random.choice(sample_list1)
        ac1 = a*c1
        a1c = a1*c
        aclcm = lib.lcm(ac1, a1c)
        c1 = aclcm//a
        c = aclcm//a1
        b = random.choice(sample_list2)
        b1 = random.choice(sample_list2)
        d = random.choice(sample_list2)
        d1 = random.choice(sample_list2)
        expr1 = (c * x+d)/(a*x+b)
        expr2 = (c1 * x+d1)/(a1*x+b1)
        St = sp.Eq(expr1, expr2)  # f1(x)=f2(x)
        Val = sp.solve(St)
        TE = GetTE(Qid, sp.latex(St), Val, Tx)
        if Val == []:
            pass
        else:
            NTE.append(TE)
    return NTE


"""
PF207一次函數圖像的性質
"""


def Post_PF207_Expr(NTE):
    for TE in NTE:
        Val=TE["Val"]
        ans=TE["Ans"]
        ans=lib.Text2St(ans)
        try:
            if parse_expr(ans)==Val:                   #比對答案:
                TE["OK"]=1
            else:                                      #不則
                TE["OK"]=0
        except:
            pass


def Get_PF207_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    x, y, z = sp.symbols('x,y,z')
    sample_list0 = list(range(-10, 10))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-10, 10))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        k = random.choice(sample_list1)
        b = random.choice(sample_list0)
        St = sp.Eq(y, k*x+b)  
        Val = 1
        if k < 0:
            Val = -1
        TE = GetTE(Qid, sp.latex(St), Val, Tx)
        TE["Tip"] = " y 隨 x 的增大而____  (  +1 表示 增大  或  -1 表示  減少 )"
        
        try:
            TE["PlotImg"]="img"+GetKey()+str(Qid)+".png"
            expr= k*x+b
            lam_x = lambdify(x, expr, modules=['numpy'])
            x_vals = np.linspace(-5, 5, 10)
            y_vals = lam_x(x_vals)
            fig = Figure()
            ax = fig.subplots()
            ax.plot(x_vals, y_vals)
            ax.axhline(0, color='black')
            ax.axvline(0, color='black')            
            fig.savefig(os.getcwd()+"\\static\\"+TE["PlotImg"])
            # Save it to a temporary buffer.
            #buf = BytesIO()
            #fig.savefig(buf, format="png")
            #data = base64.b64encode(buf.getbuffer()).decode("ascii")
            #return f"<img src='data:image/png;base64,{data}'/>"        
        except:
            TE["PlotImg"]=None
        NTE.append(TE)

    return NTE


"""
PF291一元二次方程式十字相乘法求因式
"""


def Post_PF291_Expr(NTE):
    x=sp.Symbol('x')
    for TE in NTE:
        Val=TE["Val"]
        ans=TE["Ans"]
        ans = lib.Text2St(ans)
        try:
            if parse_expr(ans).subs({x:7})==Val.subs({x:7}):                   #比對答案:
                TE["OK"]=1
            else:                                      #不則
                TE["OK"]=0
        except:
            pass
    



def Get_PF291_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    sample_list0 = list(range(-39, 29))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-39, 29))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        a = 1
        p = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        q = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        b = p+q
        c = p*q
        express_str = f"{a}*x**2 + {b}*x +  {c} "
        St = parse_expr(express_str, evaluate=False)  # 字串解釋為可運算式子 expression
        Val = sp.factor(St)  # 因式分解,得出標準答案
        TE = GetTE(Qid, sp.latex(St), Val, Tx)
        TE["Tip"] = "十字相乘法因式分解"
        NTE.append(TE)
    return NTE


"""
PF292一元二次方程式求解
"""


def Post_PF292_Expr(NTE):
    for TE in NTE:
        Val=TE["Val"]
        ans_=TE["Ans"].split(";")
        try:
            cnt=0
            for idx in ans_:
                for v_ in Val:
                    if int(idx)==v_ : cnt+=1
            if cnt>1:                   #比對答案:
                TE["OK"]=1
            else:                                      #不則
                TE["OK"]=0
        except:
            pass
        


def Get_PF292_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    sample_list1 = list(range(-39, 29))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        a = 1
        p = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        q = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        b = p+q
        c = p*q
        express_str = f"{a}*x**2 + {b}*x +  {c} "
        St = parse_expr(express_str, evaluate=False)  # 字串解釋為可運算式子 expression
        St = sp.Eq(St, 0)  # f(x)=0
        Val = sp.solve(St)  # 因式分解,得出標準答案
        TE = GetTE(Qid, sp.latex(St), Val, Tx)
        TE["Tip"] = "解方程 x1, x2?"
        NTE.append(TE)
    return NTE


"""
PF293整式的乘法練習
"""


def Post_PF293_Expr(NTE):
    x=sp.Symbol('x')
    for TE in NTE:
        Val=TE["Val"]
        ans=TE["Ans"]
        ans = lib.Text2St(ans)
        try:
            if parse_expr(ans).subs({x:7})==Val.subs({x:7}):                   #比對答案:
                TE["OK"]=1
            else:                                      #不則
                TE["OK"]=0
        except:
            pass
    

def Get_PF293_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    sample_list0 = list(range(-39, 29))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-39, 29))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        a = 1
        p = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        q = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        b = p+q
        c = p*q
        express_str = f"(x +({a}))* ( x + ({b}))  "  # 題型 express_str ax+bx+c
        St = parse_expr(express_str, evaluate=False)  # 字串解釋為可運算式子 expression
        Val = sp.expand(St)
        TE = {}
        TE = GetTE(Qid, sp.latex(St), Val, Tx)
        TE["Tip"] = "整式的乘法練習,開展式子"
        NTE.append(TE)
    return NTE


"""
PF301一元二次方程式
"""
def Post_PF301_Expr(NTE):
    for TE in NTE:
        Val=TE["Val"]
        ans_=TE["Ans"].split(";")
        ans=[]
        ans_idx=[]
        try:
            cnt=0
            for idx,value in enumerate(ans_):
                ans.append(parse_expr(value))
            
            for idx, a_ in enumerate(ans):
                for vidx, v_ in enumerate(Val):
                    if a_==v_ : 
                        if vidx in ans_idx:
                            pass
                        else:
                            cnt+=1
                            ans_idx.append(vidx)
            if cnt==len(Val):                   #比對答案:
                TE["OK"]=1
            else:                                      #不則
                TE["OK"]=0
        except:
            pass

    


def Get_PF301_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    x, y, z = sp.symbols('x,y,z')
    sample_list0 = list(range(-39, 29))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-39, 29))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        Tx = Qid % 4 + 1
        a = 1
        p = random.choice(range(-10, 10))
        q = random.choice(range(-10, 10))
        b = p+q
        c = p*q
        if Tx == 2:
            p = random.choice(range(-15, 15))
            q = random.choice(range(-15, 15))
            b = p+q
            c = p*q
        elif Tx == 3:
            m = random.choice(range(1, 6))
            n = random.choice(range(1, 6))
            a = m*n
            p = random.choice(range(-10, 10))
            q = random.choice(range(-10, 10))
            b = p*n+q*m
            c = p*q
        elif Tx == 4:
            m = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            n = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            if m*n > 0:
                n = n*-1
            a = m*n
            p = random.choice(range(-10, 10))
            q = random.choice(range(-10, 10))
            b = p*n+q*m
            c = p*q
        else:
            pass

        St = sp.Add(a*x**2, b*x, c, evaluate=False)
        St = sp.Eq(St, 0)  # f(x)=0
        Val = sp.solve(St)  # 因式分解,得出標準答案
        TE = GetTE(Qid, sp.latex(St), Val, Tx)
        TE["Tip"] = "因式分解"
        NTE.append(TE)
    return NTE


"""
PF302解可化為一元二次方程的分式方程
"""

def Post_PF302_Expr(NTE):
    for TE in NTE:
        Val=TE["Val"]
        ans_=TE["Ans"].split(";")
        ans=[]
        ans_idx=[]
        try:
            cnt=0
            for value in ans_:
                ans.append(parse_expr(lib.Text2St(value)))
            
            for idx, a_ in enumerate(ans):
                for vidx, v_ in enumerate(Val):
                    if a_==v_ : 
                        if vidx in ans_idx:
                            pass
                        else:
                            cnt+=1
                            ans_idx.append(vidx)
            if cnt==len(Val):                   #比對答案:
                TE["OK"]=1
            else:                                      #不則
                TE["OK"]=0
        except:
            pass


    


def Get_PF302_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    x, y, z = sp.symbols('x,y,z')
    sample_list1 = list(range(-10, 10))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        Tx = Qid % 4 + 1
        a = random.choice(sample_list1)
        b = random.choice(sample_list1)
        b = sp.Integer(math.copysign(b, a))
        fx1 = a / (x**2)
        St = sp.Eq(fx1, b)  # f(x)=0
        if Tx == 2:
            if a*a+4*b >= 0:
                fx1 = a / x
                fx2 = b / (x**2)
                fx = sp.Add(fx1, fx2, evaluate=False)
                St = sp.Eq(fx, sp.Integer(1))  # f(x)=0
        elif Tx == 3:
            m = random.choice(range(1, 6))
            n = random.choice(range(1, 6))
            a = m*n
            p = random.choice(range(-10, 10))
            q = random.choice(range(-10, 10))
            b = p*n+q*m
            c = p*q
        elif Tx == 4:
            m = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            n = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            if m*n > 0:
                n = n*-1
            a = m*n
            p = random.choice(range(-10, 10))
            q = random.choice(range(-10, 10))
            b = p*n+q*m
            c = p*q
        else:
            pass
        Val = sp.solve(St)  # 因式分解,得出標準答案
        TE = GetTE(Qid, sp.latex(St), Val, Tx)
        NTE.append(TE)
    return NTE


"""
PF303解二元二次方程組
"""


def Post_PF303_Expr(NTE):
    for TE in NTE:
        Val=TE["Val"]
        ans_=TE["Ans"].split(";")
        try:
            cnt=0
            for idx in ans_:
                for v_ in Val:
                    if int(idx)==v_ : cnt+=1
            if cnt>1:                   #比對答案:
                TE["OK"]=1
            else:                                      #不則
                TE["OK"]=0
        except:
            pass


def Get_PF303_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    x, y = sp.symbols('x,y')
    NTE = []
    for Qid in range(0, QN):
        p = random.choice(range(-10, 10))
        q = random.choice(range(-10, 10))
        b = p+q
        c = p*q
        f = p*q
        l = (p+q)
        eq1 = sp.Eq(x+y, b)
        eq2 = sp.Eq(x*y, c)
        St = [eq1, eq2]
        Val = sp.solve([eq1, eq2], x, y)
        #Val=sp.solve([x+y+f,x*y+l],x,y)
        St = [sp.latex(eq1), sp.latex(eq2)]  # 題目
        TE = GetTE(Qid, St, Val, Tx)
        TE["Tip"] = "分別給出,x 和 y 值"
        NTE.append(TE)
    return NTE


"""
PF304二次函數圖像的性質
"""


def Post_PF304_Expr(NTE):
    for TE in NTE:
        Val=TE["Val"]
        ans=TE["Ans"].split(";")
        anss=[]
        try:
            for idx in ans:
                if idx=="" : idx="0"
                anss.append(parse_expr(lib.Text2St(idx)))
            Flag=0
            for v_ in Val:
                for a_ in ans:
                    if(v_==a_): Flag+=1
            if Flag>1:                   #比對答案:
                TE["OK"]=1
            else:                                           #不則
                TE["OK"]=0
        except:
            pass

def Get_PF304_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    x, y, z = sp.symbols('x,y,z')
    sample_list0 = list(range(-10, 10))   # [-5,-4,-3,-2,-1,1,2,3,4,5]
    sample_list1 = list(range(-10, 10))
    sample_list1.remove(0)    # 非零數列
    NTE = []
    for Qid in range(0, QN):
        a = random.choice(sample_list1)
        h = random.choice(sample_list0)
        k = random.choice(sample_list0)
        St = sp.Eq(y, a*(x-h)**2+k)  # , evaluate=False) #字串解釋為可運算式子 expression
        Val = [h, k]
        TE = GetTE(Qid, sp.latex(St), Val, Tx)
        TE["Tip"] = "頂點坐標x ,y ?"
        #TE["Plot"]=a*(x-h)**2+k
        NTE.append(TE)
    return NTE


"""
PF305解直角三角形    
"""


def Post_PF305_Expr(NTE):
    pass


def sjstr(a, d, e):
    triang_fnc = ["", "sin", "cos", "tan"]
    str = triang_fnc[a]
    if e == 2:
        str += "^2"
    ang_degree = ["", "0^o", "30^o", "45^o", "60^o", "90^o"]
    return str+ang_degree[d]


def ang_expre(a, d, e):
    ad = [sp.pi, sp.pi*0, sp.pi/6, sp.pi/4, sp.pi/3, sp.pi/2]
    f = sp.S(1)
    if a == 1:
        f = sp.sin(ad[d])
    elif a == 2:
        f = sp.cos(ad[d])
    elif a == 3:
        f = sp.tan(ad[d])
    elif a == 4:
        f = sp.atan(ad[d])
    if e == 2:
        f = f**2
    return f
############################################################################


def Get_PF305_Expr(QN,Tx=-1):
    TxFlag=Tx==-1       

    NTE = []
    for Qid in range(0, QN):
        op = random.choice([" + ", " - ", " * ", " / "])
        e = random.choice([1, 2])
        a = random.choice([1, 2, 3])
        b = random.choice([1, 2, 3])
        d1 = random.choice([1, 2, 3, 4, 5])
        d2 = random.choice([1, 2, 3, 4, 5])

        if a == 3 and d1 == 5:
            d1 = 4
        if b == 3 and d2 == 5:
            d2 = 4
        St = sjstr(a, d1, e) + op + sjstr(b, d2, 1)
        if op == " / ":
            St = sjstr(a, d1, e) + "\div " + sjstr(b, d2, 1)
        Val = sp.S(0)
        print(ang_expre(a, d1, e))
        print(ang_expre(b, d2, 1))

        if op == " + ":
            Val = ang_expre(a, d1, e) + ang_expre(b, d2, 1)
        elif op == " - ":
            Val = ang_expre(a, d1, e) - ang_expre(b, d2, 1)
        elif op == " * ":
            Val = ang_expre(a, d1, e) * ang_expre(b, d2, 1)
        elif op == " / ":
            Val = ang_expre(a, d1, e) / ang_expre(b, d2, 1)

        TE = GetTE(Qid, St, Val, Tx)
        NTE.append(TE)
    return NTE
