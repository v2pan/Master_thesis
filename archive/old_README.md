### Soft binding 

Now after having dealt with correcting small typos, it's time to deal with the soft binding. What if teh data is badly represented. For that let's deal with the following example.

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


### Soft binding 

Now after having dealt with correcting small typos, it's time to deal with the soft binding. What if th data is badly represented. For that let's deal with the following example.


Okay, so having tried that the first_pipeline architecture, also occasionally works recognzing that dog, is also meant by the expression "chien" and "chat".

How could this be improved? Maybe through embedding and similarity measures. 

## Text approach. What if we try to write the data as text, possibly writing it to an index. And then retreiving when being asked the question.

First consider this very simple text_pipeline implemented in th the function **text_pipeline** in the **softbinding.py** file. Wit the prompt "Convert the following database entries into a descriptive text." the content is written to a text file. Then the LLM is given all this information as context and is supposed to answer the query with that. 
![Alt text for the image](images/text_pipeline.png).

However, the LLM seems to have problems linking the two databases based on the id. Even when explicitly mentioning the linkage it doesn't seem to work. Hm, seems like the approach is not going anywhere. Try another. Interestingly though, the first_pipe doesn work and gives out the correct answer to this query.

### Task

“Find all songs by the artist who released the album Reputation in 2017.” 

### Database Records

#### ARTISTS
| id | name             | language |
|----|-------------------|----------|
| 1  | Taylor Swift     | English  |
| 2  | Reputation Artist| English  |

#### ALBUMS
| id | artist_id | album_name | release_year |
|----|-----------|------------|--------------|
| 1  | 1         | Reputation | 2017         |
| 2  | 2         | Reputation | 2017         |

#### SONGS
| id | album_id | song_name      | duration |
|----|----------|----------------|----------|
| 1  | 1        | Delicate       | 3:52     |
| 2  | 2        | New Year’s Day | 3:55     |

### Result

First of all, the text pipelien is used again. It produces decent result understanding not one but multiple artists are made. A possible output was the following:

Song 1 (ID 1): Delicate, with a duration of 3:52, is from the album "Reputation" (Album ID 1) by Taylor Swift (Artist ID 1) who sings in English. This album was released in 2017.
ong 2 (ID 2): New Year's Day, with a duration of 3:55, is from the album "Reputation" (Album ID 2) by Reputation Artist (Artist ID 2) who also sings in English.  This album was also released in 2017. 

However, the idea occured whether logical mistakes in the query can be understood. In our case this would be that there are multiple artists who released the same album.

The idea of adding a text_logic_pipeline didn't work. The LLM mostly tries to give me the procedure.

![Alt text for the image](images/text_logic_pipeline.png).

Having adjusted the pipeline, especially providing exemplary input and outputs, the results produced are quite decent. (Reiteration of the result is not included).
 However, the LLM sometimes didn't produce any result due to copyrights issues with Taylor Swift and often added the rest of the songs published by Taylor Swift





| artist_name      | language | song_name      | duration   | album_id |
|-------------------|----------|-----------------|-------------|----------|
| Reputation Artist | English   | New Year’s Day | 3:55       | 2        |
| Taylor Swift       | English   | Delicate       | 3:52       | 1        | 


Another, proposal is the **log_sql_pipeline**. The query is modified to force the LLM to gieve out a specific structuin. Based on the tables it creates a SQL query and based on the query it outlines instructions in natural language on how to perceed. Based on these instructions the content is given and the
LLM gives out an answer. The pipeline is shown here

![Alt text for the image](images/logic_sql.png).

This pipeline showed smaller risk of the LLM infering different songs from the album, as in the text_logic_pipeline. It however often inferred that Taylor Swift is the reputation artist.

"The album Reputation was released by **Taylor Swift** in 2017. The artist **Taylor Swift** has released the following songs:

* Delicate
* New Year's Day 
"