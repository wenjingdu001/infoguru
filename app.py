from flask import Flask, request, render_template, Markup
from query_data import query_rag
import jinja2


app = Flask(__name__)

# Custom filter to convert newlines to <br> tags
def nl2br(value):
    return Markup(value.replace("\n", "<br>\n"))

# Register the custom filter
app.jinja_env.filters['nl2br'] = nl2br

@app.route('/', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        query_text = request.form['query']
        if query_text:
            try:
                response = query_rag(query_text)
                return render_template('index.html', query=query_text, response=response)
            except Exception as e:
                return render_template('index.html', error=f"An error occurred: {e}")
        else:
            return render_template('index.html', error="Please enter a query")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
