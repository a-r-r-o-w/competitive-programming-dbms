import streamlit as st
import mysql.connector

import config
import initialize
import create
import read
import update
import delete
import query

def main () -> None:
  connection = mysql.connector.connect(
    user = config.SQL_USER,
    password = config.SQL_PASSWORD,
    host = config.SQL_HOST,
    port = config.SQL_PORT,
    autocommit = True
  )

  cursor = connection.cursor()

  st.set_page_config(
    page_title = 'CP DBMS',
    layout = 'wide',
    initial_sidebar_state = 'expanded'
  )
  st.header('Competitive Programming Platform')
  st.sidebar.header('Options')
  operation = st.sidebar.selectbox(
    'Operation',
    ('Initialize', 'Create', 'Read', 'Update', 'Delete', 'Query', 'Cleanup')
  )

  match operation:
    case 'Initialize':
      initialize.initialize(cursor)
    
    case 'Create':
      create.create(cursor)
    
    case 'Read':
      read.read(cursor)
    
    case 'Update':
      update.update(cursor)
    
    case 'Delete':
      delete.delete(cursor)
    
    case 'Query':
      query.query(cursor)
    
    case 'Cleanup':
      initialize.cleanup(cursor)
    
    case other:
      st.error('Invalid Option selected', icon = '🚨')

if __name__ == '__main__':
  main()
