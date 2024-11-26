# Shareowner and Animalowner examples


### Table 1: shareowner

|id| name          | shares   | 
|----|-------------|----------|
|1   | Pierre       | 20      |
|2   | Vladi         | 10     |
|3   | Diego       | 15      |
|4   | Marcel         | 11     |

### Table 2: animalowner

| animalname    | category   |owner_id|
|---------------|------------|------  |
| bill          | chien      |1       |
| diego         | chat       |2       |
|chris          | dog        | 3      |
| juan          | perro       | 4      |

Different language example<br> 
**calculus** :{name, shares | ∃id (SHAREOWNER1ROW(id, name, shares) ∧ ANIMALOWNER1ROW(id , _, 'dog'))}''' <br>


**Result**:[('Pierre\n', 20), ('Diego', 15),('Marcel', 11)] <br>

Nengation and different langauge example<br>
**calculus** : {name, shares | ∃id (SHAREOWNER(id, name, shares) ∧ ¬ANIMALOWNER(id, _, 'dog'))} <br>


**Result**:[('Vladi', 10)] <br>

# Doctor example

### Table 3: doctors

| id | name       | patients_pd |
|----|------------|----------|
| 2  | Giovanni | 11     |
| 3  | Hans     | fourty |
| 4  | Lukas    | 44     |
| 1  | Peter    | ten    |
| 5  | Dr. Smith| 150    |

Doctors example with inequality<br>
**calculus=** {id, name, patients_pd | doctors(id, name, patients_pd) ∧ patients_pd < 12}<br>
**Result**  [(1, 'Peter', 'ten'), (2, 'Giovanni','11')]<br>

Doctors example with inequality and two WHERE clauses<br>
**calculus** {id, name, patients_pd | doctors(id, 'Peter', patients_pd) ∧ patients_pd < 12}<br>
**Result**  [(1, 'Peter', 'ten')] <br>




# Taylor Swift Example

### Table 4: artists 

| id | name           | language |
|----|-----------------|----------|
| 1  | "Taylor Swift"  | "English" |
| 2  | "Reputation Artist" | "English" |


### Table 4: albums

| id | artist_id | album_name  | release_year |
|----|------------|-------------|---------------|
| 1  | 1          | "Reputation" | 2017          |
| 2  | 2          | "Reputation" | 2017          |


### Table 5: songs

| id | album_id | song_name      | duration |
|----|-----------|-----------------|----------|
| 1  | 1         | "Delicate"      | "3:52"    |
| 2  | 2         | "New Year's Day" | "3:55"    |

Initial example provided<br>
 **calculus=** ARTISTS(a,_,_), ALBUMS(_,a,"Reputation",2017),SONGS(_,a2,song_name,_),ALBUMS(a2,a,_)
 row_calculus_pipeline(calculus, ['artists', 'albums', 'songs']) <br>
 **Result** [('Taylor Swift',), ('Reputation Artist',)] <br>


# Example Time and Tennis_Players

### Table 6: tennis_players

|id| name          | born   | 
|----|-------------|----------|
|1   | Juan       | 20.02.2003      |
|2   | Paul        | 18.04.1968   |
|3   | Xi       | January 1986 |
|4   | Michael       |    18.01.1997  |

### Table 7: tournaments

| winner_id    | name   |price_money in million|
|---------------|------------|------  |
| 3          | Berlin Open     |4      |
| 3         | Warsaw Open       | 3       |
|2        | Jakarta Open        | 1.5      |
| 3          | Osaka Open       | 0.5     |

Date mismatch, Tournaments won by player born in January
**Calculus** {  name, price_money |  tennis_players(id, _, 'January') ∧ tournaments(id, name, price_money) }

**Result** [[( 'Paul', 1.5), ('Xi', 7)]] <br>


# Example Influencers

### Table 8: influencers

|media_name|  clicks  | 
|----------|---------    |
|makeuptutorial   | 1000 thousand|
| outsideguy   | 50|
|surviver1000   | 1 million|
| princess   | thousand  |

### Table 9: followers

|  id  | following   | adult |
|---------------|------------|------  |
| 1          | surviver1000  | True   |
| 3         | makeuptutorial  | False |
|2        | surviver1000       | True |
| 3          | princess       | True  |


Clicks is written in a completely different format.<br>

**Calculus** {  media_name |  influencers(media_name, > 500) ∧ followers(id, media_name, _) } <br>

**Result** [[('makeuptutorial'), ('surviver1000')]] <br>


# Example Join


### Table 8: children_table

|id|  children  | 
|----------|----|
|0        | 4    |
| 1         | 1|
| 2         | 1 |
| 3         | 2  |

### Table 9: fathers

|  id  | name   |
|---------------|------------|
| zero          | Gerhard |
| one         | Joachim |
| four        | Simon |
| two          | Dieter  |


Check whether the new Join works <br>

**Calculus** ∃id (children_table(id, _) ∧ fathers(id, _)) <br> 
=> Resulting  query: 
SELECT children_table.id, children_table.children, fathers.name FROM children_table INNER JOIN  fathers ON children_table.id = CASE fathers.id
                   	WHEN 'zero' THEN 0
                        WHEN 'one' THEN 1
                        WHEN 'two' THEN 2
                        WHEN 'four' THEN 4
                        ELSE NULL
                    END;<br>

**Result** [[('makeuptutorial'), ('surviver1000')]] <br>