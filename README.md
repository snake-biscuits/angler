# ZZZ Angler Contest Tracker
```
Elpis Ultimate Angler Championship
 ===  Zenless Zone Zero Event  ===
2025/02/14 10:00 - 2025/03/10 03:59
```

## Usage

 1. Start the server in a terminal
    * `$ python fishfinder.py`
 2. Connect to `localhost:8000` in your web browser
 3. Select fishing spot & time of day
 4. Log catches
 5. Check catch rates
 6. Try fishing in a different time and place for better rates


## Goals
 - [x] know when and where to fish
   - [x] via sql queries
   - [ ] in http server
 - [x] record catches
 - [ ] `.svg` map of the docks & island
 - [ ] track completion
 - [x] reverse engineer drop rates from catch records
 - [ ] track story catches (not really nessecary)


## Variants
all fish are 3 weight stars + 1 "shiny" star
catching a 3-star weight unlocks star 1 & 2
need to track this in our queries
otherwise we'll have false positives on what needs catching

catching a shiny won't unlock the base fish
though this doesn't matter for completion afaik, just OCD


## Queries
```bash
$ sqlite3
```
```sql
> .read zzz.fish.base.sql
> .read zzz.fish.junk.sql  -- optional
> -- do your queries / track your catches
> .quit
```

### List Fish in Spot
```sql
SELECT F.name
FROM FishSpot AS FS
INNER JOIN Fish AS F ON FS.fish == F.rowid
INNER JOIN Spot AS S ON FS.spot == S.rowid
WHERE S.name == 'Deepwater';
```

### List Fish in Spot at Time
```sql
SELECT COUNT(*)
FROM FishSpot AS FS
INNER JOIN Fish AS F ON FS.fish == F.rowid
INNER JOIN Spot AS S ON FS.spot == S.rowid
INNER JOIN FishTime AS FT ON FT.fish == F.rowid
INNER JOIN Time AS T ON FT.time == T.rowid
WHERE S.name == 'Deepwater' AND T.name == 'Morning';
```

### Catch Rates
> TODO: rates relative to each spot
> -- needs the catch count to be a second query
```sql
-- catch count
SELECT COUNT(*) FROM Catch;

-- catch percentage
SELECT F.name, ROUND(COUNT(*) * 1.0 / 101, 2)  -- 101 is the total catch count
FROM Catch AS C
INNER JOIN Fish AS F ON C.fish == F.rowid
-- WHERE C.spot == ... AND C.time == ...  -- filter
GROUP BY F.name;
```
