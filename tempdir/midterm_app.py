from flask import Flask, render_template, request,redirect,url_for

app = Flask(__name__)
@app.route('/',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('login'))

    return render_template("login.html")

@app.route('/registration',methods=['GET','POST'])
def registration():
    if request.method == 'POST':
        return redirect(url_for('registration'))

    return render_template("registration.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000, debug=True)