import typer
import uvicorn
from dotenv import load_dotenv

from runner.setup import init_app

app = typer.Typer()
# @app.command("list", help="List Items")
# def app_list() -> None:
#     print("Printing Items")
#     displayer: ItemsDisplayer = ItemsDisplayer(repository.get_all_items())
#     displayer.display_items()
#
#
# @app.command("report", cls=None)
# def app_report() -> None:
#     simulator.make_final_report()
#
#
# @app.command("simulate", cls=None)
# def app_simulate() -> None:
#     simulator.simulate()


@app.command()
def run(host: str = "localhost", port: int = 8000) -> None:
    load_dotenv()
    uvicorn.run(host=host, port=port, app=init_app())
