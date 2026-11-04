from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from product_structure.controller.formula_controller import (
    router as formula_router,
)
from product_structure.controller.item_controller import item_router
from product_structure.core.exceptions import (
    FormulaNotFoundError,
    ItemError,
    NodeError,
    TreeError,
)

INTERFACE_DIR = Path(__file__).resolve().parents[2] / "interface"

app = FastAPI(
    title="Product Structure API",
    description="API para gerenciamento de estruturas de produtos.",
    version="1.0.0",
)

@app.get("/")
def home():
    return FileResponse(INTERFACE_DIR / "index.html")

@app.get("/health")
def health():
    return {"mensagem": "Product Structure API está funcionando!"}

app.include_router(formula_router)
app.include_router(item_router)
app.mount("/css", StaticFiles(directory=INTERFACE_DIR / "css"), name="css")
app.mount("/js", StaticFiles(directory=INTERFACE_DIR / "js"), name="js")


@app.exception_handler(TreeError)
async def tree_error_handler(request: Request, exc: TreeError):
    status_code = 404 if isinstance(exc, FormulaNotFoundError) else 400

    return JSONResponse(
        status_code=status_code,
        content={"detail": str(exc)}
    )

@app.exception_handler(NodeError)
async def node_error_handler(request: Request, exc: NodeError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )

@app.exception_handler(ItemError)
async def item_error_handler(request: Request, exc: ItemError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )