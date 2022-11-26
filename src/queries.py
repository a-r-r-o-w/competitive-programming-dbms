import typing

# database related

def create_database (dbname) -> str:
  return f'create database {dbname}'

def use_database (dbname):
  return f'use {dbname}'

def delete_database (dbname) -> str:
  return f'drop database {dbname}'

# table creation related

def create_table_user () -> str:
  return '''\
create table if not exists user (
  user_id int primary key,
  username varchar(20) not null,
  password varchar(20) not null,
  email varchar(50) not null,
  name varchar(50) not null,
  rating int not null default 0,
  contribution int not null default 0,
  institute varchar(50),
  country varchar(50),
  last_online timestamp
) engine=InnoDB default charset=utf8
'''

def create_table_contest () -> str:
  return '''\
create table if not exists contest (
  contest_id int primary key,
  name varchar(50) not null,
  type varchar(10) not null,
  duration int not null default 60,
  start_time timestamp
) engine=InnoDB default charset=utf8
'''

def create_table_blog () -> str:
  return '''\
create table if not exists blog (
  blog_id int primary key,
  title varchar(100) not null default ' ',
  content varchar(2000),
  upvote_count int not null default 0,
  downvote_count int not null default 0,
  user_id int,
  time timestamp,
  foreign key (user_id) references user(user_id)
    on delete set default
    on update cascade
) engine=InnoDB default charset=utf8
'''

def create_table_tag () -> str:
  return '''\
create table if not exists tag (
  tag_id int primary key,
  name varchar(50)
) engine=InnoDB default charset=utf8
'''

def create_table_comment () -> str:
  return '''\
create table if not exists comment (
  user_id int,
  blog_id int,
  content varchar(1000),
  time timestamp,
  primary key (user_id, blog_id, time),
  foreign key (user_id) references user(user_id)
    on delete set default
    on update cascade,
  foreign key (blog_id) references blog(blog_id)
    on delete set default
    on update cascade
) engine=InnoDB default charset=utf8
'''

def create_table_about () -> str:
  return '''\
create table if not exists about (
  blog_id int,
  tag_id int,
  primary key (blog_id, tag_id),
  foreign key (blog_id) references blog(blog_id)
    on delete set default
    on update cascade,
  foreign key (tag_id) references tag(tag_id)
    on delete set default
    on update cascade
) engine=InnoDB default charset=utf8
'''

def create_table_problem () -> str:
  return '''\
create table if not exists problem (
  problem_id int,
  contest_id int,
  description varchar(2000) not null,
  type varchar(50) not null,
  time_constraint int not null default 1,
  memory_constraint int not null default 256,
  points int not null default 0,
  primary key (problem_id, contest_id),
  foreign key (contest_id) references contest(contest_id)
    on delete set default
    on update cascade
) engine=InnoDB default charset=utf8
'''

def create_table_categorized () -> str:
  return '''\
create table if not exists categorized (
  problem_id int,
  tag_id int,
  primary key (problem_id, tag_id),
  foreign key (problem_id) references problem(problem_id)
    on delete set default
    on update cascade,
  foreign key (tag_id) references tag(tag_id)
    on delete set default
    on update cascade
) engine=InnoDB default charset=utf8
'''

def create_table_message () -> str:
  return '''\
create table if not exists message (
  sender_id int,
  receiver_id int,
  body varchar(1000) not null,
  time timestamp,
  primary key (sender_id, receiver_id, time),
  foreign key (sender_id) references user(user_id)
    on delete set default
    on update cascade,
  foreign key (receiver_id) references user(user_id)
    on delete set default
    on update cascade
) engine=InnoDB default charset=utf8
'''

def create_table_submission () -> str:
  return '''\
create table if not exists submission (
  submission_id int primary key,
  user_id int,
  status varchar(50),
  execution_time int not null default 0,
  execution_memory int not null default 0,
  contest_id int,
  problem_id int,
  time int,
  foreign key (user_id) references user(user_id)
    on delete set default
    on update cascade,
  foreign key (contest_id, problem_id) references problem(contest_id, problem_id)
    on delete set default
    on update cascade
) engine=InnoDB default charset=utf8
'''

def create_table_gives () -> str:
  return '''\
create table if not exists gives (
  user_id int,
  contest_id int,
  rating_change int not null default 0,
  rank int not null default -1,
  primary key (user_id, contest_id),
  foreign key (user_id) references user(user_id)
    on delete set default
    on update cascade,
  foreign key (contest_id) references contest(contest_id)
    on delete set default
    on update cascade
) engine=InnoDB default charset=utf8
'''

def insert_one (table_name: str, data: dict) -> str:
  keys = []
  values = []
  
  for k, v in data.items():
    keys.append(k)

    if type(v) == int or type(v) == float:
      values.append(f'{v}')
    elif type(v) == str:
      values.append(f"'{v}'")
    else:
      raise TypeError('Invalid type used in insert statement')
  
  keys = ', '.join(keys)
  values = ', '.join(values)

  return f'''\
insert into {table_name} 
  ({keys})
values
  ({values})
'''

def insert_many (table_name: str, data: typing.List[dict]):
  keys = [key for key in data[0].keys()]
  values = []

  for item in data:
    value = []

    for key in keys:
      v = item[key]

      if type(v) == int or type(v) == float:
        value.append(f'{v}')
      elif type(v) == str:
        value.append(f"'{v}'")
      else:
        raise TypeError('Invalid type used in insert statement')
    
    value = ', '.join(value)
    values.append(value)
  
  keys = ', '.join(keys)
  values = ',\n'.join(f'({value})' for value in values)
  
  return f'''\
insert into {table_name}
  ({keys})
values
  {values}
'''
