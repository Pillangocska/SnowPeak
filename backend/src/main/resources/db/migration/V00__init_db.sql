drop table if exists lift;
drop table if exists log;

create table lift(
    lift_id                uuid          not null primary key,
    lift_ext_id            uuid          not null,
    lift_start_latitude    float         not null,
    lift_start_longitude   float         not null,
    lift_start_elevation   float         not null,
    lift_end_latitude      float         not null,
    lift_end_longitude     float         not null,
    lift_end_elevation     float         not null,
    lift_seat_capacity     int           not null,
    lift_num_seats         int           not null
);

create table log(
    log_id          uuid            not null primary key,
    log_lift_id     uuid            not null,
    log_payload     json            not null,
    log_time        timestamp       not null,

    constraint fk_log_id_to_lift_id foreign key (log_lift_id) references lift(lift_id)
);