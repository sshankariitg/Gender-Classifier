from flask import Flask
from app import views
app = Flask(__name__)


#url
app.add_url_rule('/','base',views.base)
app.add_url_rule('/predictor','predictor',views.predictor)
app.add_url_rule('/Technologies','tech',views.tech)
app.add_url_rule('/predictor/gender','gender',views.gender,methods=['GET','POST'])
#run
if __name__ == '__main__':
    app.run(debug=True)