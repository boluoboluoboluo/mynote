from flask import Flask, flash, redirect, render_template, request, url_for
app = Flask(__name__)
app.secret_key = 'random string'


#Flask 提供了一个非常简单的方法来使用闪现系统向用户反馈信息。闪现系统使得在一个请求结束的时候记录一个信息，
# 并且在下次（且仅在下一次中）请求时访问它，这通常与布局模板结合使用以公开信息。

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid username or password. Please try again!'
        else:
            flash('You were successfully logged in')	#消息闪现
            return redirect(url_for('index'))

    return render_template('login.html', error = error)


if __name__ == '__main__':
    app.run(debug=True)