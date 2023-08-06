Something like this:

```python
import os
import random
import time

from rich.console import Console

from rich_sparklines import Graph

console = Console()


def main():
    graph = Graph("connections", lambda: random.randint(0, 20))
    while True:
        graph.update()

        os.system("cls")

        console.print(graph)

        time.sleep(1)


if __name__ == "__main__":
    main()
```

will produce something like this:

![Example](./example.png)
