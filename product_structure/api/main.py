from fastapi import FastAPI

from product_structure.controller.formula_controller import router as formula_router
from product_structure.controller.item_controller import item_router

app = FastAPI(
    title="Product Structure API",
    description="API para gerenciamento de estruturas de produtos.",
    version="1.0.0",
)

@app.get("/")
def home():
    return {"mensagem": "Product Structure API está funcionando!"}

app.include_router(formula_router)
# app.include_router(item_router)
