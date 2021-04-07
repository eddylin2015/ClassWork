from .. import get_model, login_required_auth, storage
from flask import Blueprint, current_app, redirect, render_template, request, \
    session, url_for , send_file    
import redis    
import pickle
import json    
import os
import base64
from io import BytesIO
from matplotlib.figure import Figure

QAMT=10
rediscli = redis.Redis(host='localhost', port=6379, db=0)

mathsym = Blueprint('mathsym', __name__)

def upload_image_file(file):
    """
    Upload the user-uploaded file to Google Cloud Storage and retrieve its
    publicly-accessible URL.
    """
    if not file:
        return None

    public_url = storage.upload_file(
        file.read(),
        file.filename,
        file.content_type
    )

    current_app.logger.info(
        "Uploaded file %s as %s.", file.filename, public_url)

    return public_url

# 使用模版list.html, 顯示列表 
@mathsym.route("/apps")
def list():
    books=["PF101.4.有理數運算",          "PF102.6.整數指數冪運算","PF103.4.一元一次方程",
        "PF104.4.整式的加減法練習",    "PF105.4.二元一次方程","PF106.4.一元一次不等式",
        "PF107.4.一元一次不等式組",    "PF108.4.整式的乘法練習","PF201.4.根式的運算",
        "PF202.4.整式的乘法公式平方差","PF203.4.因式分解提公因式","PF204.4.分式的乘除",
        "PF205.4.分式的加減",         "PF206.4.分式方程","PF207.4.一次函數圖像的性質",
        "PF291.4.一元二次方程式十字相乘法求因式","PF292.4.一元二次方程式求解",
        "PF293.4.整式的乘法練習",  "PF301.4.一元二次方程式","PF302.4.解可化為一元二次方程的分式方程",
        "PF303.4.解二元二次方程組","PF304.4.二次函數圖像的性質","PF305.4.解直角三角形"]
    return render_template(
        "mathsym/list.html",
        books=books
        )    

# [START CODE 數學出題及比對答案]
import esmathlib as lib    # 自定義,數學出題庫
# GET 顯示4題QID相關算式
# POST 收集作答,並對比答案.
@mathsym.route("/apps/<QID>", methods=['GET', 'POST'])
@login_required_auth
def MathPanel(QID):
    Tx = int(request.args.get('Tx', "-1"))
    QIID=QID.split(".")[0]
    if request.method == 'POST':
        SID = request.form["SID"]
        # POST 收集作答, 並對比答案. 
        # 取得題目及電腦標準答案 (NTE)
        # objstr=rediscli.get(SID)
        # rediscli.delete(SID)
        objstr=get_model().NTERead(SID)
        if objstr==None: return redirect('/mathsym/apps')
        NTE=pickle.loads(objstr["nte"]) # get_model().NTEDelete(SID)
        # 更新NTE中的 作答(Ans)㯗位資料.
        lib.Post_Expr_UpdateAns(request.form, NTE) 
        # 檢查比對作答與電腦答案.
        lib.Post_Expr_CheckAns(QIID, NTE)          
        # 顯示結果表格.
        return render_template("mathsym/result.html", title=QID, NTE=NTE)    
    # GET 顯示 QIID 相關算式
    NTE=lib.Get_Expr(QIID,QAMT,Tx)
    SID=lib.GetKey(QIID)   
    get_model().NTECreate({"id":SID,"nte":pickle.dumps(NTE)})
    # rediscli.set(SID,pickle.dumps(NTE)) 
    return render_template("mathsym/form.html", title=QID, NTE=NTE, sid=SID)      

@mathsym.route('/apps/img/<filename>')
def showimage(filename):
    # Get current path os.getcwd()
    try:
        FilePath=os.getcwd()+"/static/"+filename
        return send_file(FilePath,
                mimetype = 'image/*')
    except:
        pass

@mathsym.route("/apps/showPlt")
def showPlt():
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    ax.plot([1, 2])
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"        
# [END CODE]
