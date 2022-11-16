import streamlit as st
import mysql.connector.cursor

import config
import queries

def query (cursor: mysql.connector.cursor.MySQLCursor) -> None:
  st.subheader('Custom Query')
  
  custom_query = st.text_input(label = 'Enter custom query')
  execute_custom_query_button = st.button('Execute Custom Query', key = 'execute_custom_query_button')

  if execute_custom_query_button:
    st.info(f'''\
Executing query:\n
\n
```sql
{custom_query}
```
''')
    
    cursor.execute(queries.use_database(config.SQL_DBNAME))
    cursor.execute(custom_query)
    data = {}

    try:
      data = cursor.fetchall()
    except Exception as e:
      st.error(e)

    st.subheader('Query Results')
    st.write(data)
