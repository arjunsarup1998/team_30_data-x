from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.html5 import DateField, DateTimeLocalField, TimeField
from wtforms.validators import DataRequired, Required
from datetime import datetime

class InstagramHandleHome(FlaskForm):
	handle = StringField('demo_name', validators = [DataRequired()])
	submit = SubmitField('Submit')


class InstagramHandleFormGeneric(FlaskForm):
	ImageLink = StringField('demo_name', validators = [DataRequired()])
	#day = SelectField('Choose Day of Week', choices=[(-1,"Choose Day of Week"),(0,'Monday'),(1,'Tuesday'),(2,'Wednesday'),(3,'Thursday'),(4,'Friday'),(5,'Saturday'),(6,'Sunday')])
	#date = DateTimeLocalField('When do you want to make the post?', format="%Y-%m-%dT%H:%M:%S", default=datetime.today, validators=[Required()])
	dt = DateField('DatePicker')
	tt = TimeField('TimePicker')
	submit2 = SubmitField('Submit')
