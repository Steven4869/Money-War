from flask import Flask,render_template,request,redirect,session
import mysql.connector
import os
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    port='3306',
    database='login'
)
cursor = conn.cursor()
app = Flask(__name__)
app.secret_key=os.urandom(24)
@app.route('/')
def home():
    return render_template('login.html')
@app.route('/create')
def create():
    return render_template('create.html')
@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/products')
def products():
    cursor.execute("""SELECT * FROM `posts`""")
    items = cursor.fetchall()
    return render_template('products.html', items=items)
@app.route('/profile')
def profile():
    if 'user_id' in session:
        cursor.execute("""SELECT * FROM `data` WHERE id = '%s'""", (session['user_id']))
        profiles = cursor.fetchone()
        return render_template('profile.html', profiles=profiles)
    return redirect('/')
@app.route('/home')
def dashboard():
    cursor.execute("""SELECT * FROM `posts`""")
    data = cursor.fetchall()
    if 'user_id' in session:
        return render_template('index.html', data= data)
    else:
        return redirect('/')
@app.route('/edit')
def edit():
    return render_template('edit.html')
@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name')
    price = request.form.get('price')
    description = request.form.get('description')
    conditions = request.form.get('conditions')
    image = request.form.get('image')
    cursor.execute("""INSERT INTO `posts` (`name`, `price`, `image`,`conditions`,`description`) VALUES ('{}','{}','{}','{}','{}')""".format(name,price,image,conditions,description))
    conn.commit()
    return redirect('/home')

@app.route('/add_user',methods=['POST'])
def add_user():
    name= request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')
    cursor.execute("""INSERT INTO `data` (`name`,`username`,`password`) VALUES ('{}','{}','{}')""".format(name,username,password))
    conn.commit()
    return "User registered successfully"
@app.route('/login_validation', methods=['POST'])
def login_validation():
    username = request.form.get('username')
    password = request.form.get('password')
    cursor.execute("""SELECT * FROM `data` WHERE `username` LIKE '{}' AND `password` LIKE '{}'""".format(username,password))
    users = cursor.fetchall()
    if len(users)>0:
        session['user_id'] = users[0][0]
        return redirect('/home')
    else:
        return redirect('/')
@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')
if __name__ == "__main__":
    app.run(debug=True)
