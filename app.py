import datetime
import os

from dotenv import load_dotenv
from flask import Flask, render_template, request
from pymongo import MongoClient

load_dotenv()

def create_app():
    app = Flask(__name__)
    client = MongoClient(os.getenv('MONGODB_URI'))
    app.db = client.microblog

    @app.route("/hello")
    def hello_world():
        return "<h1>Hello, World!</h1>"


    @app.route("/", methods=['GET', 'POST'])
    def home_page():
        if request.method == 'POST':
            entry_content = request.form.get('content')
            formatted_date = datetime.datetime.now().strftime("%Y-%m-%d")
            if entry_content!='':
                app.db.entries.insert_one({"content": entry_content, "date": formatted_date})

        entries_with_date = [
            (entry["content"],
            entry["date"],
            datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")) 
            for entry in app.db.entries.find({})
        ]
        return render_template('home.html', entries=entries_with_date)
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8000)