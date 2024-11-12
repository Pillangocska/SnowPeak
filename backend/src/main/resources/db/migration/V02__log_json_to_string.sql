alter table log
alter column log_payload type text
using log_payload::text;