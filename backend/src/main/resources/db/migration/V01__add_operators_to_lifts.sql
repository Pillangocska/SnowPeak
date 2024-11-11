alter table lift
    drop column lift_ext_id;

drop table if exists worker;

create table worker(
                       worker_lift_id  uuid          not null,
                       worker_id       uuid          not null,

                       constraint fk_worker_id_worker_lift_id foreign key (worker_lift_id) references lift (lift_id),
                       primary key (worker_lift_id, worker_id)
);

alter table lift
    add column lift_master_operator_id  uuid    not null default '2c57337d-99ba-4d8d-8b1a-9eafc6b2ef2d';