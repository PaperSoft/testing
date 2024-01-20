import profile
from flask import Flask, render_template, request, redirect, url_for, session, session
from flask_mysqldb import MySQL
import requests
import ssl
import html


print(ssl.OPENSSL_VERSION)

ngrokn = "15184"
app = Flask(__name__)
app.secret_key = 'wnsgmlwnsgmlwnsgml'

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1223'
app.config['MYSQL_DB'] = 'fire'

mysql = MySQL(app)

@app.route('/')
def index():
    # Fetch data from the database

    if "user" in session:
        user_session = str(html.escape(session["user"]))

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT socksenbled FROM user WHERE email = %s', (user_session,))
        
        # Initialize socks before the if block
        socks = "no"

        # Check if the result is not empty
        socksenbled = cursor.fetchone()
        if socksenbled and socksenbled[0]:
            socks = "yes"
        else:
            socks = ''

        return render_template('index.html', data=user_session, socksdata=socks)

    else:
        user_session = ""
        return render_template('index.html', data=user_session)
        

    

@app.route('/create')
def create():
    email = str(html.escape(session["user"]))
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE user SET socksenbled = %s WHERE email = %s', ('hi', email))
    mysql.connection.commit()
    cursor.close()

    return render_template('re.html')
# @app.route('/d_t')
# def test():
#     cur = mysql.connection.cursor()
#     cur.execute('INSERT INTO user(password, email) VALUES (%s, %s)', ("ㅎㅇ", "ddd@dddd.dd"))
#     mysql.connection.commit()
#     cur.close()
#     return render_template('index.html')

# @app.route('/d_c')
# def check():
#     cursor = mysql.connection.cursor()
#     cursor.execute('SELECT * FROM user WHERE email = %s AND password = %s', ("ddd@dddd.dd", "ㅎㅇ"))
#         # 값이 유무 확인 결과값 account 변수로 넣기
#     account = cursor.fetchone()

#     if account:
#         print("dd")

#     return render_template('index.html')


@app.route("/login_naver") 
def NaverLogin():
    client_id = "SCgf7HY5hCD12ugwIAGR"
    redirect_uri = "http://0.tcp.jp.ngrok.io:"+ngrokn+"/callback"
    url = f"https://nid.naver.com/oauth2.0/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    return redirect(url)

@app.route("/login_kakao")
def KakaoLogin():
    return render_template('re.html')
    
@app.route("/login")
def LoginPage():
    return render_template('login.html')

@app.route("/callback")
def callback():
    params = request.args.to_dict()
    code = params.get("code")

    client_id = "SCgf7HY5hCD12ugwIAGR"
    client_secret = "gdSkZw6wur"

    token_request = requests.get(f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}")
    token_json = token_request.json()
    print(token_json)

    access_token = token_json.get("access_token")
    profile_request = requests.get("https://openapi.naver.com/v1/nid/me", headers={"Authorization": f"Bearer {access_token}"})
    profile_data = profile_request.json()

    email = profile_data.get("response").get("email")
    name = profile_data.get("response").get("name")
    phone = profile_data.get("response").get("mobile")



    print("USER DATA RAW::"+str(profile_data))

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
        # 값이 유무 확인 결과값 account 변수로 넣기
    account = cursor.fetchone()

    if account:
        # 계정 있음
        print("!log 계정 발견, 네이버 로그인::"+email)

        session["user"] = email

    else:
        # 계정 없음
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO user(phone, email, name) VALUES (%s, %s, %s)', (phone, email, name))
        mysql.connection.commit()
        cur.close()
        print("!log 계정 없어 생성함::"+email)

        session["user"] = email


    return render_template('re.html')

@app.route('/logout')
def get():
    # 세션 삭제
    session.pop('user', None)
    return render_template('re.html')
if __name__ == '__main__':
    app.run(debug=True)
