
# Welcome to My Master's Thesis! 😊

Hello everyone, and welcome to my Master thesis!  Through this work, I aim to show my current progress in a nice manner, so that my progress can be tracked.

Let's get started! 👋🏻

---

In the **archive** folder one can observe old pipelines as well as their description.

## Execute for yourself
Everyone trying to execute this for yourself. What is needed is a Postgres database.
1. Restore the dump by executing: 
psql -h localhost -p 5433 -U postgres -d my_new_database
\i path_to_database.sql
2. Adjust the connection details in the database.py file
3. Put a **api_key.txt** file inside of your repository. Get an API key for Gemini from  this [link](https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Faistudio.google.com%2Fapikey%3F_gl%3D1*7la1jo*_ga*MTk5NjU0NjI5Ni4xNzI4Mzk0NDI1*_ga_P1DBVKWT6V*MTczMzMzMDExNi40OS4wLjE3MzMzMzAxMTYuMC4wLjIwNzE4NDIzNzE.&followup=https%3A%2F%2Faistudio.google.com%2Fapikey%3F_gl%3D1*7la1jo*_ga*MTk5NjU0NjI5Ni4xNzI4Mzk0NDI1*_ga_P1DBVKWT6V*MTczMzMzMDExNi40OS4wLjE3MzMzMzAxMTYuMC4wLjIwNzE4NDIzNzE.&ifkv=AcMMx-cgPRy-Na5Uk6-Y0SPg2IKv4vGdWFZfpm_pHtAWq2oKvGhvMcHVvHyORe9A9j-8TUwVP1MU&passive=1209600&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S-132392570%3A1733330134082602&ddm=1).
4. Execute the **evaluation.py** file, evaluate the results by looking at the **all_metrics.txt** file.

# SOTA

At the moment the modification of the query is done through a *CASE* and additional *WHERE* statements. The modification of the *WHERE* clause is performed by adding additional matches through the *OR* statement, in case any of them were missed by the initial binding. Similarly, for the modification of the *JOIN*, a *CASE* statement is added to modify the JOIN itself (e.g CASE 0 then 'zero'). 

The SOTA can be seen in the pipeline **row_calculus_pipeline** and for the join the **join_pipeline**. Also there exists the **combined_pipeline**, which is just a combination of the previously mentioned two pipelines. The methodology in natural language can be seen here:

1. Retrieve the relevant tables necessary for the predicate calculus query.
2. Use *schema level information* from the retrieved tables, like key constraints, data types and column names, to generate an initial SQL query.
3. Use a LLM to modify the initial SQL query to account for the residual noise using *data level information*, the data itself. The modification is to be achieved through a translation based approach. The **soft binding** step, central to the query pipeline, involves mapping semantically equivalent terms. It consists in binding one variable to another. Repassing Example ( WHERE animal.category = 'dog') it would be binding the instances of 'Hund', 'perro' and 'chien' to 'dog'. The possible modifications in the query might be:
    * Modifying problematic JOIN statements through the CASE statement
    * Modifying problematic WHERE statements through extensions with the OR statement
4. Execute the modified query against the database and return both the query and the resulting dataset to the user.


The pseudocode  for the **row_calculus_pipeline** is given here. It looks for resiudal noise in the *WHERE* clause and manually adjusts it. The procedure is:



<pre>
query ← INPUT  ' Get predicate calculus expression as input<br>
tables ← get_relevant_tables(query) ' Ask LLM, what are the relevant tables based on this predicate calculus query. Retrieve a list.<br>
sql_query ← ask_LLM(f"Generate a SQL query based on {query} and {tables}") # Generate initial SQL query using exclusively schema level information (e.g. column names, data types, primary/foreign key constraints)<br>

#Extract all the necesary WHERE comparisons (e.g. WHERE animal.category='dog') using a SQL parser and slight modification  <br>
conditions ← extract_where_conditions_sqlparse(sql_query):<br>
   conditions={} # List of all WHERE statements <br>
   for token in sqlparse(sql_query): # Iteration over all tokens in SQL querey<br>
      if token is where.Clause and isinstance Comparison: # If is part of WHERE clause e.g. 'WHERE animal.category='dog''<br>
         token.left OR token.right <- Convert_to_SQL(token.left or token.right)  
         \\ Convert binding variable ('dog') to SQL query: 'animal.category' -> 'SELECT category FROM animal;' can positioned at right or left side of clause<br>
         conditions.append(token.left, comparison_operator, clause, token.right) 
         \\ Append to conditions, structure: {('SELECT category FROM  animal', "=",'WHERE animal.category='dog'', 'dog'), (...)}<br>
   return conditions<br>

#Execute SQL queries inside conditions against the database
query_results ← execute_queries_on_conditions(conditions): <br>
   for i in  conditions: \\ For the whole conditions list {(...),(...),(...)}<br>
      for l in i: \\ Inside a comparison e.g. ('SELECT category FROM  animal', "=",'WHERE animal.category='dog'', 'dog') <br>
         if l is SQL_query: \\ Check if the element is a SQL query <br>
            l ← query_database(l) \\Substitute SQL query with result from database 
                                  e.g 'SELECT category FROM  animal;' ---> ('chien','perro','chat','dog') <br>

# Main Soft Binding Procedure, Checking for Comparison  
semantic_list ← compare_semantics_in_list(query_results): <br>
   result_list ← [] #Initialize empty list for storing the binding<br>
   for each sublist in query_results: 
   # Iterate for each sublist e.g. (('chien','perro','chat','dog'), "=",'WHERE animal.category='dog'', 'dog')<br>
      if sublist contains a string and a list OR: \\ Comparing a list e.g. ('chien','perro','chat','dog') with the fixed binding e.g. 'dog'<br>
          temp_string, temp_list ← separate_string_and_list(sublist) #Generate the temp_string e.g 'dog' and the temp_list e.g ('chien','perro','chat','dog')   <br>

          phrase ← ask_gemini("Get semantic phrase for: " + sublist[1])
            #Abstracts meaning of comparison operator in antural language 
            e.g "=" ---> "Has the same sematnic meaning as"<br>
          soft_binding_list ← [] #Construct a list of expression to be included<br>
          prompt="" #Construct a prompt to feed LLM<br>
          for i in  temp_list #Iterate over temp_list e.g.('chien','perro','chat','dog') <br>
            prompt +=  build_comparison_prompt(temp_string, i, phrase)
            #Construct final prompt e.g ["Does 'dog' and 'chien' have the same meaning?",
            "Does 'dog' and 'perro' have the same meaning?",
            "Does 'dog' and 'chat' have the same meaning?",
            "Does 'dog' and 'dog' have the same meaning?", ]<br>
         boolean_results ← gemini_json(prompt, response_type = list[boolean])
         #Return a boolean list e.g [True, True, False, True]<br>
         soft_binding_list.append(temp_list if boolean_result is true)
         #Appending ('chien','dog','perro') #Retrieve variables included in the soft binding<br>
         result_list.append(soft_binding_list, where_Clause)
         #Append ((('chien','dog','perro'), 'WHERE animal.category='dog''))for output <br>
  return result_list<br>

#Modified query construction
query ← ask_LLM(f"Based on semantic list {semantic_list} and the intital query {sql_query} generate  a new query")
#Construct the modified query based on the semantics list e.g "WHERE animal.category='dog'" --->
---> "WHERE animal.category='dog' OR animal.category='perro' OR animal.category='chien'"<br>
result=query_database(query) #Query database to get result of the modified query<br>
return result #Return the results of the query to the user<br>
</pre>



Also the **join_pipeline** was implemented, which accounts for examples where during the join procedure the binding is modified using the CASE statement. The logic is pretty similar to that of the **row_calculus_pipeline** and a seperate pseudocode is not listed. The JOIN pipeline 
can now also handle multiple JOINs and distingusih in which case to use a CASE statement at all.


# Results 

Using the examples pointed out in **Testset.md** one can see the examples used is **evaluation.py**. The metrics are written to **all_metrics.txt** THe most current results are:

<pre>
---- Individual Metrics ---
Calculus ∃id ∃name ∃patients_pd (doctors(id, name, patients_pd) ∧ patients_pd < 12):
  Accuracy: 0.4000
  Precision: 0.4000
  Recall: 1.0000
  F1-score: 0.5714
Calculus ∃id ∃patients_pd (doctors(id, 'Peter', patients_pd) ∧ patients_pd < 12):
  Accuracy: 0.5000
  Precision: 0.5000
  Recall: 1.0000
  F1-score: 0.6667
Calculus ∃id ∃shares ∃name (shareowner1row(id, name, shares) ∧ animalowner1row(id, _, 'dog')):
  Accuracy: 1.0000
  Precision: 1.0000
  Recall: 1.0000
  F1-score: 1.0000
Calculus ∃id ∃shares ∃name (shareowner(id, name, shares) ∧ animalowner(id, _, 'dog')):
  Accuracy: 1.0000
  Precision: 1.0000
  Recall: 1.0000
  F1-score: 1.0000
Calculus ∃id ∃shares ∃name(shareowner(id, name, shares) ∧ ¬animalowner(id, _, 'dog')):
  Accuracy: 0.3333
  Precision: 0.3333
  Recall: 1.0000
  F1-score: 0.5000
Calculus ∃x ∃y ∃z (children_table(x, y) ∧ fathers(x, z)):
  Accuracy: 0.2000
  Precision: 0.3333
  Recall: 0.3333
  F1-score: 0.3333
Calculus ∃id (children_table(id, ) ∧ fathers(id, _) ∧ mothers(id, _) ):
  Accuracy: 1.0000
  Precision: 1.0000
  Recall: 1.0000
  F1-score: 1.0000
Calculus ∃id (tennis_players(id, _, 'January') ∧ tournaments(id, name, price_money)):
  Accuracy: 1.0000
  Precision: 1.0000
  Recall: 1.0000
  F1-score: 1.0000
Calculus ∃m ∃f ∃i (influencers(m, f) ∧ f > 500 ∧ followers(i, m, z)):
  Accuracy: 0.7500
  Precision: 1.0000
  Recall: 0.7500
  F1-score: 0.8571
Calculus ∃id (children_table(id, >1) ∧ fathers(id, _)):
  Accuracy: 1.0000
  Precision: 1.0000
  Recall: 1.0000
  F1-score: 1.0000
Calculus ARTISTS(a,,), ALBUMS(,a,"Reputation",2017),SONGS(,a2,song_name,),ALBUMS(a2,a,):
  Accuracy: 1.0000
  Precision: 1.0000
  Recall: 1.0000
  F1-score: 1.0000
Calculus ∃d weather(d, city, temperature, rainfall) ∧ website_visits(d, page, visits):
  Accuracy: 0.0000
  Precision: 0.0000
  Recall: 0.0000
  F1-score: 0.0000
Calculus ∃d weather(d, city, temperature, rainfall) ∧ website_visits(d, page, visits):
  Accuracy: 0.0000
  Precision: 0.0000
  Recall: 0.0000
  F1-score: 0.0000

--- Overall Metrics ---
Mean Accuracy: 0.6295
Mean Precision: 0.6590
Mean Recall: 0.7756
Mean F1-score: 0.6868

</pre>