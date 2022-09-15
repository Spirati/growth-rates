--The primary keys should consist of [DISCORD SNOWFLAKE]-[name]
--The classes should as well just for convenience

CREATE TABLE IF NOT EXISTS Units (
    id varchar(255) NOT NULL PRIMARY KEY,
    class varchar(255),
    hp int,
    str int,
    mag int,
    dex int,
    spd int,
    lck int,
    def int,
    res int
);

CREATE TABLE IF NOT EXISTS Classes (
    id varchar(255) NOT NULL PRIMARY KEY,
    hp int,
    str int,
    mag int,
    dex int,
    spd int,
    lck int,
    def int,
    res int
);

INSERT OR IGNORE INTO Classes ( id, hp, str, mag, dex, spd, lck, def, res ) VALUES (
    "42069-test class",             420, 69,  69,  69,  69,  69,  69,  69  
);