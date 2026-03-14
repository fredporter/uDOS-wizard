from fastapi import FastAPI
import uvicorn

from .assist import route_assist
from .budget import BudgetPolicy
from .mcp_registry import MCPRegistry
from .beacon import BeaconNode
from .orchestration import OrchestrationRegistry

app = FastAPI(title="uDOS Wizard Kernel")

budget = BudgetPolicy()
registry = MCPRegistry()
beacon = BeaconNode()
orchestration = OrchestrationRegistry()

@app.get("/")
def root():
    return {"service": "wizard", "status": "ok"}

@app.get("/assist")
def assist(task: str = "demo", mode: str = "auto"):
    return route_assist(task, mode)

@app.get("/budget")
def get_budget():
    return budget.get()

@app.get("/mcp/tools")
def list_tools():
    return registry.list_tools()

@app.get("/orchestration/status")
def orchestration_status():
    return orchestration.status()

@app.get("/orchestration/dispatch")
def orchestration_dispatch(task: str = "demo", mode: str = "auto", surface: str = "assist"):
    return orchestration.route(task=task, mode=mode, surface=surface)

@app.get("/orchestration/workflow-plan")
def orchestration_workflow_plan(objective: str = "shared-remote-flow", mode: str = "auto"):
    return orchestration.workflow_plan(objective=objective, mode=mode)

@app.get("/beacon/announce")
def beacon_announce():
    return beacon.announce()

def run():
    uvicorn.run(app, host="0.0.0.0", port=8787)
