SET client_encoding TO 'UTF8';

-- Drop + Create Tables
DROP TABLE IF EXISTS artist_credit;
CREATE TABLE artist_credit (
    id BIGINT,
    name TEXT,
    artist_count SMALLINT,
    ref_count INTEGER,
    created TIMESTAMP,
    edits_pending INTEGER,
    gid UUID
);

DROP TABLE IF EXISTS artist_credit_name;
CREATE TABLE artist_credit_name (
    artist_credit BIGINT,
    position SMALLINT,
    artist BIGINT,
    name TEXT,
    join_phrase TEXT
);

DROP TABLE IF EXISTS release;
CREATE TABLE release (
    id BIGINT,
    gid UUID,
    name TEXT,
    artist_credit BIGINT,
    release_group BIGINT,
    status SMALLINT,
    packaging SMALLINT,
    language SMALLINT,
    script SMALLINT,
    barcode TEXT,
    comment TEXT,
    edits_pending INTEGER,
    quality SMALLINT,
    last_updated TIMESTAMP
);

DROP TABLE IF EXISTS release_group;
CREATE TABLE release_group (
    id BIGINT,
    gid UUID,
    name TEXT,
    artist_credit BIGINT,
    type SMALLINT,
    comment TEXT,
    edits_pending INTEGER,
    last_updated TIMESTAMP
);

DROP TABLE IF EXISTS release_group_secondary_type_join;
CREATE TABLE release_group_secondary_type_join (
    release_group BIGINT,
    secondary_type SMALLINT,
    created TIMESTAMP
);

DROP TABLE IF EXISTS release_group_secondary_type;
CREATE TABLE release_group_secondary_type (
    id SMALLINT,
    name TEXT,
    parent SMALLINT,
    child_order SMALLINT,
    description TEXT,
    gid UUID
);

-- Import Data
\copy artist_credit FROM 'D:\\Temp\\mbdump\\artist_credit_final.tsv' WITH (FORMAT csv, DELIMITER E'\t', NULL '\N', HEADER false);
\copy artist_credit_name FROM 'D:\\Temp\\mbdump\\artist_credit_name_final.tsv' WITH (FORMAT csv, DELIMITER E'\t', NULL '\N', HEADER false);
\copy release FROM 'D:\\Temp\\mbdump\\release_final.tsv' WITH (FORMAT csv, DELIMITER E'\t', NULL '\N', HEADER false);
\copy release_group FROM 'D:\\Temp\\mbdump\\release_group_final.tsv' WITH (FORMAT csv, DELIMITER E'\t', NULL '\N', HEADER false);
\copy release_group_secondary_type_join FROM 'D:\\Temp\\mbdump\\release_group_secondary_type_join_final.tsv' WITH (FORMAT csv, DELIMITER E'\t', NULL '\N', HEADER false);
\copy release_group_secondary_type FROM 'D:\\Temp\\mbdump\\release_group_secondary_type_final.tsv' WITH (FORMAT csv, DELIMITER E'\t', NULL '\N', HEADER false);
