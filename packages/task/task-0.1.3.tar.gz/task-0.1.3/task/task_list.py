import click
import datetime
from dateutil.relativedelta import relativedelta
from tabulate import tabulate
from click_default_group import DefaultGroup

import utils


@click.group(
    name='ls',
    cls=DefaultGroup,
    default='list-tasks',
    default_if_no_args=True

)
def main():
    """List tasks."""


def get_date_age(task_date: str) -> str:
    """Get age of date."""
    task_date = datetime.datetime.strptime(task_date, '%Y-%m-%d %H:%M:%S')
    now = datetime.datetime.now()
    age = relativedelta(now, task_date)

    if age.years != 0:
        age = age.years
        age_type = "year"
    elif age.months != 0:
        age = age.months
        age_type = "month"
    elif age.days != 0:
        age = age.days
        age_type = "day"
    elif age.hours != 0:
        age = age.hours
        age_type = "hour"
    elif age.minutes != 0:
        age = age.minutes
        age_type = "minute"
    else:
        age = age.seconds
        age_type = "second"
    return f"{age} {age_type + 's' if age > 1 else age_type}"


def prettify_header(header) -> tuple:
    """Pretty header."""
    new_header = list()
    for data in header:
        new_header.append(f"\x1b[4m{data}\x1b[0m")
    return new_header


def prettify_tasks(tasks):
    """Set black background
    and red tasks when needed.
    """
    cnt = 0
    new_tasks = list()
    for task in tasks:
        new_task = list()
        for row in task:
            if (cnt % 2) != 0:
                new_task.append(f'\x1b[40m{row}')
            else:
                new_task.append(f'{row}')
        age = get_date_age(row)
        new_task[-1] = f"{age}\x1b[0m"
        cnt += 1
        new_tasks.append(new_task)
    return new_tasks


@main.command()
def list_tasks():
    """List tasks."""
    if utils.does_db_exist()[0] is False:
        utils.create_db()
        return 1

    header = ("ID", "Project", "Task", "Urgency", "Due", "Age")
    header = prettify_header(header)
    tasks = utils.list_all_tasks()
    pretty_tasks = prettify_tasks(tasks)
    print(tabulate(pretty_tasks, headers=header, tablefmt="plain"))
