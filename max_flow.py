import sys

from exception import InvalidEdgeError
from graph import Edge, Vertex

# Global variables
VERTICES = []
EDGES = []
NUM_VERTICES = 0
SOURCE_ID = 0
SINK_ID = 0
GRAPH = {
    "kind": {"graph": True},
    "nodes": [],
    "edges": [],
}
RESIDUAL_GRAPH = {
    "kind": {"graph": True},
    "nodes": [],
    "edges": [],
}


def updateGraph() -> None:
    """
    Utility function to update the graph upon any changes
    """

    global GRAPH, RESIDUAL_GRAPH
    GRAPH = {
        "kind": {"graph": True},
        "nodes": [vertex.toJSON() for vertex in VERTICES],
        "edges": [edge.toJSON() for edge in EDGES if not edge.isBackward],
    }

    # Repopulate residual graph based on edges
    residualEdges = []
    for edge in EDGES:
        if edge.isBackward:
            continue

        forwardFlow = edge.capacity - edge.flow
        if forwardFlow != 0:
            forwardEdge = Edge(edge.u, edge.v, edge.capacity, forwardFlow)
            residualEdges.append(forwardEdge)

        backwardFlow = edge.flow
        if backwardFlow != 0:
            backwardEdge = Edge(edge.v, edge.u, edge.capacity, edge.flow, True)
            residualEdges.append(backwardEdge)

    RESIDUAL_GRAPH = {
        "kind": {"graph": True},
        "nodes": [vertex.toJSON() for vertex in VERTICES],
        "edges": [edge.toJSON() for edge in residualEdges],
    }


def traverseVertex(vertexId: int, isCompleted: bool = False) -> None:
    """
    Utility function for visuals to be displayed on debugger extension
    """

    VERTICES[vertexId].isTraverse = not isCompleted
    for edge in EDGES:
        # Get adjacent nodes and update their color
        if edge.u == vertexId:
            VERTICES[edge.v].isAdjacent = not isCompleted
    updateGraph()


def selectAdjacentVertex(vertexId: int, isSelected: bool = True) -> None:
    """
    Utility function for visuals to be displayed on debugger extension
    """

    VERTICES[vertexId].isSelected = isSelected
    updateGraph()


def populateVertices():
    """
    Initialize all vertices in graph
    """

    for i in range(NUM_VERTICES):
        vertex = Vertex(i, 0, 0, SOURCE_ID, SINK_ID)
        VERTICES.append(vertex)
    updateGraph()


def addEdge(u: int, v: int, capacity: int) -> None:
    """
    Adds an edge between two vertices

    Args:
        u (int): ID of source vertex
        v (int): ID of destination vertex
        capacity (int): Maximum flow that the edge can transfer
    Raises:
        InvalidEdgeError: Either source or destination vertex does not exist in graph
    """

    isValidSource = any(vertex["id"] == str(u) for vertex in GRAPH["nodes"])
    isValidDestination = any(vertex["id"] == str(v) for vertex in GRAPH["nodes"])

    # Check if source and destination vertices are valid
    if not isValidSource or not isValidDestination:
        raise InvalidEdgeError()

    # Creation of edge
    edge = Edge(u, v, capacity, 0)
    EDGES.append(edge)

    updateGraph()


def updateBackwardEdge(edgeId: int, flow: int) -> None:
    """
    Updates the flow of an backward edge by obtaining the corresponding backward
    edge. Creates a new backward edge in the graph if it does not exist.

    Args:
        edgeId (int): ID of source vertex
    """

    currentEdge = EDGES[edgeId]

    for edge in EDGES:
        # Retrieve the corresponding backward edge
        if edge.u == currentEdge.v and edge.v == currentEdge.u:
            edge.flow -= flow
            updateGraph()
            return

    # Create a backward edge if it does not exist in the graph
    createBackwardEdge(currentEdge.v, currentEdge.u, currentEdge.capacity, flow)


def createBackwardEdge(u: int, v: int, capacity: int, flow: int) -> None:
    """
    Creation of a backward edge

    Args:
        u (int): ID of source vertex
        v (int): ID of destination vertex
        flow (int): Current flow of the edge
        capacity (int): Maximum flow that the edge can transfer
    """

    edge = Edge(u, v, flow, 0, True)
    EDGES.append(edge)
    updateGraph()


def hasExcessFlow(sourceId: int, sinkId: int) -> int:
    """
    Searches for excess flow in the graph to determine the subsequent vertex that requires
    either push() or relabel()

    Return:
        -1: If none of the vertices contain any excess flow
        index (int): ID of the vertex that contains excess flow
    """

    for index, vertex in enumerate(VERTICES):
        # Excess flow on sink vertex is not considered
        if vertex.id == sourceId or vertex.id == sinkId:
            continue

        if vertex.excessFlow > 0:
            return index
    return -1


def preFlow(sourceId: int) -> None:
    """
    Initialize the height of all vertices to 0 except the source vertex.
    Adjacent vertices of the source vertex are initialized with an excess flow of
    its full capacity.

    Args:
        sourceId (int): ID of source vertex
    """

    # Setting the height of source vertex as the number of vertices
    VERTICES[sourceId].height = len(VERTICES)

    for edge in EDGES:
        # Get adjacent vertices of source vertex
        if edge.u == sourceId:
            edge.flow = edge.capacity

            # Set excess flow of adjacent vertices to max capacity
            destinationId = edge.v
            VERTICES[destinationId].excessFlow += edge.flow

            # Creating a backward edge in the residual graph from
            # adjacent vertices back to source
            createBackwardEdge(destinationId, sourceId, edge.capacity, 0)


def push(u: int) -> bool:
    """
    Operation is performed on vertex that contains excess flow.
    Searches for adjacent vertices that:
        1. has a lower height than the current vertex
        2. does not utilise its full flow capacity
    Amount of excess flow pushed to the adjacent vertex will be the
    minimum of excess flow and the available capacity of the edge.

    Args:
        u (int): ID of the vertex that contains excess flow
    Return:
        boolean: Determines whether a push has been performed
    """

    for index, edge in enumerate(EDGES):
        # Get all edges that belongs to specified vertex
        if edge.u == u:
            # Push is impossible since the flow of
            # current edge has reached its max capacity
            if edge.flow == edge.capacity:
                continue

            sourceVertex = VERTICES[u]
            destinationVertex = VERTICES[edge.v]

            # Push is only possible if the height of current vertex
            # is taller than the adjacent vertex
            if sourceVertex.height > destinationVertex.height:
                # Amount of flow is limited to either remaining available flow
                # of the edge or excess flow of the vertex
                traverseVertex(u)
                selectAdjacentVertex(edge.v)

                flow = min(
                    edge.capacity - edge.flow,
                    sourceVertex.excessFlow,
                )

                # Transfer the flow from source to destination
                sourceVertex.excessFlow -= flow
                destinationVertex.excessFlow += flow

                edge.flow += flow
                updateBackwardEdge(index, flow)

                selectAdjacentVertex(edge.v, False)
                traverseVertex(u, True)
                return True

    traverseVertex(u, True)
    return False


def relabel(u: int) -> None:
    """
    Initialize the height of all vertices to 0 except the source vertex.
    Adjacent vertices of the source vertex are initialized with an excess flow of
    its full capacity.

    Args:
        u (int): ID of the vertex that contains excess flow but is unable to perform any push()
    """
    minHeight = sys.maxsize

    for edge in EDGES:
        # Find corresponding edge
        if edge.u == u:
            # Relabeling is impossible due to the flow reaching its
            # max capacity
            if edge.flow == edge.capacity:
                continue

            destinationVertex = VERTICES[edge.v]
            # Retrieve the minimum height of all adjacent vertices
            # and update the height current vertex
            if destinationVertex.height < minHeight:
                minHeight = destinationVertex.height
                currentVertex = VERTICES[u]
                currentVertex.height = minHeight + 1

                updateGraph()


def getMaxFlow(sourceId: int, sinkId: int) -> int:
    """
    Gets maximum flow of a given graph

    Args:
        sourceId (int): ID of the source vertex
        sinkId (int): ID of the sink vertex
    Returns:
        int: Representing the maximum flow of a graph
    """
    preFlow(sourceId)
    vertexId = hasExcessFlow(sourceId, sinkId)

    while vertexId != -1:
        if not push(vertexId):
            # If push is not possible due to the current vertex having
            # same height as all adjacent vertices
            relabel(vertexId)

        vertexId = hasExcessFlow(sourceId, sinkId)

    # Sink is located at the last vertex in the array,
    # any excess flow in the vertex will be considered the max flow
    return VERTICES[sinkId].excessFlow


def setGraphSettings(sourceId: int, sinkId: int, numOfVertices: int) -> None:
    """
    Utility function to set graph settings

    Args:
        sourceId (int): ID of the source vertex
        sinkId (int): ID of the sink vertex
        numOfVertices (int): Number of vertices in the graph
    """
    global SOURCE_ID, SINK_ID, NUM_VERTICES, GRAPH, VERTICES, EDGES

    SOURCE_ID = sourceId
    SINK_ID = sinkId
    NUM_VERTICES = numOfVertices
    GRAPH = {
        "kind": {"graph": True},
        "nodes": [],
        "edges": [],
    }
    VERTICES = []
    EDGES = []

    populateVertices()


if __name__ == "__main__":
    SOURCE_ID, SINK_ID, NUM_VERTICES = 0, 5, 6
    setGraphSettings(SOURCE_ID, SINK_ID, NUM_VERTICES)
    addEdge(0, 1, 13)
    addEdge(0, 2, 10)
    addEdge(2, 1, 3)
    addEdge(1, 5, 7)
    addEdge(1, 3, 6)
    addEdge(3, 4, 10)
    addEdge(4, 5, 5)
    addEdge(1, 5, 7)
    print(getMaxFlow(SOURCE_ID, SINK_ID))
