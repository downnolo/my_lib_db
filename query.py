

def prep_dd(field, data):
    query_part = None
    data = set(data)
    if 'Default' in data:
        data.remove('Default')
    if data:
        dd = '{' + ', '.join([f'"{d}"' for d in data]) + '}'
        #query_part = f'{field} @> {dd}'
        query_part = f" @> '{dd}'"
    return query_part


def create_query(form):
    query = {}
    # print('query')
    # query = '''SELECT main_id from story where characters @> '{"Adam", "Kain"}' '''
    # query = f'''SELECT title from story where title like '%{t}%' '''
    #characters = f"characters @> '{"Adam", "Kain"}' "
    base = 'SELECT * from story where'

    if form.more_less.data:
        if form.more_less.data == 'less':
            ml = '<' 
        elif form.more_less.data == 'more':
            ml = '>'
    else:
         ml = '>'

    if form.title.data:
        query['title'] =  f" like '%{form.title.data}%'"
    if form.author.data:
        query['author'] =  f" like '%{form.author.data}%'"
    if form.summary.data:
        query['summary'] =  f" like '%{form.summary.data}%'"
    if form.words.data:
        query['words'] = f" {ml} {form.words.data}"
    if form.serial.data:
        query['serial'] = f" like '%{form.serial.data}%'"
    
    
    query['characters'] = prep_dd('characters', form.characters.data)
    query['relationships'] = prep_dd('relationships', form.relationships.data)
    query['genres'] = prep_dd('genres', form.genres.data)
    query['tags'] = prep_dd('tags', form.tags.data)
    query['status'] = f'is {form.status.data}'
    
    q = ''
    for k,v in query.items():
        if v is not None:
            q = f'{q} and {k} {v}'

    q = q.replace(' and', '', 1)
    query = f'{base} {q}'

    return query
