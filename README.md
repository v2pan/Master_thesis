
# Welcome to My Master's Thesis! 😊

Hello everyone, and welcome to my Master thesis!  Through this work, I aim to show my current progress in a nice manner, so that my progress can be tracked.

Let's get started! 👋🏻

---

In the **archive** folder one can observe old pipelines as well as their description.

## Execute for yourself
Everyone trying to execute this for yourself. What is needed is a Postgres database.
1. Restore the dump by executing: 
psql -h localhost -p 5433 -U postgres -d my_new_database
\i database.sql
2. Adjust the connection details in the database.py file in the Helpers folder.
3. Put a **api_key.txt** file inside of your repository. Get an API key for Gemini from  this [link](https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Faistudio.google.com%2Fapikey%3F_gl%3D1*7la1jo*_ga*MTk5NjU0NjI5Ni4xNzI4Mzk0NDI1*_ga_P1DBVKWT6V*MTczMzMzMDExNi40OS4wLjE3MzMzMzAxMTYuMC4wLjIwNzE4NDIzNzE.&followup=https%3A%2F%2Faistudio.google.com%2Fapikey%3F_gl%3D1*7la1jo*_ga*MTk5NjU0NjI5Ni4xNzI4Mzk0NDI1*_ga_P1DBVKWT6V*MTczMzMzMDExNi40OS4wLjE3MzMzMzAxMTYuMC4wLjIwNzE4NDIzNzE.&ifkv=AcMMx-cgPRy-Na5Uk6-Y0SPg2IKv4vGdWFZfpm_pHtAWq2oKvGhvMcHVvHyORe9A9j-8TUwVP1MU&passive=1209600&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S-132392570%3A1733330134082602&ddm=1).
4. Execute the **evaluation.py** file, evaluate the results by looking at the **all_metrics.txt** file. Everything is located in the **Evaluation folder**.

# State of the Work
For the current state of the work please refer to the following Overleaf link [Overleaf](https://www.overleaf.com/project/67ab7042590b1362441a6e85). 

</pre>
