from flask import Flask, render_template, request, jsonify
import test_module
import query_on_whoosh
import smtplib
import math
import config
import sqlite3
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

    if query_term != "":
        #connecting to sqlite database
        conn = sqlite3.connect('history.db')
        c = conn.cursor()
        #c.execute(f"INSERT INTO search_terms (id, term, search_time) VALUES (1, '{query_term}', strftime('%s', 'now'));");
        # bryant', strftime('%s', 'now'));delete from search_terms;insert into search_terms(id, term, search_time) values (1, 'garbage
        c.execute("SELECT enable_history FROM history_settings WHERE id=1;")
        status= c.fetchone()
        if status[0]=="on":
            c.execute(f"INSERT INTO search_terms (term, search_time) VALUES (?, datetime(strftime('%s', 'now'), 'unixepoch', 'localtime', '-5 hours'));", (query_term,))
        c.execute("SELECT * FROM search_terms;")
        rows = c.fetchall()
        conn.commit()
        conn.close()

        page_index = int(page_index_arg)
        query_results = query_on_whoosh.query(query_term, current_page=page_index)
        search_results = query_results[0]
        results_cnt = int(query_results[1])
        page_cnt = math.ceil(results_cnt / 10)
        return render_template("query.html", results = search_results, 
                                page_cnt=page_cnt, current_page=page_index,
                                query_term=query_term,
                                history_list=rows)
    else:
        
        return render_template("query.html", page_cnt=0)

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

@app.route("/history", strict_slashes=False)
def handle_history():
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute("SELECT * FROM search_terms ORDER BY search_time DESC;")
    rows = c.fetchall()
    conn.commit()
    conn.close() 
    return render_template("history.html", history_list=rows)

@app.route("/remove_history", strict_slashes=False)
def handle_remove_history():
    query_id = request.args.get("id")

    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute("SELECT * FROM search_terms;")
    rows = c.fetchall()
    c.execute("DELETE FROM search_terms WHERE id=?;", (query_id,))
    conn.commit()
    conn.close()

    return render_template("remove_history.html", history_list=rows, id=query_id)

@app.route("/settings", strict_slashes=False)
def handle_settings():
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute("SELECT * FROM history_settings;") 
    rows = c.fetchall()
    conn.commit()
    conn.close()


    return render_template("settings.html", status=rows)

@app.route("/save_settings", strict_slashes=False)
def handle_save_settings():
    status = request.args.get("enable")
    if status != "on":
        status = "off"
    
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute("UPDATE history_settings SET enable_history=? WHERE id=1;", (status,))
    rows = c.fetchall()
    conn.commit()
    conn.close()
    return render_template("save_settings.html", status=status)

