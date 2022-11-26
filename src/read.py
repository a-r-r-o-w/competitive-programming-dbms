import streamlit as st
import mysql.connector.cursor
import pandas as pd

import config
import queries

def read (cursor: mysql.connector.cursor.MySQLCursor):
  '''
  Least/Most Recent Blogs
  '''
  st.subheader('Least/Most Recent Blogs')
  st.write('List of least/most recently published blogs')

  col1, col2 = st.columns(2)

  with col1:
    blog_count = st.slider('Blog Count', 0, config.SQL_TABLE_DEMO_SIZE.get('blog') - 1)
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
    for index, result in df.iterrows():
      institute = result.get('institute')
      count = result.get('count(*)')

      if institute:
        res = f'**{institute}** has {count} users'
      else:
        res = f'{count} users do not have an Organisation set'
      
      st.markdown(res)
  
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
    rating = []
    date = []

    for index, result in df.iterrows():
      if len(rating) > 0:
        rating.append(rating[-1] + result.get('rating_change'))
      else:
        rating.append(result.get('rating_change'))
      date.append(result.get('contest_start_time'))
    
    plot_df = pd.DataFrame(zip(rating, date), columns = ['Rating', 'Date'])
    st.line_chart(plot_df, x = 'Date', y = 'Rating')
  
  st.markdown('---')
