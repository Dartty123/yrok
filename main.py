from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn 

app = FastAPI()

class Dish(BaseModel):
    id: int
    name: str
    ingredients: list[str]
    instructions: str
    price: float

dishes = [{
    "id": 1,
    "name": "baked potato",
    "ingridients": "do not know", 
    "instructions": "do not know",
    "price": 2.5
    }]

@app.get("/dishes/")
def get_dishes():
    return dishes

@app.get("/dishes/{dish_id}")
def get_dish(dish_id:int):
    for dish in dishes:
        if dish["id"] == dish_id:
            return dish
    return {"message": "Страву не знайдено"}

    
@app.post("/dishes/")
def create_dish(dish:Dish):
    if any(existing_dish["id"] == dish.id for existing_dish in dishes):
        return {"message": "Страва з таким ID вже існує"}
    new_dish = dish.dict()
    dishes.append(new_dish)
    return {"message": "Страву успішно додано"}


@app.put("/dishes/{dish_id}")
def update_dish(dish_id:int, dish:Dish):
    for idx, existing_dish in enumerate(dishes):
        if existing_dish["id"] == dish_id:
            dishes[idx] = {"id": dish_id, "name": dish.name, "ingredients": dish.ingredients, "instructions": dish.instructions}
            return {"message": "Страву успішно оновлено"}
        return {"message": "Страву не знайдено"}         


@app.delete("/dishes/{dish_id}")
def delete_dish(dish_id:int):
    for idx, populated_dish in enumerate(dishes):
        if populated_dish["id"] == dish_id:
            dishes.pop(idx)
            return {"message": "Страву успішно видалено"}
        return {"message": "НЕ знайдено"}

if __name__ == "__main__":
    uvicorn.run(app)