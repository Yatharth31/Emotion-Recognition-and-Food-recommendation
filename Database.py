from deta import Deta

DETA_KEY = "c0uuvsyc_UCVewTxJTLw64KU7HbUm2vPp2jLf35F5"

deta = Deta(DETA_KEY)

db = deta.Base("Food_db")
db1 = deta.Base("User_info")


def insert_data(name, age, gender):
    return db1.put(
        {"key": name, "age": age, "gender": gender, })


def insert_feedback(comfort_food, comfort_mood):
    return db.put({"comfort_food": comfort_food, "comfort_mood": comfort_mood})
