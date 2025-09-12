from flask import Flask, render_template, request, send_file, session , url_for, redirect

from flask_bootstrap import Bootstrap

import numpy as np
import tensorflow as tf

app = Flask(__name__)
app.secret_key = "afskj988fdhafh893hkajsfjkhsf"
Bootstrap(app)


@app.route('/', methods = ["GET", "POST"])
def index():
    return render_template('index.html')

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port = port, debug = True)