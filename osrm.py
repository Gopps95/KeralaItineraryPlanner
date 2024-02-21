from flask import Flask, redirect,render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from geopy.geocoders import Nominatim

app = Flask(__name__)

app.config['SECRET_KEY'] = '16bb6643d81184bf9376c955ef359510'

geolocator = Nominatim(user_agent="app")

class OSRM(FlaskForm):
    start_point = StringField('Start Point', validators=[DataRequired()])
    end_point = StringField('End Point', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/", methods= ['GET','POST'])
def home():
     form = OSRM()
     if form.validate_on_submit():
        start_location = geolocator.geocode(form.start_point.data)
        end_location = geolocator.geocode(form.end_point.data)
        start =str(start_location.latitude) +"," +str(start_location.longitude)
        end =str(end_location.latitude) +"," +str(end_location.longitude)
        coordinate= start + ";" +end
        return redirect(f"http://router.project-osrm.org/route/v1/car/{coordinate}?overview=false")
     return render_template("home.html", form=form)


if __name__ =="__main__":
    app.run(debug=True)

#13.388860,52.517037;13.397634,52.529407