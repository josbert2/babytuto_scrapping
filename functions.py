
from alive_progress import alive_bar, config_handler
from rich import print
from rich.console import Console
import time

def taskStatus(task='Default task', limit=20):
   console = Console()
   tasks = [f"Run: {task}" for n in range(0, 1)]
   print()
   with console.status("[bold green]Working on tasks...") as status:
      while tasks:
         task = tasks.pop(0)
         time.sleep(3)
         console.log(f"{task} complete")
   
   # break line



def progressBar(limit ):
   with alive_bar(limit, length=40) as bar:
      for i in range(limit):
         time.sleep(0.15)
         bar()