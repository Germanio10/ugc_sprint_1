CREATE DATABASE replica;
//Ok
//0 rows in set. Elapsed: 0.032 sec.

CREATE TABLE replica.test (id Int64,
       user_id Int64,
       view_time Int64,
       event_time DateTime) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/test', 'replica_2') PARTITION BY toYYYYMMDD(event_time) ORDER BY id;
//Ok.
//0 rows in set. Elapsed: 0.047 sec.
