from flask_wtf import FlaskForm
from wtforms import StringField, FloatField,SelectField
from wtforms.validators import InputRequired,Optional


class AddCupcake(FlaskForm):
    """Form for adding cupcake."""

    flavor = StringField("Flavor",validators=[InputRequired()])
    size = SelectField("Size", choices=[("", "-- --"),("small", "Small"), ("medium", "Medium"), ("large", "Large")],validators=[InputRequired()])
    rating = FloatField("Rating",validators=[InputRequired()])
    image = StringField("Cupcake URL",validators=[Optional()])
  