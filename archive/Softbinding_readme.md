
### Soft binding 

Now after having dealt with correcting small typos, it's time to deal with the soft binding. What if the data is badly represented. For that let's deal with the following example.

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


### Task

Query "Get the names and the amount of shares of all people owning a dog."

This would translate to the followng query:

SELECT s.name, s.shares
FROM shareowner s
JOIN animalowner a ON s.id = a.owner_id
WHERE a.category = 'dog';


However, after inspecting this, we should arrive at the necessary query with the soft bidning:

SELECT s.name, s.shares
FROM shareowner s
JOIN animalowner a ON s.id = a.owner_id
WHERE a.category IN ('dog', 'chien', 'perro');


