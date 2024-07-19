from flask import Flask, render_template, request
import pickle, time, os
from flask_apscheduler import APScheduler

app = Flask(__name__)

global dictionary
dictionary = {}
file = open("dictionary_file.pkl", 'wb')
pickle.dump(dictionary, file)
file.close()

execute_clear_dictionary = APScheduler()

# Homepage
@app.route("/")
def crud_page():
    return render_template("/index.html")

# POST
@app.route("/post_elements")
def post_page():
    return render_template("/post.html")

@app.route("/success", methods=['POST'])
def success():
    file = open("dictionary_file.pkl", 'rb')
    dictionary = pickle.load(file)
    file.close()

    html_data_1 = request.form["entry1"]
    html_data_2 = request.form["entry2"]
    dictionary[html_data_1] = html_data_2

    file = open("dictionary_file.pkl", 'wb')
    pickle.dump(dictionary, file)
    file.close()
    time.sleep(1)

    return render_template("/success.html", html_data_1=html_data_1, html_data_2=html_data_2)


if __name__== '__main__':
    execute_clear_dictionary.add_job(id = 'Scheduled Task', func=clear_dictionary, trigger="interval", seconds=300)
    execute_clear_dictionary.start()
    app.run(host="0.0.0.0", debug=True, port=5000)