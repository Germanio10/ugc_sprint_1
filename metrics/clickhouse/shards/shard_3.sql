CREATE DATABASE shard;
//Ok.
//0 rows in set. Elapsed: 0.010 sec.

CREATE TABLE shard.test (id Int64,
       user_id Int64,
       view_time Int64,
       event_time DateTime) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/test', 'replica_1') PARTITION BY toYYYYMMDD(event_time) ORDER BY id;
//Ok.
//0 rows in set. Elapsed: 0.081 sec.

CREATE TABLE default.test (id Int64,
       user_id Int64,
       view_time Int64,
       event_time DateTime) Engine = Distributed('company_cluster', '', test, rand());
//Ok.
//0 rows in set. Elapsed: 0.039 sec.
