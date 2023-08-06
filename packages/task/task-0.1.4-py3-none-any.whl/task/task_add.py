import click
from datetime import datetime
from click_default_group import DefaultGroup

from task import utils


@click.group(
    name='add',
    cls=DefaultGroup,
    default='new-task',
    default_if_no_args=True
)
def main():
    """Add task"""


def format_current_time() -> str:
    date = str(datetime.now())
    return date.split('.')[0]


@main.command()
@click.argument('task', type=click.STRING)
@click.option('-p', '--project', help="specyfiy project")
@click.option('-u', '--urgency', help="urgency")
@click.option('-d', '--due', help="due date")
def new_task(task: str, project: str = None, urgency: int = 0, due: str = None):
    """Add task to database."""
    if utils.does_db_exist()[0] is False:
        utils.create_db()
    else:
        print("don't create db")

    task_data = dict()
    task_data['task'] = task
    task_data['project'] = project
    task_data['urgency'] = urgency
    task_data['due'] = due
    task_data['datetime'] = format_current_time()
    utils.insert_to_db(task_data)
