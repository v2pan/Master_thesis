 

import json
with open("saved_json/boolean_metrics_ollama_cot.json", "r") as f:
        cot=json.load (f)
with open("saved_json/boolean_metrics_ollama_direct.json", "r") as f:
        direct=json.load (f)

complete={}
for key in cot:
    complete[key]={}

    complete[key]["CoT"]=cot[key]["CoT"]
    complete[key]["direct"]=direct[key]["direct"]
    # complete[key]=cot[key]
    # complete[key]=direct[key]

with open("saved_json/boolean_metrics_ollama_complete.json", "w") as f:
    json.dump(complete, f, indent=4) 