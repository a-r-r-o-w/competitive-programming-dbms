import streamlit as st
import mysql.connector.cursor
import random
import time

import config
import queries

is_data_generated = False
data = {}

def create (cursor: mysql.connector.cursor.MySQLCursor) -> None:
  global is_data_generated, data

  with st.expander('Initialize With Random Data'):
    initialize_col1, initialize_col2 = st.columns(2)
    items = list(config.SQL_TABLE_DEMO_SIZE.items())
    mid = (len(items) + 1) // 2

    with initialize_col1:
      for key, value in items[: mid]:
        config.SQL_TABLE_DEMO_SIZE[key] = st.number_input(
          label = key[0].upper() + key[1:],
          min_value = 1,
          value = value,
          key = f'{key}_create_count'
        )
    
    with initialize_col2:
      for key, value in items[mid: ]:
        config.SQL_TABLE_DEMO_SIZE[key] = st.number_input(
          label = key[0].upper() + key[1:],
          min_value = 1,
          value = value,
          key = f'{key}_create_count'
        )
    
    if st.button('Generate Random Data'):
      is_data_generated = True
      data = generate_random_data()
      st.info('Random Data generated')
    
    if st.button('View Data'):
      st.write(data)

  st.write('Select table')
  table_selection = st.selectbox('Table', config.SQL_TABLENAMES)
  col1, col2 = st.columns(2)
  values = {}
  table_attribute_count = len(config.SQL_TABLE_ATTRIBUTES[table_selection].keys())
  mid = (table_attribute_count + 1) // 2

  with col1:
    for attribute, props in list(config.SQL_TABLE_ATTRIBUTES[table_selection].items())[: mid]:
      attribute: str
      props: dict
      values[attribute] = props.get('type')(props.get('function')(**props.get('params')))
  
  with col2:
    for attribute, props in list(config.SQL_TABLE_ATTRIBUTES[table_selection].items())[mid :]:
      attribute: str
      props: dict
      values[attribute] = props.get('type')(props.get('function')(**props.get('params')))
  
  with st.expander('See query'):
    st.code(queries.insert(table_selection, values))
  
  if st.button(label = f'Add {table_selection}', key = 'add_table_selection'):
    cursor.execute(queries.use_database(config.SQL_DBNAME))
    cursor.execute(queries.insert(table_selection, values))
    st.info(f'Data inserted into table {table_selection} succesfully')

def generate_random_data () -> dict:
  filename_list = ['country', 'firstname', 'institute', 'lastname', 'password', 'problem', 'tag', 'text']
  wordlist = {}

  for filename in filename_list:
    with open('data/' + filename + '.txt', 'r') as file:
      wordlist[filename] = [line.strip().lower() for line in file.readlines()]

  data = {}

  data['country'] = random.sample(wordlist.get('country'), config.SQL_TABLE_DEMO_SIZE.get('user'))
  data['firstname'] = random.sample(wordlist.get('firstname'), config.SQL_TABLE_DEMO_SIZE.get('user'))
  data['institute'] = random.sample(wordlist.get('institute'), config.SQL_TABLE_DEMO_SIZE.get('user') // 5)
  data['lastname'] = random.sample(wordlist.get('lastname'), config.SQL_TABLE_DEMO_SIZE.get('user'))
  data['password'] = random.sample(wordlist.get('password'), config.SQL_TABLE_DEMO_SIZE.get('user'))
  data['problem'] = random.sample(wordlist.get('problem'), config.SQL_TABLE_DEMO_SIZE.get('problem'))
  data['tag'] = random.sample(wordlist.get('tag'), config.SQL_TABLE_DEMO_SIZE.get('tag'))
  data['text'] = wordlist.get('text')[0].split()
  data['domains'] = ['gmail.com', 'hotmail.com', 'yahoo.com', 'protonmail.com', 'yandex.ru', 'outlook.com', 'mac.com']

  table_data = {}

  table_data['user'] = [
    {
      'user_id': index,
      'username': data.get('firstname')[index][0].upper() + data.get('lastname')[index],
      'password': data.get('password')[index],
      'email': data.get('firstname')[index] + '.' + data.get('lastname')[index] + '@' + random.choice(data['domains']),
      'name': data.get('firstname')[index][0].upper() + data.get('firstname')[index][1:] + ' ' + data.get('lastname')[index][0].upper() + data.get('lastname')[index][1:],
      'rating': random.randint(0, 4000),
      'contribution': random.randint(0, 200),
      'institute': random.choice(data['institute']) if random.uniform(0, 1) > 0.2 else '',
      'country': random.choice(data['country']),
      'last_online': int(time.time()) - random.randint(0, 100000000)
    }
    for index in range(config.SQL_TABLE_DEMO_SIZE.get('user'))
  ]

  table_data['contest'] = [
    {
      'contest_id': index,
      'name': f'Contest {index + 1}',
      'type': random.choices(
                population = ['Normal', 'IOI', 'ICPC'],
                weights = [90, 5, 5],
                k = 1
              ),
      'duration': random.choices(
                    population = [60, 90, 120, 135, 150, 165, 180],
                    weights = [5, 5, 50, 10, 10, 5, 15]
                  ),
      'start_time': int(time.time()) - random.randint(0, 100000000)
    }
    for index in range(config.SQL_TABLE_DEMO_SIZE.get('contest'))
  ]

  table_data['blog'] = [
    {
      'blog_id': index,
      'title': ' '.join(random.choice(data['text']) for _ in range(random.randint(2, 20))),
      'content': ' '.join(random.choice(data['text']) for _ in range(random.randint(20, 100))),
      'upvote_count': random.randint(0, 500),
      'downvote_count': random.randint(0, 100),
      'user_id': random.choice(range(config.SQL_TABLE_DEMO_SIZE.get('user'))),
      'time': int(time.time()) - random.randint(0, 100000000)
    }
    for index in range(config.SQL_TABLE_DEMO_SIZE.get('blog'))
  ]

  table_data['tag'] = [
    {
      'tag_id': index,
      'name': data['tag'][index]
    }
    for index in range(config.SQL_TABLE_DEMO_SIZE.get('tag'))
  ]

  table_data['comment'] = [
    {
      'user_id': random.choice(range(config.SQL_TABLE_DEMO_SIZE.get('user'))),
      'blog_id': random.choice(range(config.SQL_TABLE_DEMO_SIZE.get('blog'))),
      'content': ' '.join(random.choice(data['text']) for _ in range(random.randint(5, 50))),
      'time': int(time.time()) - random.randint(0, 100000000)
    }
    for index in range(config.SQL_TABLE_DEMO_SIZE.get('comment'))
  ]

  del table_data['user']
  del table_data['contest']
  del table_data['blog']
  del table_data['tag']

  return table_data
