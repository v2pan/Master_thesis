
However, for more rows this procedure seems to have problems as it can't isolate each bidning accurately and sometimes the soft bidning is done at the wrong place.

Also it was tried to implement such a function directly in the Python extension for
SQL plpython3u. However, it doesnÄt have access to an API like for example a LLM, so 
this unfortunately can't be used.

CREATE OR REPLACE FUNCTION normalize_category(category TEXT)
RETURNS TEXT AS $$
# Define a set of terms that mean "dog" in different languages
dog_terms = {'dog', 'chien', 'perro', 'Hund', 'cane'}
if category in dog_terms:
    return 'dog'
return category
$$ LANGUAGE plpython3u;

SELECT T1.name, T1.shares
FROM shareowner1row AS T1
INNER JOIN animalowner1row AS T2 ON T1.id = T2.owner_id
WHERE normalize_category(T2.category) = 'dog';