\encoding 'UTF-8'

-- suppress warnings in psql output
set client_min_messages TO WARNING;

/*
 * Prepare database
 *
 */

-- never use public, ever. like, yeh.
drop schema if exists public;

-- use custom schema instead
create schema if not exists log_1708;
set search_path = log_1708;

/*
 * Load modules
 *
 */

\echo

\echo '*** TRAINING MODULE ***'
\ir 'training/__module__.sql'
\echo
