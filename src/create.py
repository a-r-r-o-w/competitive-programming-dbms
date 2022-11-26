import streamlit as st
import mysql.connector.cursor
import random
import time
import datetime

import config
import queries

is_data_generated = False
data = {
  'user': [],
  'contest': [],
  'blog': [],
  'tag': [],
  'comment': [],
  'about': [],
  'problem': [],
  'categorized': [],
  'message': [],
  'submission': [],
  'gives': []
}

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
    
    if st.button('Insert Data'):
      insert_data(cursor)

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
    st.code(queries.insert_one(table_selection, values))
  
  if st.button(label = f'Add {table_selection}', key = 'add_table_selection'):
    cursor.execute(queries.use_database(config.SQL_DBNAME))
    cursor.execute(queries.insert_one(table_selection, values))
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
      'last_online': get_random_time()
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
              )[0],
      'duration': random.choices(
                    population = [60, 90, 120, 135, 150, 165, 180],
                    weights = [5, 5, 50, 10, 10, 5, 15]
                  )[0],
      'start_time': get_random_time()
    }
    for index in range(config.SQL_TABLE_DEMO_SIZE.get('contest'))
  ]

  table_data['blog'] = [
    {
      'blog_id': index,
      'title': ' '.join(random.choice(data['text']) for _ in range(random.randint(2, 10))),
      'content': ' '.join(random.choice(data['text']) for _ in range(random.randint(20, 100))),
      'upvote_count': random.randint(0, 500),
      'downvote_count': random.randint(0, 100),
      'user_id': random.choice(range(config.SQL_TABLE_DEMO_SIZE.get('user'))),
      'time': get_random_time()
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
      'time': get_random_time()
    }
    for index in range(config.SQL_TABLE_DEMO_SIZE.get('comment'))
  ]

  about = set()

  while len(about) < config.SQL_TABLE_DEMO_SIZE.get('about'):
    blog_id = random.choice(range(config.SQL_TABLE_DEMO_SIZE.get('blog')))
    tag_id = random.choice(range(config.SQL_TABLE_DEMO_SIZE.get('tag')))
    about.add((blog_id, tag_id))
  
  about = list(about)

  table_data['about'] = [
    {
      'blog_id': about[index][0],
      'tag_id': about[index][1]
    }
    for index in range(config.SQL_TABLE_DEMO_SIZE.get('about'))
  ]

  table_data['problem'] = [
    {
      'problem_id': index,
      'contest_id': random.choice(range(config.SQL_TABLE_DEMO_SIZE.get('contest'))),
      'description': ' '.join(random.choice(data['text']) for _ in range(random.randint(20, 200))),
      'type': random.choices(
                population = ['MCQ', 'Non-Interactive', 'Interactive'],
                weights = [10, 70, 20]
              )[0],
      'time_constraint': random.choice([0.5, 1, 1.5, 2, 2.5, 3, 5, 10]),
      'memory_constraint': random.choices(
                              population = [16, 32, 64, 128, 256, 512, 1024],
                              weights = [5, 5, 10, 10, 50, 15, 5]
                            )[0],
      'points': random.choice([250, 500, 750, 1000, 1250, 1500, 2000, 2500, 3000])
    }
    for index in range(config.SQL_TABLE_DEMO_SIZE.get('problem'))
  ]

  contest_problems = {}

  for problem in table_data['problem']:
    contest_id: int = problem.get('contest_id')
    problem_id: int = problem.get('problem_id')

    if contest_id in contest_problems.keys():
      contest_problems[contest_id].append(problem_id)
    else:
      contest_problems[contest_id] = [problem_id]

  categorized = set()

  while len(categorized) < config.SQL_TABLE_DEMO_SIZE.get('categorized'):
    problem_id = random.choice(range(config.SQL_TABLE_DEMO_SIZE.get('problem')))
    tag_id = random.choice(range(config.SQL_TABLE_DEMO_SIZE.get('tag')))
    categorized.add((problem_id, tag_id))
  
  categorized = list(categorized)
  
  table_data['categorized'] = [
    {
      'problem_id': categorized[index][0],
      'tag_id': categorized[index][1]
    }
    for index in range(config.SQL_TABLE_DEMO_SIZE.get('categorized'))
  ]

  table_data['message'] = [
    {
      'sender_id': random.choice(range(config.SQL_TABLE_DEMO_SIZE.get('user'))),
      'receiver_id': random.choice(range(config.SQL_TABLE_DEMO_SIZE.get('user'))),
      'body': ' '.join(random.choice(data['text']) for _ in range(random.randint(1, 50))),
      'time': get_random_time()
    }
    for index in range(config.SQL_TABLE_DEMO_SIZE.get('message'))
  ]

  table_data['submission'] = [
    {
      'submission_id': index,
      'user_id': random.choice(range(config.SQL_TABLE_DEMO_SIZE.get('user'))),
      'status': random.choices(
                  population = [
                    'Failed', 'Passed', 'Partial', 'Compilation Error', 'Runtime Error',
                    'Wrong Answer', 'Presentation Error', 'Time Limit Exceeded',
                    'Memory Limit Exceeded', 'Idleness Limit Exceeded', 'Security Violated',
                    'Crashed', 'Input Preparation Crashed', 'Challenged', 'Skipped',
                    'Testing', 'Rejected'
                  ],
                  weights = [
                    3, 40, 2, 3, 3,
                    25, 1, 5, 
                    3, 2, 1,
                    1, 1, 3, 3,
                    3, 1
                  ]
                )[0],
      'execution_time': random.random() * random.choice(range(1, 5 + 1)),
      'execution_memory': random.random() * random.choice(range(16, 256 + 1)),
      'contest_id': random.choice(range(config.SQL_TABLE_DEMO_SIZE.get('contest'))),
      'problem_id': -1,
      'time': int(random.random() * 1000)
    }
    for index in range(config.SQL_TABLE_DEMO_SIZE.get('submission'))
  ]

  for submission in table_data['submission']:
    submission['problem_id'] = random.choice(contest_problems.get(submission['contest_id']))
  
  gives = set()

  while len(gives) < config.SQL_TABLE_DEMO_SIZE.get('gives'):
    user_id = random.choice(range(config.SQL_TABLE_DEMO_SIZE.get('user')))
    contest_id = random.choice(range(config.SQL_TABLE_DEMO_SIZE.get('contest')))
    gives.add((user_id, contest_id))
  
  gives = list(gives)
  
  table_data['gives'] = [
    {
      'user_id': gives[index][0],
      'contest_id': gives[index][1],
      'rating_change': random.randint(-200, 400),
      'rank': random.randint(1, 10000)
    }
    for index in range(config.SQL_TABLE_DEMO_SIZE.get('gives'))
  ]

  return table_data

def insert_data (cursor: mysql.connector.cursor.MySQLCursor):
  if not is_data_generated:
    return
  
  for table_name, table_data in data.items():
    cursor.execute(queries.use_database(config.SQL_DBNAME))
    cursor.execute(queries.insert_many(table_name, table_data))
    st.info(f'Data inserted into table "{table_name}" sucessfully')
  
  st.info('Database initialized with random data')

def get_random_time ():
  return str(datetime.datetime.fromtimestamp(int(time.time()) - random.randint(0, 100000000)))
