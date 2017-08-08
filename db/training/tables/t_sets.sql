\echo '* t_sets'

create table if not exists t_sets
  ( id              serial
                    primary key
  , workout_id      int
                    references t_workouts (id)

  , exercise        text

  , sets            int
                    not null
                    default 1

  , reps            int
                    not null
                    default 1

  , weight          float
                    not null

  , failure         boolean
                    not null
                    default false
  );
