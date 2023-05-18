from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider

from model import InfectionModel
from agent import InfectableAgent, State
from mesa.visualization.modules import CanvasGrid, ChartModule

NUM_CELLS = 10
CANVAS_SIZE_X = 500
CANVAS_SIZE_Y = 500

sim_params = {
    "num_agents": Slider(
        "Number of agents",
        value=50,  # default
        min_value=10,
        max_value=100,
        step=1,
    ),
    "infection_rate": Slider(
        "Infection rate",
        value=0.4,  # default
        min_value=0.1,
        max_value=1.0,
        step=0.1,
    ),
    "death_rate": Slider(
        "Death rate",
        value=0.02,  # default
        min_value=0.01,
        max_value=0.5,
        step=0.01,
    ),
    "start_infection_rate": Slider(
        "Start infection rate",
        value=0.05,  # default
        min_value=0.01,
        max_value=0.2,
        step=0.01,
    ),
    "width": NUM_CELLS,
    "height": NUM_CELLS,
}


def agent_display(agent: InfectableAgent) -> dict:
    """Display agent with infection state"""
    display = {"Shape": "circle", "Filled": "true", "Layer": 0}
    if agent.state is State.SUSCEPTIBLE:
        display["Color"] = "Blue"
        display["r"] = 0.5
    elif agent.state is State.INFECTED:
        display["Color"] = "Red"
        display["Layer"] = 3
        display["r"] = 0.2
    elif agent.state is State.RECOVERED:
        display["Color"] = "Green"
        display["Layer"] = 1
        display["r"] = 0.4
    elif agent.state is State.DECEASED:
        display["Color"] = "Black"
        display["Layer"] = 2
        display["r"] = 0.3
    return display


grid = CanvasGrid(agent_display, NUM_CELLS, NUM_CELLS, CANVAS_SIZE_X, CANVAS_SIZE_Y)

chart = ChartModule(
    [
        {"Label": "Susceptible", "Color": "Blue"},
        {"Label": "Infected", "Color": "Red"},
        {"Label": "Recovered", "Color": "Green"},
        {"Label": "Deceased", "Color": "Black"},
    ],
    canvas_height=300,
    data_collector_name="datacollector",
)

server = ModularServer(InfectionModel, [grid, chart], "Infection Model", sim_params)
server.port = 8521
server.launch()
