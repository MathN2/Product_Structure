from product_structure.api.main import app


def test_item_crud_routes_are_exposed():
    paths = app.openapi()["paths"]

    assert {"get", "post"} <= paths["/itens/"].keys()
    assert {"get", "patch", "delete"} <= paths["/itens/{item_id}"].keys()


def test_formula_supports_production_quantity_and_component_update():
    paths = app.openapi()["paths"]

    assert "get" in paths["/formulas/{formula_id}"]
    parameters = paths["/formulas/{formula_id}"]["get"]["parameters"]
    quantity = next(
        parameter for parameter in parameters
        if parameter["name"] == "quantidade_producao"
    )
    assert quantity["schema"]["minimum"] == 1
    assert "patch" in paths["/formulas/{formula_id}/nodes/{node_id}"]
