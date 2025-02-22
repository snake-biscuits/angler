# ZZZ Angler Contest Tracker
```
Elpis Ultimate Angler Championship
 ===  Zenless Zone Zero Event  ===
2025/02/14 10:00 - 2025/03/10 03:59
```

## Uncaught
| Fish                  | Variants  |
| :-------------------- | :-------- |
| Crescent Grunter      | 3 + Shiny |
| Butterfly Fish        | 3 + Shiny |
| Humphead Fish         |     Shiny |
| Little Flying Octopus | 3         |
| Lionfish              |     Shiny |
| Manta Ray             | 3         |


## Goals
 * know where and when to fish
 * record catches (basic HTTP server w/ form? flask app?)
 * `.svg` map of the docks & island
 * track completion
 * reverse engineer drop rates from catch records
 * track bonus discoveries (rate dilution by location & ToD)


## Variants
all fish are 3 weight stars + 1 "shiny" star
catching a 3-star weight unlocks star 1 & 2
need to track this in our queries
otherwise we'll have false positives on what needs catching
catching a shiny won't unlock the base fish
though this doesn't matter for completion afaik, just OCD


## Junk
also part of the catch possibility table for each spot
NOT FISH (no shiny, 1 star, lower rates, one-time-only catches)
3x Story Bottles
1x Bangboo
1x Cactus Thing? (TODO: confirm)
Infinite Cans, Batteries & Message Bottles
Get a bonus for giving a battery to some Bangboo


## Queries
```bash
$ sqlite3
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
