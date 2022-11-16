import streamlit as st

SQL_USER = 'competitive-programming-dbms-admin'
SQL_PASSWORD = '5up3r-s3cur3-p4ssw0rd'
SQL_HOST = 'localhost'
SQL_PORT = '3306'
SQL_DBNAME = 'cpdbms'

SQL_TABLENAMES = [
  'user', 'contest', 'blog', 'tag', 'comment', 'about', 'problem',
  'categorized', 'message', 'submission', 'gives'
]

SQL_TABLE_ATTRIBUTES = {
  'user': {
    'user_id': {
      'function': st.number_input,
      'params': {
        'label': 'User ID',
        'min_value': 0,
        'value': 0,
        'key': 'user.user_id'
      },
      'type': int
    },
    'username': {
      'function': st.text_input,
      'params': {
        'label': 'Username',
        'max_chars': 20,
        'key': 'user.username'
      },
      'type': str
    },
    'password': {
      'function': st.text_input,
      'params': {
        'label': 'Password',
        'max_chars': 20,
        'key': 'user.password',
        'type': 'password'
      },
      'type': str
    },
    'email': {
      'function': st.text_input,
      'params': {
        'label': 'Email',
        'max_chars': 50,
        'key': 'user.email'
      },
      'type': str
    },
    'name': {
      'function': st.text_input,
      'params': {
        'label': 'Name',
        'max_chars': 50,
        'key': 'user.name'
      },
      'type': str
    },
    'rating': {
      'function': st.number_input,
      'params': {
        'label': 'Rating',
        'min_value': 0,
        'max_value': 4000,
        'value': 0,
        'key': 'user.rating'
      },
      'type': int
    },
    'contribution': {
      'function': st.number_input,
      'params': {
        'label': 'Contribution',
        'min_value': 0,
        'max_value': 1000,
        'value': 0,
        'key': 'user.contribution'
      },
      'type': int
    },
    'institute': {
      'function': st.text_input,
      'params': {
        'label': 'Institute',
        'max_chars': 50,
        'key': 'user.institute'
      },
      'type': str
    },
    'country': {
      'function': st.text_input,
      'params': {
        'label': 'Country',
        'max_chars': 50,
        'key': 'user.country'
      },
      'type': str
    },
    'last_online': {
      'function': st.number_input,
      'params': {
        'label': 'Last Online',
        'min_value': 0,
        'value': 0,
        'key': 'user.lastonline'
      },
      'type': int
    }
  },

  'contest': {
    'contest_id': {
      'function': st.number_input,
      'params': {
        'label': 'Contest ID',
        'key': 'contest.contest_id'
      },
      'type': int
    },
    'name': {
      'function': st.text_input,
      'params': {
        'label': 'Name',
        'max_chars': 50,
        'key': 'contest.name'
      },
      'type': str
    },
    'type': {
      'function': st.selectbox,
      'params': {
        'label': 'Type',
        'options': ['Normal', 'IOI', 'ICPC'],
        'key': 'contest.type'
      },
      'type': str
    },
    'duration': {
      'function': st.number_input,
      'params': {
        'label': 'Duration',
        'min_value': 0,
        'key': 'contest.duration'
      },
      'type': int
    },
    'start_time': {
      'function': st.number_input,
      'params': {
        'label': 'Start Time',
        'min_value': 0,
        'key': 'contest.start_time'
      },
      'type': int
    },
  },

  'blog': {
    'blog_id': {
      'function': st.number_input,
      'params': {
        'label': 'Blog ID',
        'min_value': 0,
        'key': 'blog.blog_id'
      },
      'type': int
    },
    'title': {
      'function': st.text_input,
      'params': {
        'label': 'Title',
        'max_chars': 50,
        'key': 'blog.title'
      },
      'type': str
    },
    'content': {
      'function': st.text_area,
      'params': {
        'label': 'Content',
        'max_chars': 1000,
        'key': 'blog.content'
      },
      'type': str
    },
    'upvote_count': {
      'function': st.number_input,
      'params': {
        'label': 'Upvote Count',
        'min_value': 0,
        'key': 'blog.upvote_count'
      },
      'type': int
    },
    'downvote_count': {
      'function': st.number_input,
      'params': {
        'label': 'Downvote Count',
        'min_value': 0,
        'key': 'blog.downvote_count'
      },
      'type': int
    },
    'writer_id': {
      'function': st.number_input,
      'params': {
        'label': 'Writer ID',
        'min_value': 0,
        'key': 'blog.writer_id'
      },
      'type': int
    },
    'time': {
      'function': st.number_input,
      'params': {
        'label': 'Time',
        'min_value': 0,
        'key': 'blog.time'
      },
      'type': int
    },
  },

  'tag': {
    'tag_id'
    'name'
  }
}
