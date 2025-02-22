-- zzz.fish.junk.sql (2025-02-22)
-- ----------------------------------- --
-- Elpis Ultimate Angler Championship  --
--  ===  Zenless Zone Zero Event  ===  --
-- 2025/02/14 10:00 - 2025/03/10 03:59 --
-- ----------------------------------- --
-- SQL Fishing Encyclopedia

-- !!! load zzz.fish.base.sql first !!!

-- NOTE: Junk starts at Fish index 18
-- you can filter out Junk w/ `WHERE Fish.rowid < 18`
INSERT INTO Fish(name) VALUES
    ('Aluminium Can'),
    ('Waterlogged Ether Battery'),
    ('Waterlogged Message Bottle'); 
-- NOTE: The following are one-time-only (story) catches:
-- Mini Submarine
-- Drift Bottle No.1
-- Sharkboo (Bling)
-- Ugly Doll
-- Drift Bottle No.2
-- Drift Bottle No.3

INSERT INTO FishSpot(fish, spot) VALUES
    (18, 1), (18, 2), (18, 3),           -- Can
    (19, 1), (19, 2), (19, 3), (19, 4),  -- Battery
    (20, 1), (20, 2), (20, 4);           -- Message

INSERT INTO FishTime(fish, time) VALUES
    (18, 1), (18, 2), (18, 3),           -- Can
    (19, 1), (19, 2), (19, 3), (19, 4),  -- Battery
    (20, 1), (20, 2), (20, 3), (20, 4);  -- Message
