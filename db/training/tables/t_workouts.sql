\echo '* t_workouts'

create table if not exists t_workouts
  ( id              serial
                    primary key
  , timestamp       timestamp
                    not null
                    default now()
  , title           text
  );
