from flask import Flask, render_template
import os

template_dir =  os.path.join(os.path.dirname(os.path.abspath(__file__)),"templates")

static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),"static")


server = Flask(__name__,static_folder = static_dir,template_folder = template_dir)


@server.route("/",methods = ['GET'])
def index():
    return render_template("index.html")



