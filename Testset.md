Here one can find the examples used in the **evluation.py** file listed. These examples
try to cover different types of semantic missmatches like different formats, different spelling,
numbers written as text and so on.


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
**calculus** : ∃id ∃shares ∃name (shareowner(id, name, shares) ∧ animalowner(id, _, 'dog')) <br>


**Result**: {(3, 'Diego', 15, 3, 'chris', 'dog'), (4, 'Marcel', 11, 4, 'juan', 'perro'), (1, 'Pierre', 20, 1, 'bill', 'chien')} <br>

Nengation and different langauge example<br>
**calculus** : ∃id ∃shares ∃name(shareowner(id, name, shares) ∧ ¬animalowner(id, _, 'dog')) <br>


**Result**:{(2, 'Vladi', 10, 2, 'diego', 'chat')} <br>

**calculus**: ∃id ∃shares ∃name (shareowner1row(id, name, shares) ∧ animalowner1row(id, _, 'dog')),
**Result**: {(1, 'Pierre', 20, 1, 'bill', 'chien')},

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
**calculus=** ∃id ∃name ∃patients_pd (doctors(id, name, patients_pd) ∧ patients_pd < 12) <br>
**Result**  {(2, 'Giovanni', '11'), (1, 'Peter', 'ten')} <br>

Doctors example with inequality and two WHERE clauses<br>
**calculus** ∃id ∃patients_pd (doctors(id, 'Peter', patients_pd) ∧ patients_pd < 12) <br>
**Result** {(1, 'Peter', 'ten')} <br>






# Taylor Swift Example (not used, provided by supervision)

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
| 4          | Berlin Open     |4      |
| 3         | Warsaw Open       | 3       |
|2        | Jakarta Open        | 1.5      |
| 3          | Osaka Open       | 0.5     |

Date mismatch, Tournaments won by player born in January
**Calculus** ∃id (tennis_players(id, _, 'January') ∧ tournaments(id, name, price_money))

**Result** {(4, 'Michael', '18.01.1997', 4, 'Berlin Open', 4.0), (3, 'Xi', 'January 1986', 3, 'Warsaw Open', 3.0), (3, 'Xi', 'January 1986', 3, 'Osaka Open', 0.5)}<br>


# Example Influencers

### Table 8: influencers

|media_name|  clicks  | 
|----------|---------    |
|makeuptutorial   | 1000 thousand|
| outsideguy   | 50|
|surviver1000   | 1 million|
| princess   | one thousand  |

### Table 9: followers

|  id  | following   | adult |
|---------------|------------|------  |
| 1          | surviver1000  | True   |
| 3         | makeuptutorial  | False |
|2        | surviver1000       | True |
| 3          | princess       | True  |


Clicks is written in a completely different format.<br>

**Calculus** ∃m ∃f ∃i (influencers(m, f) ∧ f > 500 ∧ followers(i, m, z)) <br>

**Result** {('surviver1000', '1 million', 1, 'surviver1000', True), ('makeuptutorial', '1000 thousand', 3, 'makeuptutorial', False), ('surviver1000', '1 million', 2, 'surviver1000', True), ('princess', 'one thousand', 3, 'princess', True)} <br>


# Example Join


### Table 8: children_table

|id|  children  | 
|----------|----|
|0        | 4    |
| 1         | 1|
| 2         | many |
| 3         | 2  |

### Table 9: fathers

|  id  | name   |
|---------------|------------|
| zero          | Gerhard |
| one         | Joachim |
| four        | Simon |
| two          | Dieter  |

### Table 10: mothers

|  id  | name   |
|---------------|------------|
| 1          | Julia |
| 2        | Petra |
| 3        | Claudia |
| 4          | Lena  |




Check whether the new Join works <br>

**Calculus** ∃id (children_table(id, _) ∧ fathers(id, _)) <br>

=> Resulting  query should be: <br>
SELECT children_table.id, children_table.children, fathers.name <br>
FROM children_table INNER JOIN  fathers ON children_table.id = CASE fathers.id <br>
                   	WHEN 'zero' THEN 0 <br>
                        WHEN 'one' THEN 1 <br>
                        WHEN 'two' THEN 2 <br>
                        WHEN 'four' THEN 4 <br>
                        ELSE NULL<br>
                    END;<br>

**Result** {(0, 4, 'zero', 'Gerhard'), (1, 1, 'one', 'Joachim'), (2, 'many', 'two', 'Dieter')} <br>

**Calculus**: ∃id (children_table(id, >1) ∧ fathers(id, _)) (Use of combined pipelines)<br>
**Result**: {(0, '4', 'zero', 'Gerhard'), (2, 'many', 'two', 'Dieter')} <br>

Multiple Join example, !!!!!EXPERIMENTAL SO FAR!!!!! <br>
**Calculus**: ∃id (children_table(id, ) ∧ fathers(id, _) ∧ mothers(id, _) ) (Use of combined pipelines)<br>
**Result**: {(0, '4', 'zero', 'Gerhard'), (2, 'many', 'two', 'Dieter')} <br>