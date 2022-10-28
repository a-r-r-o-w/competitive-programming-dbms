import streamlit as st

def main () -> None:
  st.header('Competitive Programming Platform')
  st.sidebar.header('Options')
  operation = st.sidebar.selectbox(
    'Operation',
    ('Create', 'Read', 'Update', 'Delete')
  )
  st.subheader(operation)

  match operation:
    case 'Create':
      pass
    case 'Read':
      pass
    case 'Update':
      pass
    case 'Delete':
      pass
    case other:
      st.error('Invalid Option selected', icon = '🚨')

if __name__ == '__main__':
  main()
