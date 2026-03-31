import random, csv


rows = []


for _ in range(50):
    height = random.randint(150, 200)
    weight = random.randint(40, 120)
    age = random.randint(18, 65)
    gender = random.choice(["male", "female"])
    
    rows.append([height, weight, age, gender])
    

with open("data/sample_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["height", "weight", "age", "gender"])
    writer.writerows(rows)