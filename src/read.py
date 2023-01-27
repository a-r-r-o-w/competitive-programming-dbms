import streamlit as st
import mysql.connector.cursor
import pandas as pd
import matplotlib.pyplot as plt

import config
import queries

def read (cursor: mysql.connector.cursor.MySQLCursor):
  config.SQL_FUNCTIONS_SETUP = True
  cursor.execute(queries.use_database(config.SQL_DBNAME))
  cursor.execute(queries.drop_count_problems_in_tags_function())
  cursor.execute(queries.count_problems_in_tags_function())
  cursor.execute(queries.drop_display_user_profile())
  cursor.execute(queries.display_user_profile())
  cursor.execute(queries.drop_users_with_five_contests_and_a_blog())
  cursor.execute(queries.users_with_five_contests_and_a_blog())

  '''
  Least/Most Recent Blogs
  '''
  st.subheader('Least/Most Recent Blogs')
  st.write('List of least/most recently published blogs')

  col1, col2 = st.columns(2)

  with col1:
    blog_count = st.slider('Blog Count', 1, config.SQL_TABLE_DEMO_SIZE.get('blog'))
  with col2:
    blog_order = st.selectbox('Blog Order', ['Least Recent', 'Most Recent'], index = 1)

  cursor.execute(queries.use_database(config.SQL_DBNAME))
  cursor.execute(queries.most_recent_blogs(blog_count, blog_order))

  df = pd.DataFrame(columns = cursor.column_names)
  data = {}
  
  try:
    data = cursor.fetchall()
    df = pd.DataFrame(data = data, columns = cursor.column_names)
  except Exception as e:
    st.error(e)

  with st.expander('See Query'):
    st.code(queries.most_recent_blogs(blog_count, blog_order))
  
  with st.expander('See Dataframe'):
    st.dataframe(df)
  
  with st.expander('See Result'):
    for index, result in df.iterrows():
      st.subheader(result.get('title'))
      st.markdown(f'**Author: {result.get("username")}**')
      st.markdown(f'**Posted: {result.get("time")}**')
      st.markdown(f'**Votes:** {result.get("upvote_count") - result.get("downvote_count")}')
      st.markdown(result.get('content'))
      
      if index < df.shape[0] - 1:
        st.markdown('---')
  
  st.markdown('---')

  '''
  User Count in Organisation
  '''
  st.subheader('User Count in Organisation')
  st.write('Count of number of users in every organisation')

  cursor.execute(queries.use_database(config.SQL_DBNAME))
  cursor.execute(queries.user_count_in_organisations())

  df = pd.DataFrame(columns = cursor.column_names)
  data = {}

  try:
    data = cursor.fetchall()
    df = pd.DataFrame(data = data, columns = cursor.column_names)
  except Exception as e:
    st.error(e)

  with st.expander('See Query'):
    st.code(queries.user_count_in_organisations())
  
  with st.expander('See Dataframe'):
    st.dataframe(df)
  
  with st.expander('See Result'):
    # df[df['institute'] == ''] = ('None', 0)
    fig1, ax1 = plt.subplots()
    ax1.pie(df['count(*)'], labels = df['institute'])
    ax1.axis('equal')
    st.pyplot(fig1)
  
  st.markdown('---')
  
  '''
  User Rating Graph
  '''
  st.subheader('User Rating Graph')
  st.write('Rating graph of a user')

  user_id = st.selectbox('User ID', list(range(config.SQL_TABLE_DEMO_SIZE.get('user'))))

  cursor.execute(queries.use_database(config.SQL_DBNAME))
  cursor.execute(queries.user_rating_graph(user_id))

  df = pd.DataFrame(columns = cursor.column_names)
  data = {}
  
  try:
    data = cursor.fetchall()
    df = pd.DataFrame(data = data, columns = cursor.column_names)
  except Exception as e:
    st.error(e)

  with st.expander('See Query'):
    st.code(queries.user_rating_graph(user_id))
  
  with st.expander('See Dataframe'):
    st.dataframe(df)
  
  with st.expander('See Result'):
    rating = [1500]
    date = [0]

    for index, result in df.iterrows():
      if len(rating) > 0:
        rating.append(rating[-1] + result.get('rating_change'))
      else:
        rating.append(result.get('rating_change'))
      date.append(result.get('contest_start_time'))
    
    date[0] = date[1]
    plot_df = pd.DataFrame(zip(rating, date), columns = ['Rating', 'Date'])
    st.line_chart(plot_df, x = 'Date', y = 'Rating')
  
  st.markdown('---')

  '''
  Contributions
  '''
  st.subheader('Contributions')
  st.write('Contribution of users')

  col1, col2 = st.columns(2)

  with col1:
    user_count = st.slider('User Count', 1, config.SQL_TABLE_DEMO_SIZE.get('user'), key = 'user_count_contribution')
  with col2:
    user_order = st.selectbox('User Order', ['Ascending', 'Descending'], 1, key = 'user_order_contribution')

  cursor.execute(queries.use_database(config.SQL_DBNAME))
  cursor.execute(queries.user_contribution(user_count, user_order))

  df = pd.DataFrame(columns = cursor.column_names)
  data = {}
  
  try:
    data = cursor.fetchall()
    df = pd.DataFrame(data = data, columns = cursor.column_names)
  except Exception as e:
    st.error(e)

  with st.expander('See Query'):
    st.code(queries.user_contribution(user_count, user_order))
  
  with st.expander('See Dataframe'):
    st.dataframe(df)
  
  with st.expander('See Result'):
    st.dataframe(df)
  
  st.markdown('---')
  
  '''
  Rating
  '''
  st.subheader('Rating')
  st.write('Rating of users')

  col1, col2 = st.columns(2)

  with col1:
    user_count = st.slider('User Count', 1, config.SQL_TABLE_DEMO_SIZE.get('user'), key = 'user_count_rating')
  with col2:
    user_order = st.selectbox('User Order', ['Ascending', 'Descending'], 1, key = 'user_order_rating')

  cursor.execute(queries.use_database(config.SQL_DBNAME))
  cursor.execute(queries.user_rating(user_count, user_order))

  df = pd.DataFrame(columns = cursor.column_names)
  data = {}
  
  try:
    data = cursor.fetchall()
    df = pd.DataFrame(data = data, columns = cursor.column_names)
  except Exception as e:
    st.error(e)

  with st.expander('See Query'):
    st.code(queries.user_rating(user_count, user_order))
  
  with st.expander('See Dataframe'):
    st.dataframe(df)
  
  with st.expander('See Result'):
    st.dataframe(df)
  
  st.markdown('---')

  '''
  Problems
  '''
  st.subheader('Problems')
  st.write('List of problems')

  col1, col2 = st.columns(2)

  with col1:
    problem_count = st.slider('Problem Count', 1, config.SQL_TABLE_DEMO_SIZE.get('problem'), key = 'problem_count_contribution')
  with col2:
    problem_order = st.selectbox('Problem Order', ['Ascending', 'Descending'], 1, key = 'problem_order_contribution')

  cursor.execute(queries.use_database(config.SQL_DBNAME))
  cursor.execute(queries.problem_list(problem_count, problem_order))

  df = pd.DataFrame(columns = cursor.column_names)
  data = {}
  
  try:
    data = cursor.fetchall()
    df = pd.DataFrame(data = data, columns = cursor.column_names)
  except Exception as e:
    st.error(e)

  with st.expander('See Query'):
    st.code(queries.problem_list(problem_count, problem_order))
  
  with st.expander('See Dataframe'):
    st.dataframe(df)
  
  with st.expander('See Result'):
    st.dataframe(df)
  
  st.markdown('---')

  '''
  Contest Problems
  '''
  st.subheader('Contest Problems')
  st.write('Problems in a Contest')

  contest_id = st.selectbox('Contest ID', list(range(config.SQL_TABLE_DEMO_SIZE.get('contest'))))

  cursor.execute(queries.use_database(config.SQL_DBNAME))
  cursor.execute(queries.contest_problems(contest_id))

  df = pd.DataFrame(columns = cursor.column_names)
  data = {}
  
  try:
    data = cursor.fetchall()
    df = pd.DataFrame(data = data, columns = cursor.column_names)
  except Exception as e:
    st.error(e)

  with st.expander('See Query'):
    st.code(queries.contest_problems(contest_id))
  
  with st.expander('See Dataframe'):
    st.dataframe(df)
  
  with st.expander('See Result'):
    st.dataframe(df)
  
  st.markdown('---')

  '''
  Number of Problems in Different Categories
  '''
  st.subheader('Problems in Different Categories')
  st.write('Number of Problems in Different Categories')

  cursor.execute(queries.use_database(config.SQL_DBNAME))
  cursor.execute(queries.problem_in_categories())

  df = pd.DataFrame(columns = cursor.column_names)
  data = {}
  
  try:
    data = cursor.fetchall()
    df = pd.DataFrame(data = data, columns = cursor.column_names)
  except Exception as e:
    st.error(e)

  with st.expander('See Query'):
    st.code(queries.problem_in_categories())
  
  with st.expander('See Dataframe'):
    st.dataframe(df)
  
  with st.expander('See Result'):
    fig1, ax1 = plt.subplots()
    ax1.pie(df['problem_count'], labels = df['tag'])
    ax1.axis('equal')
    st.pyplot(fig1)
  
  st.markdown('---')

  '''
  Display User Profile
  '''
  st.subheader('Display User Profile')
  st.write('Display User Profile')

  user_id = st.selectbox('User ID', list(range(config.SQL_TABLE_DEMO_SIZE.get('user'))), key = 'user_id_display_profile')

  qry = f'''
select
  contest.name as contests
from
  contest natural join (
    select
      gives.contest_id
    from
      gives natural join user
    where
      user.user_id = {user_id}
  ) as t
'''

  # '''
  # Number of Problems in Different Categories
  # '''
  # st.subheader('Problems in Different Categories')
  # st.write('Number of Problems in Different Categories')

  # cursor.execute(queries.use_database(config.SQL_DBNAME))
  # cursor.execute(queries.problem_in_categories())

  # df = pd.DataFrame(columns = cursor.column_names)
  # data = {}
  
  # try:
  #   data = cursor.fetchall()
  #   df = pd.DataFrame(data = data, columns = cursor.column_names)
  # except Exception as e:
  #   st.error(e)

  # with st.expander('See Query'):
  #   st.code(queries.problem_in_categories())
  
  # with st.expander('See Dataframe'):
  #   st.dataframe(df)
  
  # with st.expander('See Result'):
  #   fig1, ax1 = plt.subplots()
  #   ax1.pie(df['problem_count'], labels = df['tag'])
  #   ax1.axis('equal')
  #   st.pyplot(fig1)
  
  # st.markdown('---')

  cursor.execute(queries.use_database(config.SQL_DBNAME))
  cursor.execute(qry)

  df = pd.DataFrame(columns = cursor.column_names)
  data = {}
  
  try:
    data = cursor.fetchall()
    df = pd.DataFrame(data = data, columns = cursor.column_names)
  except Exception as e:
    st.error(e)

  with st.expander('See Query'):
    st.code(queries.display_user_profile())
    st.code(queries.user_profile(user_id))
  
  with st.expander('See Dataframe'):
    st.dataframe(df)
  
  with st.expander('See Result'):
    st.dataframe(df)
  
  st.markdown('---')
