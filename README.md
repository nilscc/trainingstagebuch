Setup
=====

PostgreSQL Database
-------------------

Developed for PostgreSQL 9.

First create a new database:

    $ createdb training

Then run the main SQL script:

    $ psql -f db/main.sql training

This will install all SQL tables. Open the database with psql:

    $ psql training

Once in the database list all existing schemas:

    training=# \dn
       Liste der Schemas
       Name   | Eigentümer
    ----------+------------
     log_1708 | nils
    (1 Zeile)


Pick the most recent one:

    training=# set search_path = log_1708;


To see all tables use `\dt`:

    training=# \dt
                 Liste der Relationen
      Schema  |    Name    |   Typ   | Eigentümer
    ----------+------------+---------+------------
     log_1708 | t_sets     | Tabelle | nils
     log_1708 | t_workouts | Tabelle | nils
    (2 Zeilen)


For more information on a table use `\d`, e.g.:

    training=# \d t_workouts
                                         Tabelle »log_1708.t_workouts«
      Spalte   |             Typ             |                          Attribute
    -----------+-----------------------------+-------------------------------------------------------------
     id        | integer                     | not null Vorgabewert nextval('t_workouts_id_seq'::regclass)
     timestamp | timestamp without time zone | not null Vorgabewert now()
     title     | text                        |
    Indexe:
        "t_workouts_pkey" PRIMARY KEY, btree (id)
    Fremdschlüsselverweise von:
        TABLE "t_sets" CONSTRAINT "t_sets_workout_id_fkey" FOREIGN KEY (workout_id) REFERENCES t_workouts(id)

    training=# \d t_sets
                                    Tabelle »log_1708.t_sets«
       Spalte   |       Typ        |                        Attribute
    ------------+------------------+---------------------------------------------------------
     id         | integer          | not null Vorgabewert nextval('t_sets_id_seq'::regclass)
     workout_id | integer          |
     exercise   | text             |
     sets       | integer          | not null Vorgabewert 1
     reps       | integer          | not null Vorgabewert 1
     weight     | double precision | not null
     failure    | boolean          | not null Vorgabewert false
    Indexe:
        "t_sets_pkey" PRIMARY KEY, btree (id)
    Fremdschlüssel-Constraints:
        "t_sets_workout_id_fkey" FOREIGN KEY (workout_id) REFERENCES t_workouts(id)


To add a new workout, simply [INSERT] a new row into `t_workouts` with default values:

    training=# insert into t_workouts default values returning id;
     id
    ----
      1
    (1 Zeile)

    INSERT 0 1


Then add all workout sets to this workout ID, again using [INSERT]:

    training=# insert into t_sets (workout_id, exercise, weight, reps, sets) values (1, '3x clean + jerk', 60, 3, 2);
    training=# insert into t_sets (workout_id, exercise, weight, reps, sets) values (1, '3x clean + jerk', 70, 3, 1);
    training=# insert into t_sets (workout_id, exercise, weight, reps, sets) values (1, '3x clean + jerk', 75, 3, 1);
    training=# insert into t_sets (workout_id, exercise, weight, reps, sets) values (1, '3x clean + jerk', 80, 3, 1);
    training=# insert into t_sets (workout_id, exercise, weight, reps, sets) values (1, '3x clean + jerk', 85, 3, 1);
    training=# insert into t_sets (workout_id, exercise, weight, reps, sets) values (1, 'c&j', 90, 1, 2);
    training=# insert into t_sets (workout_id, exercise, weight, reps, sets) values (1, 'jerk from rack', 60, 3, 2);
    training=# insert into t_sets (workout_id, exercise, weight, reps, sets) values (1, 'jerk from rack', 65, 3, 1);
    training=# insert into t_sets (workout_id, exercise, weight, reps, sets) values (1, 'jerk from rack', 70, 3, 1);
    training=# insert into t_sets (workout_id, exercise, weight, reps, sets) values (1, 'jerk from rack', 75, 3, 1);
    training=# insert into t_sets (workout_id, exercise, weight, reps, sets) values (1, 'fsq', 60, 3, 1);
    training=# insert into t_sets (workout_id, exercise, weight, reps, sets) values (1, 'fsq', 100, 3, 1);
    training=# insert into t_sets (workout_id, exercise, weight, reps, sets) values (1, 'fsq', 110, 3, 1);
    training=# insert into t_sets (workout_id, exercise, weight, reps, sets) values (1, 'fsq', 120, 3, 1);


And eventually display all data using [SELECT]:

    training=# select * from t_sets where workout_id = 1;
     id | workout_id |    exercise     | sets | reps | weight | failure
    ----+------------+-----------------+------+------+--------+---------
      1 |          1 | 3x clean + jerk |    2 |    3 |     60 | f
      2 |          1 | 3x clean + jerk |    1 |    3 |     70 | f
      3 |          1 | 3x clean + jerk |    1 |    3 |     75 | f
      4 |          1 | 3x clean + jerk |    1 |    3 |     80 | f
      5 |          1 | 3x clean + jerk |    1 |    3 |     85 | f
      6 |          1 | c&j             |    2 |    1 |     90 | f
      7 |          1 | jerk from rack  |    2 |    3 |     60 | f
      8 |          1 | jerk from rack  |    1 |    3 |     65 | f
      9 |          1 | jerk from rack  |    1 |    3 |     70 | f
     10 |          1 | jerk from rack  |    1 |    3 |     75 | f
     11 |          1 | fsq             |    1 |    3 |     60 | f
     12 |          1 | fsq             |    1 |    3 |    100 | f
     13 |          1 | fsq             |    1 |    3 |    110 | f
     14 |          1 | fsq             |    1 |    3 |    120 | f
    (14 Zeilen)


All workouts are listed in the `t_workouts`  table:

    training=# select * from t_workouts;
     id |         timestamp          | title
    ----+----------------------------+-------
      1 | 2017-08-08 22:37:37.308922 |
    (1 Zeile)


To add a title to the workout, [UPDATE] the corresponding row:

    training=# update t_workouts set title = 'The first workout' where id = 1;
    training=# select * from t_workouts;
     id |         timestamp          |       title
    ----+----------------------------+-------------------
      1 | 2017-08-08 22:37:37.308922 | The first workout
    (1 Zeile)



[SELECT]: https://www.postgresql.org/docs/current/static/sql-select.html
[INSERT]: https://www.postgresql.org/docs/current/static/sql-insert.html
[UPDATE]: https://www.postgresql.org/docs/current/static/sql-update.html
