from flask import Flask ,render_template , request ,session
from flask_mysqldb import MySQL
import MySQLdb.cursors 
import re

app = Flask(__name__)

app.secret_key = 'cf94fc35564f5dc7a231b2d7'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'vargees06@'
app.config['MYSQL_DB'] = 'Office'
mysql = MySQL(app)

@app.route("/", methods =['POST','GET'])
@app.route("/register", methods =['POST','GET'])
def register():
    errormsg = ''
    if request.method == 'POST' and 'Username' in request.form and 'EmailAddress' in request.form and 'Passcode' in request.form and 'Phone' in request.form :
        Username = request.form['Username']
        EmailAddress = request.form['EmailAddress']
        Passcode = request.form['Passcode']
        Phone = request.form['Phone']
        print(Username,Phone,EmailAddress,Passcode)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employee WHERE Username = % s',  (Username, ))
        account = cursor.fetchone()
        if account:
            errormsg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', EmailAddress):
            errormsg = 'Invalid EmailAddress !'
        elif not re.match(r'[A-Za-z]+', Username):
            errormsg = 'Username must contain only characters !'
        elif not re.match(r'[0-9]',Phone):
            errormsg = 'Enter your Phone number !'
        elif not re.match(r'[a-z]',Passcode):
            errormsg = 'Enter your Passcode !'
        else:
            cursor.execute('INSERT INTO employee VALUES (NULL,% s, % s, % s,% s)', (Username,EmailAddress,Passcode,Phone,))
            mysql.connection.commit()
            errormsg = 'You have successfully registered !'
    elif request.method == 'POST':
        errormsg = 'Please fill out the form !'
    return render_template('index.html', errormsg = errormsg)



@app.route("/login",methods =['POST','GET'])
def login():
    errormsg = ''
    if request.method == 'POST' and 'Username' in request.form and 'Passcode' in request.form:
        Username = request.form['Username']
        Passcode = request.form['Passcode']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employee WHERE Username = % s AND Passcode = % s', (Username, Passcode, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['Username'] = account['Username']
            session['Passcode'] = account['Passcode']
            errormsg = 'Logged in successfully !'
            return render_template('index.html', errormsg = errormsg)
        else:
            errormsg = 'Incorrect Username / Passcode !'
    return render_template("login.html",errormsg=errormsg)

if __name__ =="__main__":
    app.run(debug=True)


