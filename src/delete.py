import streamlit as st
import mysql.connector.cursor
import pandas as pd
import matplotlib.pyplot as plt

import config
import queries

def delete (cursor: mysql.connector.cursor.MySQLCursor):
  st.write('Select table')
  table_selection = st.selectbox('Table', config.SQL_TABLENAMES)
  attribute = st.selectbox('Attribute', config.SQL_TABLE_ATTRIBUTES[table_selection])
  props = config.SQL_TABLE_ATTRIBUTES[table_selection].get(attribute)
  value = props.get('type')(props.get('function')(**props.get('params')))

  query = f'''
delete from
  {table_selection}
where 
  {attribute} = {value}
'''

  st.code(query)

  if st.button('Delete'):
    cursor.execute(queries.use_database(config.SQL_DBNAME))
    cursor.execute(query)
    st.info('Delete executed successfully')
