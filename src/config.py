import streamlit as st
import time
import datetime

SQL_USER = 'competitive-programming-dbms-admin'
SQL_PASSWORD = '5up3r-s3cur3-p4ssw0rd'
SQL_HOST = 'localhost'
SQL_PORT = '3306'
SQL_DBNAME = 'cpdbms'

SQL_TABLENAMES = [
  'user', 'contest', 'blog', 'tag', 'comment', 'about', 'problem',
  'categorized', 'message', 'submission', 'gives'
]

_current_time = int(time.time())

_timestamp_to_date = lambda x: str(datetime.datetime.fromtimestamp(x))

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
      'type': _timestamp_to_date
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
        'value': 60,
        'key': 'contest.duration'
      },
      'type': int
    },
    'start_time': {
      'function': st.number_input,
      'params': {
        'label': 'Start Time',
        'min_value': 0,
        'value': _current_time,
        'key': 'contest.start_time'
      },
      'type': _timestamp_to_date
    }
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
    'user_id': {
      'function': st.number_input,
      'params': {
        'label': 'User ID',
        'min_value': 0,
        'key': 'blog.user_id'
      },
      'type': int
    },
    'time': {
      'function': st.number_input,
      'params': {
        'label': 'Time',
        'min_value': 0,
        'value': _current_time,
        'key': 'blog.time'
      },
      'type': _timestamp_to_date
    }
  },

  'tag': {
    'tag_id':{ 
      'function': st.number_input,
      'params': {
        'label': 'Tag ID',
        'min_value': 0,
        'key': 'tag.tag_id'
      },
      'type': int
    },
    'name':{ 
      'function': st.text_input,
      'params': {
        'label': 'Name',
        'max_chars': 20,
        'key': 'tag.name'
      },
      'type': str
    }
  },

  'comment': {
    'user_id': {
      'function': st.number_input,
      'params': {
        'label': 'User ID',
        'min_value': 0,
        'key': 'comment.user_id'
      },
      'type': int
    },
    'blog_id': {
      'function': st.number_input,
      'params': {
        'label': 'Blog ID',
        'min_value': 0,
        'key': 'comment.blog_id'
      },
      'type': int
    },
    'content': {
      'function': st.text_area,
      'params': {
        'label': 'Content',
        'max_chars': 200,
        'key': 'comment.content'
      },
      'type': str
    },
    'time': {
      'function': st.number_input,
      'params': {
        'label': 'Time',
        'min_value': 0,
        'value': _current_time,
        'key': 'comment.time'
      },
      'type': _timestamp_to_date
    }
  },

  'about': {
    'blog_id': {
      'function': st.number_input,
      'params': {
        'label': 'Blog ID',
        'min_value': 0,
        'key': 'about.blog_id'
      },
      'type': int
    },
    'tag_id': {
      'function': st.number_input,
      'params': {
        'label': 'Tag ID',
        'min_value': 0,
        'key': 'about.tag_id'
      },
      'type': int
    }
  },

  'problem': {
    'problem_id': {
      'function': st.number_input,
      'params': {
        'label': 'Problem ID',
        'min_value': 0,
        'key': 'problem.problem_id'
      },
      'type': int
    },
    'contest_id': {
      'function': st.number_input,
      'params': {
        'label': 'Contest ID',
        'min_value': 0,
        'key': 'problem.contest_id'
      },
      'type': int
    },
    'type': {
      'function': st.selectbox,
      'params': {
        'label': 'Type',
        'options': ['MCQ', 'Non-Interactive', 'Interactive'],
        'key': 'problem.type'
      },
      'type': str
    },
    'time_constraint': {
      'function': st.number_input,
      'params': {
        'label': 'Time Constraint',
        'min_value': 0,
        'value': 1,
        'key': 'problem.time_constraint'
      },
      'type': int
    },
    'memory_constraint': {
      'function': st.number_input,
      'params': {
        'label': 'Memory Constraint',
        'min_value': 0,
        'value': 256,
        'key': 'problem.memory_constraint'
      },
      'type': int
    }
  },

  'categorized': {
    'contest_id': {
      'function': st.number_input,
      'params': {
        'label': 'Contest ID',
        'min_value': 0,
        'key': 'categorized.contest_id'
      },
      'type': int
    },
    'problem_id': {
      'function': st.number_input,
      'params': {
        'label': 'Problem ID',
        'min_value': 0,
        'key': 'categorized.problem_id'
      },
      'type': int
    },
    'tag_id': {
      'function': st.number_input,
      'params': {
        'label': 'Tag ID',
        'min_value': 0,
        'key': 'categorized.tag_id'
      },
      'type': int
    },
  },

  'message': {
    'sender_id': {
      'function': st.number_input,
      'params': {
        'label': 'Sender ID',
        'min_value': 0,
        'key': 'message.sender_id'
      },
      'type': int
    },
    'receiver_id': {
      'function': st.number_input,
      'params': {
        'label': 'Receiver ID',
        'min_value': 0,
        'key': 'message.receiver_id'
      },
      'type': int
    },
    'body': {
      'function': st.text_area,
      'params': {
        'label': 'Body',
        'max_chars': 500,
        'key': 'message.body'
      },
      'type': str
    },
    'time': {
      'function': st.number_input,
      'params': {
        'label': 'Time',
        'min_value': 0,
        'value': _current_time,
        'key': 'message.time'
      },
      'type': _timestamp_to_date
    }
  },

  'submission': {
    'submission_id': {
      'function': st.number_input,
      'params': {
        'label': 'Submission ID',
        'min_value': 0,
        'key': 'submission.submission_id'
      },
      'type': int
    },
    'user_id': {
      'function': st.number_input,
      'params': {
        'label': 'User ID',
        'min_value': 0,
        'key': 'submission.user_id'
      },
      'type': int
    },
    'status': {
      'function': st.selectbox,
      'params': {
        'label': 'Status',
        'options': [
          'Failed', 'Passed', 'Partial', 'Compilation Error', 'Runtime Error',
          'Wrong Answer', 'Presentation Error', 'Time Limit Exceeded',
          'Memory Limit Exceeded', 'Idleness Limit Exceeded', 'Security Violated',
          'Crashed', 'Input Preparation Crashed', 'Challenged', 'Skipped',
          'Testing', 'Rejected'
        ],
        'key': 'submission.status'
      },
      'type': str
    },
    'execution_time': {
      'function': st.number_input,
      'params': {
        'label': 'Execution Time',
        'min_value': 0,
        'key': 'submission.execution_time'
      },
      'type': int
    },
    'execution_memory': {
      'function': st.number_input,
      'params': {
        'label': 'Execution Memory',
        'min_value': 0,
        'key': 'submission.execution_memory'
      },
      'type': int
    },
    'contest_id': {
      'function': st.number_input,
      'params': {
        'label': 'Contest ID',
        'min_value': 0,
        'key': 'submission.contest_id'
      },
      'type': int
    },
    'problem_id': {
      'function': st.number_input,
      'params': {
        'label': 'Problem ID',
        'min_value': 0,
        'key': 'submission.problem_id'
      },
      'type': int
    },
    'time': {
      'function': st.number_input,
      'params': {
        'label': 'Time',
        'min_value': 0,
        'value': _current_time,
        'key': 'submission.time'
      },
      'type': _timestamp_to_date
    }
  },

  'gives': {
    'user_id': {
      'function': st.number_input,
      'params': {
        'label': 'User ID',
        'min_value': 0,
        'key': 'gives.user_id'
      },
      'type': int
    },
    'contest_id': {
      'function': st.number_input,
      'params': {
        'label': 'Contest ID',
        'min_value': 0,
        'key': 'gives.contest_id'
      },
      'type': int
    },
    'rating_change': {
      'function': st.number_input,
      'params': {
        'label': 'Rating Change',
        'min_value': -500,
        'max_value': +500,
        'value': 0,
        'key': 'gives.rating_change'
      },
      'type': int
    },
    'rank': {
      'function': st.number_input,
      'params': {
        'label': 'Rank',
        'min_value': -1,
        'key': 'gives.rank'
      },
      'type': int
    }
  }
}
