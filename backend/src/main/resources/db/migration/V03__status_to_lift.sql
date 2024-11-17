alter table lift
    add column lift_status  varchar(255)    not null default 'PUBLIC';

alter table log
    drop column log_queue_name;