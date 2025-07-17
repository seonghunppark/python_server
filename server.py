from flask import Flask
from flask import render_template 
from flask import request, redirect, make_response
from aws import detect_labels_local_file as label
from aws import compare_faces 
from werkzeug.utils import secure_filename

app = Flask(__name__)


# 1. Day13.py에 /campare라는 경로 만들기
# 2. home.html에 입력태그(form) 하나 추가
# 이미지 2개를 (file1, file2)전송
# 3. compare에서 받은 이미지 2개를 static 폴더에 잘 저장 !! 
# 4. aws.py안에 compare_faces 그 결과를 문자열로 "동일 인물일 확률은 15.24%"리턴
# 5. compare에서 리턴된 문자열을 받아서 웹 상에 출력(return)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/compare", methods=["POST"])
def compare():

    try:
        if request.method == "POST":
            f1 = request.files["file1"]
            f2 = request.files["file2"]
            filename1 = secure_filename(f1.filename)
            filename2 = secure_filename(f2.filename)

            f1.save("static/" + filename1)
            f2.save("static/" + filename2)

            r = compare_faces("static/" + filename1, "static/" + filename2)
            
            return r
            # POST

    except:
        return "얼굴 비교 실패"

    return ""





@app.route("/detect", methods=["POST"])
def detect():
    try:
        if request.method == "POST":
            f = request.files["file"]
            filename = secure_filename(f.filename)
            # 외부에서 온 이미지, 파일 등을 
            # 마음대로 저장할 수 없음
            # 서버에 클라이언트가 보낸 이미지를 저장!!
            
            f.save("static/" + filename)
            r = label("static/" + filename)
            return r          
    except:
        return "감지 실패"


#     return "객체 탐지"

@app.route("/mbti", methods=["POST"])
def mbti():
    try:
        if request.method == "POST":
            mbti = request.form["mbti"]

            return f"당신의 MBTI는 {mbti}입니다"


    except:
        return "데이터 수신 실패"



# html 폴더 내 exam04.html을
# templates 폴더로 복사
@app.route("/login", methods=["GET"])
def login():

    try:

        if request.method == "GET":
            # login_id, login_pw
            # get -> request.args
            login_id = request.args["login_id"]
            login_pw = request.args["login_pw"]





            # 로그인 성공 ->
            if (login_id == "park") and (login_pw == "1234"):
                # 로그인 성공 -> 로그인 성공 페이지로 이동
                # park님 환영합니다

                response = make_response(redirect("/login/success"))
                response.set_cookie("user", login_id)

                return response

            else:
                # 로그인 실패 -> / 경로로 다시 이동
            # 로그인 실패 ->
                return redirect("/")
            
            return f"{login_id}님 환영합니다"
    except:
        return "로그인 실패"
    

@app.route("/login/success", methods=["GET"])
def login_success():

    login_id = request.cookies.get("user")
    return f"{login_id}님 환영합니다"


if __name__ == "__main__":
    
    app.run(host="0.0.0.0")

# Ctrl + L 하면 터미널 클리어


