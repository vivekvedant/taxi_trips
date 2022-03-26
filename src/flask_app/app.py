from flask import Flask, render_template
import os
import pickle
import pandas as pd

template_dir =  os.path.join(os.path.dirname(os.path.abspath(__file__)),"templates")

static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),"static")


server = Flask(__name__,static_folder = static_dir,template_folder = template_dir)


@server.route("/",methods = ['GET'])
def index():
    # get the location zone name
    read_zone_pickle_file = pickle.load(open("../pickle_files/zone.pickle","rb"))
    return render_template("index.html",zone_list=read_zone_pickle_file)



