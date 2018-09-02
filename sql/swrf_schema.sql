
create table boat ( boatid integer primary key,
                    skipperid integer,
                    name text not null,
                    sail_number integer,
                    model text,
                    meas_i real,
                    meas_j real,
                    meas_p real,
                    meas_e real,
                    phrf_rlc integer,
                    phrf_buoy integer,
                    nonspin integer,
                    active integer,
                    foreign key (skipperid) references person(personid) );


create table person ( personid integer primary key,
                      last_name text,
                      first_name text not null );

create table race ( raceid integer primary key,
                    courseid integer,
                    name text not null,
                    date_time text not null,
                    distance_nm real,
                    high_points integer, --TODO: too SWRF specific?
                    foreign key (courseid) references course(courseid) );

create table series ( seriesid integer,
                      name text not null,
                      best_of integer not null );

create table series_race ( seriesid integer,
                           raceid integer,
                           racenum integer,
                           foreign key (seriesid) references series(seriesid),
                           foreign key (raceid) references race(raceid) );

create table course ( courseid integer primary key,
                      distance_nm real );

create table mark ( markid integer primary key,
                    name text not null,
                    latitude real,
                    longitude real );

create table courses_mark ( courseid integer,
                            markid integer,
                            marknum integer not null,
                            foreign key (courseid) references course(courseid),
                            foreign key (markid) references mark(markid) );

create table race_result ( raceid integer not null,
                           boatid integer not null,
                           result TEXT, -- TODO: enum
                           start_time text,
                           phrf integer,
                           handicap_speed real,
                           nonspin integer,
                           correction integer,
                           finish_time text,
                           phrf_correction text,
                           foreign key (boatid) references boat(boatid) );
