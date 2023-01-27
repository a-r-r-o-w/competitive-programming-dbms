import streamlit as st
import mysql.connector.cursor
import pandas as pd
import matplotlib.pyplot as plt
import random
import string

import config
import queries

def update (cursor: mysql.connector.cursor.MySQLCursor):
  st.write('Select table')
  table_selection = st.selectbox('Table', config.SQL_TABLENAMES)
  
  selection_attribute = st.selectbox('Selection Attribute', config.SQL_TABLE_ATTRIBUTES[table_selection])
  props = config.SQL_TABLE_ATTRIBUTES[table_selection].get(selection_attribute)
  selection_value = props.get('type')(props.get('function')(**props.get('params')))
  
  change_attribute = st.selectbox('Change Attribute', config.SQL_TABLE_ATTRIBUTES[table_selection])
  props = config.SQL_TABLE_ATTRIBUTES[table_selection].get(change_attribute)
  d = props.get('params').copy()
  d['key'] += 'change'
  change_value = props.get('type')(props.get('function')(**d))

  query = f'''
update
  {table_selection}
set
  {change_attribute} = "{change_value}"
where
  {selection_attribute} = {selection_value}
'''

  st.code(query)

  if st.button('Update'):
    cursor.execute(queries.use_database(config.SQL_DBNAME))
    cursor.execute(query)
    st.info('Update executed successfully')
