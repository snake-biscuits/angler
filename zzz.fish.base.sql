-- zzz.fish.base.sql (2025-02-22)
-- ----------------------------------- --
-- Elpis Ultimate Angler Championship  --
--  ===  Zenless Zone Zero Event  ===  --
-- 2025/02/14 10:00 - 2025/03/10 03:59 --
-- ----------------------------------- --
-- SQL Fishing Encyclopedia

-- tables
CREATE TABLE IF NOT EXISTS Fish (
    name  VARCHAR NOT NULL,
    shiny VARCHAR  -- Rare Subspecies
);

CREATE TABLE IF NOT EXISTS Spot (
    name  VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS FishSpot (
    fish  NUMBER NOT NULL,
    spot  NUMBER NOT NULL,
    FOREIGN KEY (fish) REFERENCES Fish(rowid),
    FOREIGN KEY (spot) REFERENCES Spot(rowid)
);

CREATE TABLE IF NOT EXISTS Time (
    name  VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS FishTime (
    fish  NUMBER NOT NULL,
    time  NUMBER NOT NULL,
    FOREIGN KEY (fish) REFERENCES Fish(rowid),
    FOREIGN KEY (time) REFERENCES Time(rowid)
);

CREATE TABLE IF NOT EXISTS Catch (
    time  NUMBER  NOT NULL,
    spot  NUMBER  NOT NULL,
    fish  NUMBER  NOT NULL,
    stars NUMBER  NOT NULL,  -- 1-3
    shiny BOOLEAN NOT NULL,  -- is shiny
    FOREIGN KEY (time) REFERENCES Time(rowid),
    FOREIGN KEY (spot) REFERENCES Spot(rowid),
    FOREIGN KEY (fish) REFERENCES Fish(rowid)
);

-- data
-- TODO: replace NULLs once shinies have been caught
INSERT INTO Fish(name, shiny) VALUES
    ('Mackerel', 'Spiny-Finned Mackerel'),
    ('Flatfish', 'Yellow-Scaled Flatfish'),
    ('Crescent Grunter', 'Crimson Lightning'),
    ('Striped Prawn', 'Tiger Prawn'),
    ('Roller Octopus', 'Coral Octopus'),
    ('Arrow Squid', 'Rocket Squid'),
    ('Porcupinefish', 'Blown-Up Pufferfish'),
    ('Seahorse', 'Red-Brown Seahorse'),
    ('Lantern Fish', 'Infernal Lantern'),
    ('Butterfly Fish', NULL),
    ('Humphead Fish', 'Rounded-Headed Immortal'),
    ('Blackfin Shark', 'Zebra Shark'),
    ('Little Flying Octopus', 'Pink-Fringed Octopus'),
    ('Bluefin Tuna', 'Deep-Sea Gem'),
    ('Lionfish', 'Dance of Fire'),
    ('Sailfish', 'Green-Winged Warship'),
    ('Manta Ray', 'Sea Monster Carpet');

INSERT INTO Spot(name) VALUES
    ('Coastal'),    -- Coastal Fishing Spot
    ('Bridge'),     -- Bridge Fishing Spot
    ('Deepwater'),  -- Deepwater Fishing Spot
    ('Reef');       -- Reef Fishing Spot (Coastal Reef)

INSERT INTO FishSpot(fish, spot) VALUES
    (1, 1), (1, 2), (1, 3), (1, 4),  -- Mackerel
    (2, 1), (2, 2), (2, 3), (2, 4),  -- Flatfish
    (3, 3), (3, 4),                  -- Crescent Grunter
    (4, 1), (4, 4),                  -- Striped Prawn
    (5, 1),                          -- Roller Octopus
    (6, 1),                          -- Arrow Squid
    (7, 1),                          -- Porcupinefish
    (8, 2), (8, 3), (8, 4),          -- Seahorse
    (9, 2),                          -- Lantern Fish
    (10, 2), (10, 4),                -- Butterfly Fish
    (11, 2), (11, 4),                -- Humphead Fish
    (12, 3),                         -- Blackfin Shark
    (13, 3),                         -- Little Flying Octopus
    (14, 3),                         -- Bluefin Tuna
    (15, 4),                         -- Lionfish
    (16, 4),                         -- Sailfish
    (17, 4);                         -- Manta Ray

INSERT INTO Time(name) VALUES
    ('Morning'),    -- Yellow Sun & Clound
    ('Afternoon'),  -- Orange Sun
    ('Evening'),    -- Blue Moon
    ('LateNight'); -- Navy Mood & Cloud

INSERT INTO FishTime(fish, time) VALUES
    (1, 1), (1, 2), (1, 3), (1, 4),      -- Mackerel
    (2, 1), (2, 2), (2, 3), (2, 4),      -- Flatfish
    (3, 1), (3, 2), (3, 3), (3, 4),      -- Crescent Grunter
    (4, 1), (4, 2), (4, 3), (4, 4),      -- Striped Prawn
    (5, 1), (5, 2), (5, 3), (5, 4),      -- Roller Octopus
    (6, 1), (6, 2), (6, 3),              -- Arrow Squid
    (7, 1), (7, 2), (7, 3), (7, 4),      -- Porcupinefish
    (8, 1), (8, 2), (8, 3), (8, 4),      -- Seahorse
    (9, 1), (9, 2), (9, 3), (9, 4),      -- Lantern Fish
    (10, 1), (10, 2), (10, 3), (10, 4),  -- Butterfly Fish
    (11, 1), (11, 2), (11, 3), (11, 4),  -- Humphead Fish
    (12, 2), (12, 3), (12, 4),           -- Blackfin Shark
    (13, 1), (13, 2), (13, 3), (13, 4),  -- Little Flying Octopus
    (14, 1), (14, 2), (14, 3), (14, 4),  -- Bluefin Tuna
    (15, 1), (15, 2), (15, 3), (15, 4),  -- Lionfish
    (16, 1), (16, 2), (16, 3), (16, 4),  -- Sailfish
    (17, 1), (17, 2), (17, 3);           -- Manta Ray

-- NOTE: you should track your catches in your own .sql or .db
