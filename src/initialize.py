import random
import string
import streamlit as st
import mysql.connector.cursor

import config
import queries

def generate_random_name () -> str:
  return 'cpdbms_' + ''.join(random.sample(string.ascii_lowercase, 10))

dbname = generate_random_name()
is_db_created = False

def initialize (cursor: mysql.connector.cursor.MySQLCursor) -> None:
  global dbname, is_db_created
  
  st.subheader('Database Creation')

  with st.expander('MySQL Connection Information'):
    st.json({
      'SQL_USER': config.SQL_USER,
      'SQL_PASSWORD': config.SQL_PASSWORD,
      'SQL_HOST': config.SQL_HOST,
      'SQL_PORT': config.SQL_PORT
    })
    st.write('Connect to server with using the following command:')
    st.code(f'''mysql -u {config.SQL_USER} -p'{config.SQL_PASSWORD}' -h {config.SQL_HOST} -P {config.SQL_PORT}''')
  
  dbname = st.text_input(label = 'Database Name', value = dbname, autocomplete = dbname, max_chars = 20)
  
  if st.button('Create'):
    if not is_db_created:
      cursor.execute(queries.create_database(dbname))
      cursor.execute(queries.use_database(dbname))
      is_db_created = True
      st.info(f'Database "{dbname}" created successfully!')
    
    elif is_db_created:
      st.error(f'Cleanup existing database "{dbname}" before creating new!')
    
    else:
      st.info('Database with this name already exists!')
  
  if is_db_created:
    st.subheader('Data Initialization')

    with st.container():
      st.write('Create all tables by executing all commands or individually executing')

      execute_all_button = st.button('Execute All', key = 'execute_all_button')
      
      st.markdown('##') ## line spacing

      user, contest = st.columns(2)

      with user:
        st.markdown('##### User')
        
        with st.expander("See query"):
          st.code(queries.create_table_user())
        
        create_user_button = st.button('Execute', key = 'create_user_button')

        if execute_all_button or create_user_button:
          cursor.execute(queries.use_database(dbname))
          cursor.execute(queries.create_table_user())
          st.info('User table created succesfully')
      
      with contest:
        st.markdown('##### Contest')
        
        with st.expander("See query"):
          st.code(queries.create_table_contest())
        
        create_contest_button = st.button('Execute', key = 'create_contest_button')

        if execute_all_button or create_contest_button:
          cursor.execute(queries.use_database(dbname))
          cursor.execute(queries.create_table_contest())
          st.info('Contest table created succesfully')
      
      st.markdown('##') # line spacing

      blog, tag = st.columns(2)

      with blog:
        st.markdown('##### Blog')
        
        with st.expander("See query"):
          st.code(queries.create_table_blog())
        
        create_blog_button = st.button('Execute', key = 'create_blog_button')

        if execute_all_button or create_blog_button:
          cursor.execute(queries.use_database(dbname))
          cursor.execute(queries.create_table_blog())
          st.info('Blog table created succesfully')
      
      with tag:
        st.markdown('##### Tag')
        
        with st.expander("See query"):
          st.code(queries.create_table_tag())
        
        create_tag_button = st.button('Execute', key = 'create_tag_button')

        if execute_all_button or create_tag_button:
          cursor.execute(queries.use_database(dbname))
          cursor.execute(queries.create_table_tag())
          st.info('Tag table created succesfully')
      
      st.markdown('##') # line spacing
      
      comment, about = st.columns(2)

      with comment:
        st.markdown('##### Comment')
        
        with st.expander("See query"):
          st.code(queries.create_table_comment())
        
        create_comment_button = st.button('Execute', key = 'create_comment_button')

        if execute_all_button or create_comment_button:
          cursor.execute(queries.use_database(dbname))
          cursor.execute(queries.create_table_comment())
          st.info('Comment table created succesfully')
      
      with about:
        st.markdown('##### About')
        
        with st.expander("See query"):
          st.code(queries.create_table_about())
        
        create_about_button = st.button('Execute', key = 'create_about_button')

        if execute_all_button or create_about_button:
          cursor.execute(queries.use_database(dbname))
          cursor.execute(queries.create_table_about())
          st.info('About table created succesfully')
      
      st.markdown('##') # line spacing
      
      problem, categorized = st.columns(2)

      with problem:
        st.markdown('##### Problem')
        
        with st.expander("See query"):
          st.code(queries.create_table_problem())
        
        create_problem_button = st.button('Execute', key = 'create_problem_button')

        if execute_all_button or create_problem_button:
          cursor.execute(queries.use_database(dbname))
          cursor.execute(queries.create_table_problem())
          st.info('Problem table created succesfully')
      
      with categorized:
        st.markdown('##### Categorized')
        
        with st.expander("See query"):
          st.code(queries.create_table_categorized())
        
        create_categorized_button = st.button('Execute', key = 'create_categorized_button')

        if execute_all_button or create_categorized_button:
          cursor.execute(queries.use_database(dbname))
          cursor.execute(queries.create_table_categorized())
          st.info('Categorized table created succesfully')
      
      st.markdown('##') # line spacing
      
      message, submission = st.columns(2)

      with message:
        st.markdown('##### Message')
        
        with st.expander("See query"):
          st.code(queries.create_table_message())
        
        create_message_button = st.button('Execute', key = 'create_message_button')

        if execute_all_button or create_message_button:
          cursor.execute(queries.use_database(dbname))
          cursor.execute(queries.create_table_message())
          st.info('Message table created succesfully')
      
      with submission:
        st.markdown('##### Submission')
        
        with st.expander("See query"):
          st.code(queries.create_table_submission())
        
        create_submission_button = st.button('Execute', key = 'create_submission_button')

        if execute_all_button or create_submission_button:
          cursor.execute(queries.use_database(dbname))
          cursor.execute(queries.create_table_submission())
          st.info('Submission table created succesfully')
      
      st.markdown('##') # line spacing

      gives, _ = st.columns(2)

      with gives:
        st.markdown('##### Gives')
        
        with st.expander("See query"):
          st.code(queries.create_table_gives())
        
        create_gives_button = st.button('Execute', key = 'create_gives_button')

        if execute_all_button or create_gives_button:
          cursor.execute(queries.use_database(dbname))
          cursor.execute(queries.create_table_gives())
          st.info('Gives table created succesfully')

def cleanup (cursor: mysql.connector.cursor.MySQLCursor) -> None:
  global is_db_created

  if is_db_created:
    st.info(f'Database: {dbname}')
    
    if st.button('Cleanup'):
      cursor.execute(queries.delete_database(dbname))
      st.info(f'Database "{dbname}" deleted successfully!')
      is_db_created = False
  
  else:
    st.info('No database created')
