from flask import Flask, render_template, request, jsonify
import test_module
import query_on_whoosh

#from this file (app.py) into a web page

app = Flask(__name__)
#app.config.update(dict/JSONIFY_PRETTYPRINT_REGULAR=True)

@app.route("/")
def handle_slash():
    requested_name = request.args.get("user_name")
    return render_template("index.html", user_name=requested_name)
    
@app.route("/test", strict_slashes=False)
def handle_test():
    input = "ac"
    return test_module.test(input) 

@app.route("/query", strict_slashes=False)
def handle_paging_query():
    query_term = request.args.get("q")
    query_page = int(request.args.get("p"))
    return jsonify({"query_term": query_term, "search_results": query_on_whoosh.query(query_term, 10, query_page)})
    
