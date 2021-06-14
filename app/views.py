from flask import render_template,request
from flask import redirect,url_for
from app.utils import pipeline
from PIL import Image
import os

UPLOAD_FOLDER='static/uploads'

def base():
    return render_template('base.html')
def predictor():
    return render_template('face.html')
def tech():
    return render_template('tech.html')
def getwidth(path):
    img=Image.open(path)
    size=img.size
    aspect=size[0]/size[1]
    w=300*aspect
    return int(w)    
def gender():
    if request.method=='POST':
        f=request.files['image']
        filename=f.filename
        path=os.path.join(UPLOAD_FOLDER,filename)
        f.save(path)
        w=getwidth(path)
        img=pipeline(path,filename,color='bgr')
        return render_template('gender.html',fileupload=True,img_name=filename,w=w)
    return render_template('gender.html',fileupload=False,img_name="flask.png",w="300")
