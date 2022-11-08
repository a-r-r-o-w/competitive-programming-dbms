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
      is_db_created = True
      st.info(f'Database "{dbname}" created successfully!')
    
    elif is_db_created:
      st.error(f'Cleanup existing database "{dbname}" before creating new!')
    
    else:
      st.info('Database with this name already exists!')
  
  if is_db_created:
    st.subheader('Data Initialization')

    with st.container():
      st.write('Initialize the database by clicking the seed buttons for each table')

      first, second = st.columns(2)

      with first:
        st.write('This is first')
        
        with st.expander("See query"):
          st.write('First query')
        
        st.write('After query')
        st.button('Execute', key = 'button-execute-query-1')
      
      with second:
        st.write('This is second')

        with st.expander("See query"):
          st.write('Second query')
        
        st.write('After query')
        st.button('Execute', key = 'button-execute-query-2')

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
