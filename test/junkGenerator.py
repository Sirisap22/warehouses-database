import json
import requests as rq
import random as rd

tcasRound = ["1" for i in range(2000)]+["2" for i in range(2000)]+["3" for i in range(2000)]+["4" for i in range(2000)]+["5" for i in range(2000)]
for i in range(10000):
    data = {
        "name" : f"JackD{i}",
        "age" : rd.randint(18,40),
        "years" : rd.randint(1,4)
    }
    province = ["Saraburi", "Bangkok", "Chiang_mai","Krabee","NakhonNayok","Surattani","Singburi","Lobburi"]
    gender = ["Male","Female"]
    faculty = ["Engineer","Science","IT","Medical","Business","Architect"]

    rq.post(f"http://127.0.0.1:8000/student/tag/{rd.choices(province)[0]}-{rd.choices(gender)[0]}-{rd.choices(faculty)[0]}-{tcasRound.pop()}", json.dumps(data))