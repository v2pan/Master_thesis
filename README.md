
# Welcome to My Master Thesis! 😊

Hello everyone, and welcome to my first interactions with my Master thesis!  Through this work, I aim to show my current progress in a nice manner, so that my progress can be tracked.

Let's get started! 👋🏻

---


## Row-wise playground


Now tet's try to start with two tables, with only one row per table inside. Thus, the procedure has to be developed by row rather than by table.


### Table 1: shareowner1row

|id| name          | shares   | 
|----|-------------|----------|
|1   | Pierre       | 20      |


### Table 2: animalowner1row

| animalname    | category   |owner_id|
|---------------|------------|------  |
| bill          | chien      |1       |

The query given is still the same:
"Give me the names and the shares of all people owning a dog.", which written in predicate calculus would be:
{name, shares | ∃id (SHAREOWNER1ROW(id, name, shares) ∧ ANIMALOWNER1ROW(id , _, 'dog'))}



The results for the 18th November can be seen in the pipeline **row_calculus_pipeline**. The pipeline is not so easy to overlook, so here the idea in pseudocde:

## Pseudocde

GENERATE context
GEMINII GENERATE initial SQL query based on context (!Important to not renamne the tables and not not have subqueries)
EXTRACT_where_conditions_sqlparse
PARSE the query using the library sqlparse
GENERATE list conditions using a where clause like for example [['animalowner1row.category;', "(2, <Comparison '=' at 0x72DFE159C7C0>)", 'dog']]
Substitute all reference like 'animalowner1row.category;' to SELECT queries

execute_queries_on_conditions()
Run those only those rewritten statements on the database and substitute them
compare_semantics_in_list() (So far only works with one string and another list(0 to many Strings))
Retrieves the originally queried String and last
Iteration over every combination
GEMINI: Does '{a}' and '{b}' have the same semantic meaning?"
If YES: same_meaning_list.append
GENERATE SQL query with same_meaning_list
EXTRACT sql_query
query_database(sql_query)

'''
1. **Gather Context:**
   - Obtain schema information (table names, column names, data types, constraints) for relevant tables.  Store this as structured data (e.g., a dictionary or list of dictionaries).

2. **Initial SQL Generation:**
   - Use a large language model (LLM) like Gemini to translate the input row calculus query into an initial SQL query.
   - Constraints: The LLM must not rename tables, and the generated SQL should avoid subqueries, using JOINs instead.

3. **WHERE Clause Extraction and Preprocessing:**
   - Parse the initial SQL query using `sqlparse`.
   - Extract the WHERE clause.
   - Identify conditions within the WHERE clause.  Represent each condition as a list: `[left_operand, operator, right_operand]`.
   - For each condition, if the left operand or the right operand  or the ' references a column (e.g., `table.column`), replace it with a corresponding `SELECT` statement: `SELECT column FROM table`.

4. **Database Query Execution:**
   - Execute the modified `SELECT` statements against the database to obtain the actual values.
   - Replace the original `left_operand` or `left_operand` placeholders with the query results in the `conditions` list.

5. **Semantic Comparison:**
   - For each condition in the list:
     - Compare the semantic meaning of the `left_operand` value (obtained from the database query in step 4) and the `right_operand` or `left_operand` using the LLM.
     - If the LLM determines they are semantically equivalent, add them to the list.

6. **SQL Query Optimization (based on semantic comparisons):**
   - If semantically equivalent conditions exist, adjust WHERE clause of the SQL query accordingly. This involves merging conditions found in the previous step. 

7. **Final Query Execution:**
   - Execute the optimized SQL query against the database.
   - Return the results.

The results with one row, where quite good, so I extended it to multiple

I have performed a short evaluation with multiple rows, I used this example:

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

Witht the query:

{name, shares | ∃id (SHAREOWNER1ROW(id, name, shares) ∧ ANIMALOWNER1ROW(id , _, 'dog'))}

The result should be:
[('Pierre\n', 20), ('Diego', 15), ('Marcel', 11)], as **dog** should have the same semantic meaning as **(chien, perro )**

Out of 3 times the desired result was returned 3 times 🥳

Now of course, there are some limitations

- so far only where clause
- dependency to have clear structure without subclauses and without renaming
- not covered case where there is not a '='
- How much tokens are being used? If too frequently, quota exhaustion

Still, a first step forward 😊