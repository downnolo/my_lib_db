import psycopg2
import psycopg2.extras
from flask import Flask, render_template, request, redirect, url_for, session
from forms import StoryInput, StorySearch, OpenFileForm, UpdateSearch, UpdateSearchDD, EditForm
from query import create_query
import os
from flask import flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'

def db_conn():
    conn = psycopg2.connect(database="lib_db", host="localhost", user="postgres", password="admin")
    return conn

# @app.route('/')
# def index():
#    #conn = psycopg2.connect("postgresql://postgres:admin@localhost:5432/lib_db")
#    return render_template('index.html')


def clean_up_select_field(data):
   data = set(data)
   data.discard(None)
   data.discard('Default') 

   return list(data)


def update_entry(plus, minus, base):
   new_entry = []

   if not base:
      new_entry = new_entry + plus
   else:
      new_entry = base + plus

   new_entry = [e for e in new_entry if e not in minus]
   
   return list(set(new_entry))



@app.route('/', methods=['GET', 'POST'])
def index():
   return render_template('index.html')


@app.route('/input', methods=['GET', 'POST'])
def input():
   input_dict = {}
   form=StoryInput()
   input_dict['title']=form.title.data
   if form.author.data:
      input_dict['author']=form.author.data
   if form.words.data:
      input_dict['words'] = form.words.data
   if form.summary.data:
      input_dict['summary'] = form.summary.data
   if form.characters.data:
      clean_up_select_field(form.characters.data)
      input_dict['characters'] = clean_up_select_field(form.characters.data)
   if form.relationships.data:
      input_dict['relationships'] = clean_up_select_field(form.relationships.data)
   if form.genres.data:
      input_dict['genres'] = clean_up_select_field(form.genres.data)
   if form.tags.data:
      input_dict['tags'] = clean_up_select_field(form.tags.data)
   if form.serial.data:
      input_dict['serial'] = form.serial.data
   if form.part.data:
      input_dict['part'] = form.part.data
   if form.status.data:
      input_dict['status'] = form.status.data

   dels = [k for k,v in input_dict.items() if v == []]
   for d in dels:
      del input_dict[d]

   columns = ', '.join(list(input_dict.keys()))
   values = ', '.join(['%({})s'.format(v) for v in list(input_dict.keys())])

   if form.validate_on_submit():
      print('yeah')
      conn = db_conn()
      cur = conn.cursor()
      cur.execute('INSERT INTO story ({0}) values ({1})'.format(columns, values), (input_dict))
      conn.commit()
      cur.close()
      conn.close()
   else:
      print('No')
   print(form.errors)
   return render_template('input.html', form=form)

@app.route('/search', methods=['GET', 'POST'])
def search():
   search_form = StorySearch()
   open_file_form = OpenFileForm()
   results = []
   session['results'] = []
   headers = ['main_id', 'title', 'author', 'words', 'status', 'summary', 'characters', 'relationships', 'genres', 'tags', 'serial', 'part']
   headers = headers[:5] + headers[-2:]
   header_details = headers[5:10]
   if request.method == 'POST':
      if search_form.submit_search.data and search_form.is_submitted():
         query = create_query(search_form)
         conn2 = db_conn()
         dict_cur = conn2.cursor(cursor_factory=psycopg2.extras.DictCursor)
         dict_cur.execute(query)
         db_results = dict_cur.fetchall()
         for r in db_results:
            entry = {
               'main_id': r[0],
               'title': r[1],
               'author': r[2],
               'words': r[3],
               'status': r[4],
               'summary': r[5],
               'characters': r[6],
               'relationships': r[7],
               'genres': r[7],
               'tags': r[9],
               'serial': r[10],
               'part': r[11]
            }

            session['results'].append(entry)
         
         results = session.get('results') if session.get('results') else results

      # elif open_file_form.submit_open.data:
      #    print('open_file_form.submit_open.data')
      # #    print(f"submit_open: {open_file_form.submit_open.data}")
      # # #    flash(f"part: {open_file_form.part.data}")

      # elif open_file_form.validate_on_submit():
      #    print('open_file_form.validate_on_submit()') 
         
      elif open_file_form.submit_open and open_file_form.validate_on_submit():
         print('ta')
         base_path = "C:\\Users\\Yvonne\\Desktop"
         part = open_file_form.data.get('part')
         full_path = os.path.join(base_path, f"{part}")
         print(full_path)
         try:
               os.startfile(full_path)
               print(f'Datei erfolgreich geöffnet: {full_path}')
         except Exception as e:
               print(f'Fehler beim Öffnen der Datei: {str(e)}') 
      #print('open_file_form.part:' + str(open_file_form.part))

   return render_template('search.html', search_form=search_form, open_file_form=open_file_form, results=results, headers=headers)



@app.route('/details/<int:entry_id>')
def details(entry_id):
   results = []
   entries = session.get('results') if session.get('results') else results
   entry = next((item for item in entries if item['main_id'] == entry_id), None)
   if entry:
        return render_template('details.html', entry=entry) 
   else:
      return "-nichts gefunden 404"


def get_entry_by_id(main_id):
   query = f'''SELECT * from story where main_id = '{main_id}' '''
   conn3 = db_conn()
   dict_cur = conn3.cursor(cursor_factory=psycopg2.extras.DictCursor)
   dict_cur.execute(query)
   results = dict_cur.fetchone()   
   return results

@app.route('/search3', methods=['GET', 'POST'])
def search3():
    form = EditForm()
    if request.method == 'POST':
        main_id = form.main_id.data
        entry = get_entry_by_id(main_id)
        if entry:
            return redirect(url_for('edit_entry', main_id=main_id, entry=entry))
        else:
            flash('No entry found with the given Main ID.')
    return render_template('search3.html', form=form)


@app.route('/edit/<main_id>', methods=['GET', 'POST'])
def edit_entry(main_id):
    form = EditForm()
    entry = get_entry_by_id(main_id)
    
    if not entry:
        flash('Entry not found.')
        return redirect(url_for('search'))

    if request.method == 'POST':
      # Aktualisieren Sie den Eintrag in der Datenbank
      updated_entry = {
         'main_id': main_id,
         'title': form.title.data,
         'author': form.author.data,
         'words': form.words.data,
         'summary': form.summary.data,
         'characters' : update_entry(form.chars_add.data, form.chars_del.data, entry['characters']),
         'relationships' : update_entry(form.rels_add.data, form.rels_del.data, entry['relationships']),
         'genres' : update_entry(form.genres_add.data, form.genres_del.data, entry['genres']),
         'tags' : update_entry(form.tags_add.data, form.tags_del.data, entry['tags'])
        }
      print(entry)
      print(updated_entry)

      columns = ', '.join(list(updated_entry.keys()))
      values = ', '.join(['%({})s'.format(v) for v in list(updated_entry.keys())])



      #update_entry_in_database(updated_entry)  # Implementieren Sie diese Funktion
      flash('Entry updated successfully!')


    return render_template('edit.html', form=form, entry=entry)



# @app.route('/updates', methods=['GET', 'POST'])
# def get_title():
#    results = []
#    update_form = UpdateSearch()
#    # updated_dd = UpdateSearchDD()
#    if request.method == 'POST':
#       main_id = update_form.main_id.data
#       query = f'''SELECT * from story where main_id = '{main_id}' '''
#       conn3 = db_conn()
#       dict_cur = conn3.cursor(cursor_factory=psycopg2.extras.DictCursor)
#       dict_cur.execute(query)
#       results = dict_cur.fetchone()
#       x = change_dd(results['characters'])
      
#    # if request.method == 'GET':
#    #    print('yes')
#    #    if results:
#    #       print('r')
#    #       x = change_dd(results['characters'])
#    #       print(x)
#    #       print(updated_dd.characters.data)

#    return render_template('updates.html', update_form=update_form, results=results)


