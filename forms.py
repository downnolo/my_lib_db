from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField, TextAreaField, FieldList, SelectField, RadioField, HiddenField
from wtforms.validators import DataRequired

character_dd_list  = [
    'Default',
    'Adam',
    'Eve',
    'Kain',
    'Abel'
]


relationship_dd_list = [
    'Default',
    'A/E',
    'K/S',
    'AB/S',
    'X/Y'
]

genre_dd_list = [
    'Default',
    'Angst',
    'Humor',
    'Fantasy',
    'Drama'
]

tag_dd_list = [
    'Default',
    'spring',
    'summer',
    'fall',
    'winter'
]

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class StoryInput(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author')
    words = IntegerField('Words')
    summary = TextAreaField('Summary') 
    characters = FieldList(SelectField('Characters', choices=character_dd_list), min_entries=3, max_entries=5)
    relationships = FieldList(SelectField('Relationships', choices=relationship_dd_list), min_entries=3, max_entries=5)
    genres = FieldList(SelectField('Genres', choices=genre_dd_list), min_entries=3, max_entries=5)
    tags = FieldList(SelectField('Tags', choices=tag_dd_list), min_entries=3, max_entries=5)
    serial = StringField('Serial')
    part = StringField('Part')
    status = BooleanField('Status')
    
    submit = SubmitField('Write to DB')



class StorySearch(FlaskForm):
    title = StringField('Title')
    author = StringField('Author')
    words = IntegerField('Words')
    more_less = RadioField('More_Less', choices=['less', 'more'])
    summary = TextAreaField('Summary')
    characters = FieldList(SelectField('Characters', choices=character_dd_list), min_entries=3, max_entries=5)
    relationships = FieldList(SelectField('Relationships', choices=relationship_dd_list), min_entries=3, max_entries=5)
    genres = FieldList(SelectField('Genres', choices=genre_dd_list), min_entries=3, max_entries=5)
    serial = StringField('Serial')
    serial_part = StringField('Part')
    tags = FieldList(SelectField('Tags', choices=tag_dd_list), min_entries=3, max_entries=5)
    status = BooleanField('Status')
    submit_search = SubmitField('Search to DB')

class OpenFileForm(FlaskForm):
    part = HiddenField()
    submit_open = SubmitField('Datei öffnen')