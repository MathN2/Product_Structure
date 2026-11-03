from fastapi import FastAPI
from product_structure.controller.formula_controller import formula_router
from product_structure.controller.item_controller import item_router


app = FastAPI()

app.include_router(formula_router)
app.include_router(item_router)