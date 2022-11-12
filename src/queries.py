# database related

def create_database (dbname):
  return f'create database {dbname}'

def use_database (dbname):
  return f'use {dbname}'

def delete_database (dbname):
  return f'drop database {dbname}'

# table creation related

def create_table_user ():
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
) engine=InnoDB default charset = utf8
'''

def create_table_contest ():
  return '''\
create table if not exists contest (
  contest_id int primary key,
  name varchar(50) not null,
  type varchar(50) not null,
  duration int not null default 60,
  start_time timestamp
) engine=InnoDB default charset = utf8
'''

def create_table_blog ():
  return '''\
create table if not exists blog (
  blog_id int primary key,
  title varchar(50) not null default ' ',
  content varchar(500),
  upvote_count int not null default 0,
  downvote_count int not null default 0,
  writer_id int,
  time timestamp,
  foreign key (writer_id) references user(user_id)
    on delete set default
    on update cascade
) engine=InnoDB default charset = utf8
'''

def create_table_tag ():
  return '''\
create table if not exists tag (
  tag_id int primary key,
  name varchar(20)
) engine=InnoDB default charset = utf8
'''

def create_table_comment ():
  return '''\
create table if not exists comment (
  writer_id int,
  blog_id int,
  content varchar(100),
  time timestamp,
  primary key (writer_id, blog_id, time),
  foreign key (writer_id) references user(user_id)
    on delete set default
    on update cascade,
  foreign key (blog_id) references blog(blog_id)
    on delete set default
    on update cascade
)
'''

def create_table_about ():
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
)
'''

def create_table_problem ():
  return '''\
create table if not exists problem (
  problem_id int,
  contest_id int,
  type varchar(50) not null,
  time_constraint int not null default 1,
  memory_constraint int not null default 256,
  primary key (problem_id, contest_id),
  foreign key (contest_id) references contest(contest_id)
    on delete set default
    on update cascade
)
'''

def create_table_categorized ():
  return '''\
create table if not exists categorized (
  contest_id int,
  problem_id int,
  tag_id int,
  primary key (problem_id, contest_id, tag_id),
  foreign key (contest_id, problem_id) references problem(contest_id, problem_id)
    on delete set default
    on update cascade,
  foreign key (tag_id) references tag(tag_id)
    on delete set default
    on update cascade
)
'''

def create_table_message ():
  return '''\
create table if not exists message (
  sender_id int,
  receiver_id int,
  body varchar(200) not null,
  time timestamp,
  primary key (sender_id, receiver_id, time),
  foreign key (sender_id) references user(user_id)
    on delete set default
    on update cascade,
  foreign key (receiver_id) references user(user_id)
    on delete set default
    on update cascade
)
'''

def create_table_submission ():
  return '''\
create table if not exists submission (
  submission_id int primary key,
  user_id int,
  status varchar(30),
  execution_time int not null default 0,
  execution_memory int not null default 0,
  contest_id int,
  problem_id int,
  time timestamp,
  foreign key (user_id) references user(user_id)
    on delete set default
    on update cascade,
  foreign key (contest_id, problem_id) references problem(contest_id, problem_id)
    on delete set default
    on update cascade
)
'''

def create_table_gives ():
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
)
'''
