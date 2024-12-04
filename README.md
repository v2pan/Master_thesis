
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
4. Execute the **evaluation.py** file, evaluate the results by looking at the **all_metrics-txt** file.

# SOTA

The SOTA for the 4th of December can be seen in the pipeline **row_calculus_pipeline** and for the join the **join_pipeline**. Also there exists the **combined_pipeline**, which is just a combination of the previously mentioned two pipelines. The pseudocode  for the **row_calculus_pipeline** is given here:


<pre>
query ← INPUT  // More explicit about getting the query<br>
tables ← get_relevant_tables(query) <br>
sql_query ← ask_LLM(f"Generate a SQL query based on {query} and {tables}")<br>
join_conditions, order ← extract_join_conditions_sqlparse(sql_query):<br>
   conditions={}<br>
   for token in sqlparse(sql_query):<br>
      if token is where.Clause and isinstance Comparison:<br>
         left_part or right_part ← Convert to SQL querying all values represented  <br>
         conditions.append(left_part, comparison_operator, clause, right_part)<br>
   return conditions<br>
query_results ← execute_queries_on_conditions(conditions):<br>
   for i in  conditions:<br>
      for l in i:<br>
         if l is SQL_query:<br>
            l ← query_database(l)<br>
semantic_list ← compare_semantics_in_list(query_results):<br>
   result_list ← []<br>
   for each sublist in query_results:<br>
      if sublist contains a string and a list OR:<br>
         temp_string, temp_list ← separate_string_and_list(sublist) <br>
         goal ← ask_gemini("Get semantic goal: " + sublist[-2])  # Leads to confusion -> not used currently<br>
         phrase ← ask_gemini("Get semantic phrase for: " + sublist[1]) <br>
         same_meaning_list ← []<br>
         prompt=""<br>
         for i in  temp_list<br>
            prompt +=  build_comparison_prompt(temp_string, i, phrase) <br>
         boolean_results ← gemini_json(prompt, response_type = list[boolean])<br>
         same_meaning_list.append(temp_list if boolean_result is true)<br>
         result_list.append(same_meaning_list, where_Clause)<br>
  return result_list<br>
query ← ask_LLM(f"Based on semantic list {semantic_list} and the intital query {sql_query} generate  a new query") <br>
result=query_database(query) <br>
return result<br>
   </pre>

The idea is that the LLM generates the phrase with which it queries the two values
by itself. Also some prompts were adjusted using 1-shot or 2-shot learning. 

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