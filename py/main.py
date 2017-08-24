#!/usr/bin/env python3

import psycopg2
import http.server
import contextlib

@contextlib.contextmanager
def schema_connection(connection_string, schema='log_1708'):

    class conwrap:
        '''
        Connection wrapper class.
        '''
        def __init__(self, con):
            self._con = con
        @contextlib.contextmanager
        def cursor(self):
            with self._con.cursor() as cur:
                cur.execute('set search_path = {}'.format(schema))
                yield cur

    with psycopg2.connect(connection_string) as con:
        yield conwrap(con)

def main_template(body_content):
    return bytes('''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
</head>
<body>
{body_content}
</body>
</html>'''.format(body_content=body_content), 'utf-8')

class Workout:
    def __init__(self, workout_id, timestamp, title):
        self.workout_id = workout_id
        self.timestamp  = timestamp
        self.title      = title
        self.sets       = None

    def load_sets(self, cursor):
        cursor.execute('''
            select
                *
            from
                t_sets
            where
                workout_id = %s
        ''', (self.workout_id,))
        self.sets = [ WorkoutSet(*row) for row in cursor.fetchall() ]
        print('Loaded', len(self.sets), 'sets.')

    def render(self):
        return '''
            <div class="workout">
                <h1>Workout #{workout_id}</h1>
                <p class="timestamp">{timestamp}</p>
                {title}
                <table>
                    <thead>
                        <tr>
                            <th>Exercise</th>
                            <th>Weight</th>
                            <th>Sets</th>
                            <th>Reps</th>
                        </tr>
                    </thead>
                    {sets}
                </table>
            </div>
        '''.format(
            workout_id=self.workout_id,
            timestamp=str(self.timestamp),
            title=self.title or '',
            sets=''.join( s.render() for s in self.sets ))


class WorkoutSet:
    def __init__(self, set_id, workout_id, exercise, sets, reps, weight, failure):
        self.set_id = set_id
        self.workout_id = workout_id
        self.exercise = exercise
        self.sets = sets
        self.reps = reps
        self.weight = weight
        self.failure = failure

    def render(self):
        return '''
            <tr class="workout_set {failure}">
                <td class="exercise">{exercise}</td>
                <td class="weight">{weight}</td>
                <td class="sets">{sets}</td>
                <td class="reps">{reps}</td>
            </tr>
        '''.format(
            workout_id=self.workout_id,
            set_id=self.set_id,
            exercise=self.exercise,
            sets=self.sets,
            reps=self.reps,
            weight=self.weight,
            failure='failure' if self.failure else 'no_failure',
        )

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def _connect_db(self):
        return schema_connection('dbname=training', schema='log_1708')

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        with self._connect_db() as con:
            with con.cursor() as cur:

                # fetch most recent workouts
                cur.execute('''
                    select
                        *
                    from
                        t_workouts
                    order by
                        timestamp
                        desc
                    limit
                        20
                    ''')
                workouts = [ Workout(*row) for row in cur.fetchall() ]

                for workout in workouts:
                    workout.load_sets(cur)

                self.wfile.write(main_template('''
                    <p>{N_workouts} workouts found.</p>
                    {workouts}
                '''.format(
                    N_workouts=len(workouts),
                    workouts=''.join( w.render() for w in workouts )
                )))

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write(bytes('<html><body><h1>POST!</h1></body></html>', 'utf-8'))
        
def run(server_class=http.server.HTTPServer, handler_class=RequestHandler, port=8098):

    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    print('Starting httpd...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print() # empty line

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
