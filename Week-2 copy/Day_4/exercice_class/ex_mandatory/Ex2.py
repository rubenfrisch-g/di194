import json

sampleJson = """{
   "company":{
      "employee":{
         "name":"emma",
         "payable":{
            "salary":7000,
            "bonus":800
         }
      }
   }
}"""

data = json.loads(sampleJson)
salary = data ["company"]["employee"]["payable"]["salary"]
print(salary)
data ["company"]["employee"]["birth_date"] = "2007-08-06"
with open("empolyee.json", "w") as f:
    json.dump(data, f, indent=2)

with open ("employee.json", "r") as f:
    verified = json.load(f)

