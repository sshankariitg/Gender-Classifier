import numpy as np
import pandas as pd
import sklearn
import pickle
import cv2


#Load all models
haar=cv2.CascadeClassifier('./model/haarcascade_frontalface_default.xml')
#pickel files
pca_model=pickle.load(open('./model/p_50.pickle','rb'))
mean=pickle.load(open('./model/preprocessing_mean.pickle','rb'))
svm_model=pickle.load(open('./model/svm_best_model.pickle','rb'))

font=cv2.FONT_HERSHEY_SIMPLEX
predict_gender=['Male','Female']

#Pipeline model
def pipeline(path,filename,color='bgr'):
            #convert to grayscale
            img=cv2.imread(path)
            if color=='bgr':
                gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            else:
                gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
            #CROP FACE USING HAAR CASCADE CLASSIFIER
            face=haar.detectMultiScale(gray,1.5,3)
            for x,y,w,h in face:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
                cropping=gray[y:y+h,x:x+w]
                #normalization
                cropping=cropping/255.0
                #resize image (100,100)
                if cropping.shape[1]>=100:
                    cropping_resize=cv2.resize(cropping,(100,100),cv2.INTER_AREA)
                else:
                    cropping_resize=cv2.resize(cropping,(100,100),cv2.INTER_CUBIC)
                #flattening (1x10000)
                cropping_reshape=cropping_resize.reshape(1,10000)
                #subtract with mean
                cropping_mean=cropping_reshape-mean
                #get eigen image from pca model
                eigen_img=pca_model.transform(cropping_mean)
                #pass img to svm model
                result=svm_model.predict_proba(eigen_img)[0]
                predict=result.argmax() #0 or 1
                score=result[predict]
                text="%s : %0.2f"%(predict_gender[predict],score)
                cv2.putText(img,text,(x,y),font,1,(0,255,0),2)
            cv2.imwrite('./static/predict/{}'.format(filename),img)    
            return img

