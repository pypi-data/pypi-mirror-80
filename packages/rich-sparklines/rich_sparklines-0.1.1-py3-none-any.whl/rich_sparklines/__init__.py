from collections import deque
from typing import Callable, Deque

import sparklines
from rich.console import RenderGroup
from rich.padding import Padding
from rich.panel import Panel
from rich.text import Text


class Graph(Panel):
    length = 20
    queue: Deque[int]

    def __init__(
        self,
        label,
        get_value: Callable[[], int],
        colours=("red1", "orange1", "yellow1", "green"),
    ):
        self.queue = deque([0] * self.length, maxlen=self.length)
        self.label = label
        self.colours = colours
        self.get_value = get_value

        super().__init__(
            self.rerender(), title=f"{label}: [blue]?[/]", width=self.length + 4,
        )

    def rerender(self):
        lines = [
            Text(line, style=colour)
            for colour, line in zip(
                self.colours,
                sparklines.sparklines(
                    self.queue, num_lines=len(self.colours), minimum=0, maximum=20
                ),
            )
        ]
        return Padding(RenderGroup(*lines), 1)

    def update(self):
        used = self.get_value()

        self.q.extend([max(0, used if used != "?" else 0)])

        self.title = f"{self.label}: [blue]{used}[/]"
        self.renderable = self.rerender()
