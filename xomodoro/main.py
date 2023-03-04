import importlib_resources
import rich_click as click
import time

from .Xomodoro import Xomodoro
from .XomodoroDisplay import XomodoroDisplay


@click.command()
@click.option(
    "--focus",
    "focus_total",
    type=float,
    default=25,
    help="how much time do you want to work during each session?",
)
@click.option(
    "--long-break",
    "long_break_total",
    type=float,
    default=25,
    help="how much time do you want to rest after a few work session?",
)
@click.option(
    "--short-break",
    "short_break_total",
    type=float,
    default=5,
    help="how much time do you want to rest between two work session?",
)
@click.option(
    "--focus-count",
    "focus_till_long_break",
    type=int,
    default=4,
    help="how many work session before a long rest?",
)
def main(focus_total, long_break_total, short_break_total, focus_till_long_break):
    xomodoro = Xomodoro(
        focus_total=focus_total,
        long_break_total=long_break_total,
        short_break_total=short_break_total,
        focus_till_long_break=focus_till_long_break,
    )

    with XomodoroDisplay(xomodoro) as display:
        xomodoro.start()

        while True:
            time.sleep(1)
            xomodoro.update()
