import streamlit as st
import mysql.connector.cursor

import config
import queries

def create (cursor: mysql.connector.cursor.MySQLCursor) -> None:
  with st.expander('Add random generated data'):
    pass

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
