from flask import Flask, render_template, request, jsonify
import test_module
import query_on_whoosh
import smtplib
import math
import config
#from this file (app.py) into a web page

app = Flask(__name__)
#app.config.update(dict/JSONIFY_PRETTYPRINT_REGULAR=True)

@app.route("/")
def handle_slash():
    requested_name = request.args.get("user_name")
    return render_template("index.html", user_name=requested_name)

@app.route("/query", strict_slashes=False)
def handle_query():
    query_term = request.args.get("q")
    page_index = int(request.args.get("p"))
    return jsonify({"query_term": query_term, "search_results": query_on_whoosh.query(query_term, 10, page_index)})
    
@app.route("/query_view", strict_slashes=False)
def handle_query_view():
    query_term = request.args.get("q")
    if not query_term:  
        query_term = ""
    
    page_index_arg = request.args.get("p")
    if not page_index_arg:
        page_index_arg = "1"

    page_index = int(page_index_arg)
    query_results = query_on_whoosh.query(query_term, current_page=page_index)
    search_results = query_results[0]
    results_cnt = int(query_results[1])
    page_cnt = math.ceil(results_cnt / 10)
    return render_template("query.html", results = search_results, 
                            page_cnt=page_cnt, query_term=query_term)

@app.route("/about", strict_slashes=False)
def handle_about():
    return render_template("about.html")

@app.route("/success", strict_slashes=False)
def handle_request():
    new_data = request.args.get("new_data")
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login("fmartin7@emich.edu", config.gmail_password)
    #message = "Subject: {}\n\n{}".format("Request to add new data", "request to add: " + topic)
    server.sendmail("fmartin7@emich.edu", "fmartin7@emich.edu", "request " + new_data)
    return render_template("success.html", new_data=new_data)