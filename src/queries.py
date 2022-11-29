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
    on delete cascade
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
    on delete cascade
    on update cascade,
  foreign key (blog_id) references blog(blog_id)
    on delete cascade
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
    on delete cascade
    on update cascade,
  foreign key (tag_id) references tag(tag_id)
    on delete cascade
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
    on delete cascade
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
    on delete cascade
    on update cascade,
  foreign key (tag_id) references tag(tag_id)
    on delete cascade
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
    on delete cascade
    on update cascade,
  foreign key (receiver_id) references user(user_id)
    on delete cascade
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
    on delete cascade
    on update cascade,
  foreign key (contest_id, problem_id) references problem(contest_id, problem_id)
    on delete cascade
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
    on delete cascade
    on update cascade,
  foreign key (contest_id) references contest(contest_id)
    on delete cascade
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

def most_recent_blogs (blog_count: int, blog_order: str):
  if blog_order == 'Least Recent':
    order = 'asc'
  else:
    order = 'desc'
  
  return f'''
select
  blog.*, user.username
from
  blog
join
  user on blog.user_id = user.user_id
order by
  time {order}
limit {blog_count}
'''

def user_count_in_organisations ():
  return '''
select
  institute, count(*)
from
  user
group by
  institute
order by
  count(*) desc
'''

def user_rating_graph (user_id):
  return f'''
select
  gives.user_id, gives.contest_id, gives.rating_change,
  contest.name as 'contest_name', contest.start_time as 'contest_start_time'
from
  user
join
  gives on user.user_id = gives.user_id
join
  contest on gives.contest_id = contest.contest_id
where
  user.user_id = {user_id}
order by
  contest.start_time
'''

def user_contribution (user_count, user_order):
  if user_order == 'Ascending':
    order = 'asc'
  else:
    order = 'desc'
  
  return f'''
select
  user_id, username, contribution
from
  user
order by
  contribution {order}
limit {user_count}
'''

def user_rating (user_count, user_order):
  if user_order == 'Ascending':
    order = 'asc'
  else:
    order = 'desc'
  
  return f'''
select
  user_id, username, rating
from
  user
order by
  rating {order}
limit {user_count}
'''

def problem_list (problem_count, problem_order):
  if problem_order == 'Ascending':
    order = 'asc'
  else:
    order = 'desc'
  
  return f'''
select
  *
from
  problem
order by
  problem_id {order}
limit {problem_count}
'''

def contest_problems (contest_id):
  return f'''
select
  *
from
  problem
where
  contest_id = {contest_id}
order by
  problem_id
'''

def drop_count_problems_in_tags_function ():
  return '''
drop function if exists count_problems_in_tags
'''

def count_problems_in_tags_function ():
  return '''
create function count_problems_in_tags (id int)
returns int
deterministic
begin
  declare problem_count int;
  set problem_count = (
    select
      count(*)
    from
      categorized as C natural join problem as P
    where
      C.tag_id = id
  );
  return problem_count;
end;
'''

def problem_in_categories ():
  return '''
select
  T.name as tag, problem_count
from
  tag as T natural join (
    select
      C.tag_id, (select count_problems_in_tags(C.tag_id)) as problem_count
    from
      categorized as C
    group by
      C.tag_id
  ) as tag_counts
'''
