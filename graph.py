class Vertex:
    def __init__(
        self, id: int, height: int, excessFlow: int, sourceId: int, sinkId: int
    ) -> None:
        self.id = id
        self.height = height
        self.excessFlow = excessFlow
        self.sourceId = sourceId
        self.sinkId = sinkId
        self.isTraverse = False
        self.isAdjacent = False
        self.isSelected = False
        self.isRelabel = False

    def toJSON(self):
        color = "lightblue"  # Normal vertex
        if self.isSelected:
            color = "red"  # Adjacent vertex that is selected to receive excess flow
        elif self.isRelabel:    # Peforming relabel on vertex
            color = "lightgray"
        elif self.isTraverse:
            color = "lightgreen"  # Current selected vertex
        elif self.isAdjacent:
            color = "lightyellow"  # Adjacent vertex
        elif self.id == self.sourceId:
            color = "lightpink"  # Source vertex
        elif self.id == self.sinkId:
            color = "orange"  # Sink vertex

        return {
            "id": str(self.id),
            "label": f"{self.height}:{str(self.excessFlow)}",
            "color": color,
        }

    def __str__(self) -> str:
        return str(
            {
                "id": self.id,
                "height": self.height,
                "excessFlow": self.excessFlow,
                "isTraverse": self.isTraverse,
                "isAdjacent": self.isAdjacent,
            }
        )


class Edge:
    def __init__(
        self, u: int, v: int, capacity: int, flow: int, isBackward: bool = False
    ) -> None:
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = flow
        self.isBackward = isBackward

    def toJSON(self):
        return {
            "from": str(self.u),
            "to": str(self.v),
            "label": str(self.flow),
            "style": "dotted" if self.isBackward else "solid",
            "color": "lightblue",
        }

    def __str__(self) -> str:
        return str(
            {
                "from": self.u,
                "to": self.v,
                "capacity": self.capacity,
                "flow": self.flow,
                "isBackward": self.isBackward,
            }
        )
