from max_flow import getMaxFlow, setGraphSettings, addEdge

def test_case_one():
    SOURCE_ID, SINK_ID, NUM_VERTICES = 0, 3, 4
    setGraphSettings(SOURCE_ID, SINK_ID, NUM_VERTICES)
    addEdge(0, 1, 3)
    addEdge(1, 2, 1)
    addEdge(2, 3, 2)

    max_flow = getMaxFlow(SOURCE_ID, SINK_ID)
    assert max_flow == 1

def test_case_two():
    SOURCE_ID, SINK_ID, NUM_VERTICES = 0, 5, 6
    setGraphSettings(SOURCE_ID, SINK_ID, NUM_VERTICES)
    addEdge(0, 1, 16)
    addEdge(0, 2, 13)
    addEdge(1, 2, 10)
    addEdge(2, 1, 4)
    addEdge(1, 3, 12)
    addEdge(2, 4, 14)
    addEdge(3, 2, 9)
    addEdge(3, 5, 20)
    addEdge(4, 3, 7)
    addEdge(4, 5, 4)

    max_flow = getMaxFlow(SOURCE_ID, SINK_ID)
    assert max_flow == 23

def test_case_three():
    SOURCE_ID, SINK_ID, NUM_VERTICES = 0, 5, 6
    setGraphSettings(SOURCE_ID, SINK_ID, NUM_VERTICES)
    addEdge(0, 1, 10)
    addEdge(1, 2, 5)
    addEdge(0, 3, 8)
    addEdge(1, 3, 2)
    addEdge(3, 4, 10)
    addEdge(4, 2, 8)
    addEdge(4, 5, 10)
    addEdge(2, 5, 7)

    max_flow = getMaxFlow(SOURCE_ID, SINK_ID)
    assert max_flow == 15


if __name__ == "__main__":
    test_case_one()
    test_case_two()
    test_case_three()
