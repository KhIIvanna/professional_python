import csv
import random
from pathlib import Path

def generate_csv(filename: str = "data/cars_large.csv", rows: int = 100000):
    Path("data").mkdir(exist_ok=True)
    brands = ["BMW", "Audi", "Mercedes", "Toyota", "Ford", "Porsche", "Honda", "Volkswagen", "Nissan", "Volvo"]
    models = ["Model X", "Series 3", "A4", "Civic", "Mustang", "911", "Camry", "Golf", "Leaf", "XC90"]
    
    print(f"Генерація файлу {filename} на {rows} записів...")
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "brand", "model", "year", "price", "mileage"])
        for i in range(1, rows + 1):
            writer.writerow([
                i,
                random.choice(brands),
                random.choice(models),
                random.randint(2010, 2024),
                round(random.uniform(5000, 120000), 2),
                random.randint(1000, 200000)
            ])
    print("Генерацію завершено успішно!")

if __name__ == "__main__":
    generate_csv("data/cars_large.csv", 100000)