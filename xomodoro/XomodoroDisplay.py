import importlib_resources
import notifypy
import rich.align
import rich.console
import rich.layout
import rich.live
import rich.panel
import rich.progress_bar
import rich.table
import rich.text

from xomodoro import Xomodoro

from .XomodoroState import XomodoroState


class XomodoroDisplay(rich.live.Live):
    # constructor **************************************************************
    def __init__(self, xomodoro):
        self.__xomodoro = xomodoro

        resources = importlib_resources.files("xomodoro") / "resources"
        icon_path = resources / "icon.ico"
        alert_default_path = resources / "alert_default.wav"
        alert_success_path = resources / "alert_success.wav"

        self.__previous_state = xomodoro.state

        self.__state_to_alert_path = {
            XomodoroState.focus: alert_default_path,
            XomodoroState.long_break: alert_success_path,
            XomodoroState.short_break: alert_default_path,
            XomodoroState.stopped: alert_default_path,
        }

        self.__notification = notifypy.Notify()
        self.__notification.title = "Xomodoro"
        self.__notification.icon = icon_path

        self.__notify()

        # create the renderable
        root_layout = rich.layout.Layout(name="root")
        root_layout.split(
            rich.layout.Layout(name="title", size=10), rich.layout.Layout(name="body")
        )
        root_layout["body"].split(
            rich.layout.Layout(name="state", size=20),
            rich.layout.Layout(name="progress"),
        )

        self.__root_layout = root_layout

        title = rich.text.Text(
            "                            _                  \n"
            "                           | |                 \n"
            " _   _ ___  ____   ___   __| | ___   ____ ___  \n"
            "( \ / ) _ \|    \ / _ \ / _  |/ _ \ / ___) _ \ \n"
            " ) X ( |_| | | | | |_| ( (_| | |_| | |  | |_| |\n"
            "(_/ \_)___/|_|_|_|\___/ \____|\___/|_|   \___/\n",
            style="magenta",
        )
        root_layout["title"].update(rich.align.Align.center(title, vertical="middle"))

        self.__update_state_text()

        self.__progress_bars = []
        for _ in range(3):
            self.__progress_bars.append(
                rich.progress_bar.ProgressBar(0, completed=0, width=100)
            )
        progress_table = rich.table.Table(
            show_edge=False, show_footer=False, show_header=False
        )
        progress_table.add_column()

        for progress_bar in self.__progress_bars:
            progress_table.add_row(progress_bar)

        progress_panel = rich.panel.Panel(progress_table)

        root_layout["progress"].update(
            rich.align.Align.center(progress_panel, vertical="middle")
        )

        self.__progress_panel = progress_panel
        self.__reset_progress_bars()

        # init the live display
        super().__init__(root_layout, screen=True)

    # notification *************************************************************
    __xomodoro_state_to_notification_text = {
        XomodoroState.focus: "Focus now",
        XomodoroState.long_break: "Let's relax for a while",
        XomodoroState.short_break: "Let's take a break",
        XomodoroState.stopped: "stopped",
    }

    def __notify(self):
        state = self.__xomodoro.state
        notification_text = XomodoroDisplay.__xomodoro_state_to_notification_text[state]
        notification_audio = str(self.__state_to_alert_path[state])

        self.__notification.message = notification_text
        self.__notification.audio = notification_audio

        self.__notification.send()

    # progress *****************************************************************
    def __reset_progress_bars(self):
        state = self.__xomodoro.state
        seconds = self.__xomodoro.seconds
        total_seconds = self.__xomodoro.total_seconds

        self.__progress_panel.style = XomodoroDisplay.__xomodoro_state_to_style[state]

        for progress_bar in self.__progress_bars:
            progress_bar.pulse = state == XomodoroState.stopped

            progress_bar.update(seconds, total=total_seconds)

    def __update_progress_bars(self):
        seconds = self.__xomodoro.seconds

        for progress_bar in self.__progress_bars:
            progress_bar.update(seconds)

    # state ********************************************************************
    __xomodoro_state_to_text = {
        XomodoroState.focus: (
            "      ___           ___           ___           ___           ___     \n"
            "     /\__\         /\  \         /\__\         /\  \         /\__\    \n"
            "    /:/ _/_       /::\  \       /:/  /         \:\  \       /:/ _/_   \n"
            "   /:/ /\__\     /:/\:\  \     /:/  /           \:\  \     /:/ /\  \  \n"
            "  /:/ /:/  /    /:/  \:\  \   /:/  /  ___   ___  \:\  \   /:/ /::\  \ \n"
            " /:/_/:/  /    /:/__/ \:\__\ /:/__/  /\__\ /\  \  \:\__\ /:/_/:/\:\__\ \n"
            " \:\/:/  /     \:\  \ /:/  / \:\  \ /:/  / \:\  \ /:/  / \:\/:/ /:/  / \n"
            "  \::/__/       \:\  /:/  /   \:\  /:/  /   \:\  /:/  /   \::/ /:/  /\n"
            "   \:\  \        \:\/:/  /     \:\/:/  /     \:\/:/  /     \/_/:/  /\n"
            "    \:\__\        \::/  /       \::/  /       \::/  /        /:/  /\n"
            "     \/__/         \/__/         \/__/         \/__/         \/__/\n"
        ),
        XomodoroState.long_break: (
            "                    ___           ___           ___                                  ___           ___           ___           ___     \n"
            "                   /\  \         /\  \         /\__\                  _____         /\  \         /\__\         /\  \         /|  |    \n"
            "                  /::\  \        \:\  \       /:/ _/_                /::\  \       /::\  \       /:/ _/_       /::\  \       |:|  |    \n"
            "                 /:/\:\  \        \:\  \     /:/ /\  \              /:/\:\  \     /:/\:\__\     /:/ /\__\     /:/\:\  \      |:|  |    \n"
            "  ___     ___   /:/  \:\  \   _____\:\  \   /:/ /::\  \            /:/ /::\__\   /:/ /:/  /    /:/ /:/ _/_   /:/ /::\  \   __|:|  |    \n"
            " /\  \   /\__\ /:/__/ \:\__\ /::::::::\__\ /:/__\/\:\__\          /:/_/:/\:|__| /:/_/:/__/___ /:/_/:/ /\__\ /:/_/:/\:\__\ /\ |:|__|____\n"
            " \:\  \ /:/  / \:\  \ /:/  / \:\~~\~~\/__/ \:\  \ /:/  /          \:\/:/ /:/  / \:\/:::::/  / \:\/:/ /:/  / \:\/:/  \/__/ \:\/:::::/__/\n"
            "  \:\  /:/  /   \:\  /:/  /   \:\  \        \:\  /:/  /            \::/_/:/  /   \::/~~/~~~~   \::/_/:/  /   \::/__/       \::/~~/~    \n"
            "   \:\/:/  /     \:\/:/  /     \:\  \        \:\/:/  /              \:\/:/  /     \:\~~\        \:\/:/  /     \:\  \        \:\~~\     \n"
            "    \::/  /       \::/  /       \:\__\        \::/  /                \::/  /       \:\__\        \::/  /       \:\__\        \:\__\    \n"
            "     \/__/         \/__/         \/__/         \/__/                  \/__/         \/__/         \/__/         \/__/         \/__/\n"
        ),
        XomodoroState.short_break: (
            "      ___           ___           ___           ___                                                ___           ___           ___           ___     \n"
            "     /\__\         /\  \         /\  \         /\  \                                _____         /\  \         /\__\         /\  \         /|  |    \n"
            "    /:/ _/_        \:\  \       /::\  \       /::\  \         ___                  /::\  \       /::\  \       /:/ _/_       /::\  \       |:|  |    \n"
            "   /:/ /\  \        \:\  \     /:/\:\  \     /:/\:\__\       /\__\                /:/\:\  \     /:/\:\__\     /:/ /\__\     /:/\:\  \      |:|  |    \n"
            "  /:/ /::\  \   ___ /::\  \   /:/  \:\  \   /:/ /:/  /      /:/  /               /:/ /::\__\   /:/ /:/  /    /:/ /:/ _/_   /:/ /::\  \   __|:|  |    \n"
            " /:/_/:/\:\__\ /\  /:/\:\__\ /:/__/ \:\__\ /:/_/:/__/___   /:/__/               /:/_/:/\:|__| /:/_/:/__/___ /:/_/:/ /\__\ /:/_/:/\:\__\ /\ |:|__|____\n"
            " \:\/:/ /:/  / \:\/:/  \/__/ \:\  \ /:/  / \:\/:::::/  /  /::\  \               \:\/:/ /:/  / \:\/:::::/  / \:\/:/ /:/  / \:\/:/  \/__/ \:\/:::::/__/\n"
            "  \::/ /:/  /   \::/__/       \:\  /:/  /   \::/~~/~~~~  /:/\:\  \               \::/_/:/  /   \::/~~/~~~~   \::/_/:/  /   \::/__/       \::/~~/~    \n"
            "   \/_/:/  /     \:\  \        \:\/:/  /     \:\~~\      \/__\:\  \               \:\/:/  /     \:\~~\        \:\/:/  /     \:\  \        \:\~~\     \n"
            "     /:/  /       \:\__\        \::/  /       \:\__\          \:\__\               \::/  /       \:\__\        \::/  /       \:\__\        \:\__\    \n"
            "     \/__/         \/__/         \/__/         \/__/           \/__/                \/__/         \/__/         \/__/         \/__/         \/__/\n"
        ),
        XomodoroState.stopped: (
            "      ___                         ___           ___         ___         ___                   \n"
            "     /\__\                       /\  \         /\  \       /\  \       /\__\         _____    \n"
            "    /:/ _/_         ___         /::\  \       /::\  \     /::\  \     /:/ _/_       /::\  \   \n"
            "   /:/ /\  \       /\__\       /:/\:\  \     /:/\:\__\   /:/\:\__\   /:/ /\__\     /:/\:\  \  \n"
            "  /:/ /::\  \     /:/  /      /:/  \:\  \   /:/ /:/  /  /:/ /:/  /  /:/ /:/ _/_   /:/  \:\__\ \n"
            " /:/_/:/\:\__\   /:/__/      /:/__/ \:\__\ /:/_/:/  /  /:/_/:/  /  /:/_/:/ /\__\ /:/__/ \:|__|\n"
            " \:\/:/ /:/  /  /::\  \      \:\  \ /:/  / \:\/:/  /   \:\/:/  /   \:\/:/ /:/  / \:\  \ /:/  /\n"
            "  \::/ /:/  /  /:/\:\  \      \:\  /:/  /   \::/__/     \::/__/     \::/_/:/  /   \:\  /:/  / \n"
            "   \/_/:/  /   \/__\:\  \      \:\/:/  /     \:\  \      \:\  \      \:\/:/  /     \:\/:/  /  \n"
            "     /:/  /         \:\__\      \::/  /       \:\__\      \:\__\      \::/  /       \::/  /   \n"
            "     \/__/           \/__/       \/__/         \/__/       \/__/       \/__/         \/__/\n"
        ),
    }
    __xomodoro_state_to_style = {
        XomodoroState.focus: "bright_red",
        XomodoroState.long_break: "blue",
        XomodoroState.short_break: "bright_blue",
        XomodoroState.stopped: "cyan",
    }

    def __update_state_text(self):
        state = self.__xomodoro.state

        text = XomodoroDisplay.__xomodoro_state_to_text[state]
        style = XomodoroDisplay.__xomodoro_state_to_style[state]
        text = rich.text.Text(text, style=style)

        self.__root_layout["state"].update(
            rich.align.Align.center(text, vertical="middle")
        )

    # update *******************************************************************
    def refresh(self):
        state = self.__xomodoro.state

        if state != self.__previous_state:
            self.__previous_state = state

            self.__reset_progress_bars()
            self.__update_state_text()
            self.__notify()

        self.__update_progress_bars()

        super().refresh()
