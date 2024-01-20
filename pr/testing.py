from flask import Flask, session, jsonify
import html

app = Flask(__name__)
app.secret_key = "ABCD"

@app.route("/")
def index():
    if "username" in session: 
        # 세션이 있는 경우
        return jsonify("You are {}".format(html.escape(session["username"])))
    else:
        # 세션이 없는 경우
        return jsonify("Who are you??")

@app.route('/set/<value>')
def set(value):
    # set url의 value를 username으로 등록
    print(value)
    session["username"] = value
    return jsonify("userName is {}".format(value))

@app.route('/clear')
def get():
    # 세션 삭제
    session.pop('username', None)
    return jsonify("Now No Session..")
if __name__ == '__main__':
    app.run(debug=True)
