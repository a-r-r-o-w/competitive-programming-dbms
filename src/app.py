import streamlit as st
import mysql.connector

import config
import initialize
import query

def main () -> None:
  connection = mysql.connector.connect(
    user = config.SQL_USER,
    password = config.SQL_PASSWORD,
    host = config.SQL_HOST,
    port = config.SQL_PORT
  )

  cursor = connection.cursor()

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
      pass
    
    case 'Read':
      pass
    
    case 'Update':
      pass
    
    case 'Delete':
      pass
    
    case 'Query':
      query.query(cursor)
    
    case 'Cleanup':
      initialize.cleanup(cursor)
    
    case other:
      st.error('Invalid Option selected', icon = '🚨')

if __name__ == '__main__':
  main()
