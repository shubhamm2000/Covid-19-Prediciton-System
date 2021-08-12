from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import pickle
from datetime import datetime

app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "root"
app.config['MYSQL_DB'] = "covid19"

mysql = MySQL(app)

#open a file where you want to store the data
file = open('model.pkl','rb')
lr = pickle.load(file)
file.close()

@app.route('/', methods=["GET","POST"])
def hello_world():
    if request.method =="POST":
        myDict = request.form
        name = str(myDict['name'])
        fever = int(myDict['fever'])
        age = int(myDict['age'])
        pain = int(myDict['pain'])
        runnynose = int(myDict['runnynose'])
        diffbreath = int(myDict['diffbreath'])
        # Code for inference
        ip = [fever, pain, age, runnynose, diffbreath]
        infecprob = lr.predict_proba([ip])[0][1]
        print(infecprob)
        finalvalue = round(infecprob*100)

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (Name,Age,Time,Covid_percentage) VALUES (%s,%s,%s,%s)",(name,age,current_time,finalvalue))


        mysql.connection.commit()
        cur.close()

    # return 'Hello World!' + str(infecprob)
        return render_template("show.html",inf=round(infecprob*100))
        

    return render_template("index.html")

@app.route('/database')
def table():
    cur = mysql.connection.cursor()
    cur.execute("Select * from users order by Covid_percentage DESC, Age DESC,Name DESC, Time DESC;")
    data = cur.fetchall()
    cur.close()
    return render_template('table.html', users = data)


if __name__ == "__main__":
    app.run(debug=True)