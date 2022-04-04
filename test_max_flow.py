from time import time
from max_flow import getMaxFlow, setGraphSettings, addEdge


def test_case_one():
    SOURCE_ID, SINK_ID, NUM_VERTICES = 0, 3, 4
    setGraphSettings(SOURCE_ID, SINK_ID, NUM_VERTICES)
    addEdge(0, 1, 3)
    addEdge(1, 2, 1)
    addEdge(2, 3, 2)

    return getMaxFlow(SOURCE_ID, SINK_ID)


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

    return getMaxFlow(SOURCE_ID, SINK_ID)


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

    return getMaxFlow(SOURCE_ID, SINK_ID)


def test_case_four():
    SOURCE_ID, SINK_ID, NUM_VERTICES = 0, 5, 6
    setGraphSettings(SOURCE_ID, SINK_ID, NUM_VERTICES)
    addEdge(0, 1, 13)
    addEdge(0, 2, 10)
    addEdge(2, 1, 3)
    addEdge(1, 5, 7)
    addEdge(1, 3, 6)
    addEdge(3, 4, 10)
    addEdge(4, 5, 5)

    return getMaxFlow(SOURCE_ID, SINK_ID)


if __name__ == "__main__":
    test_cases = [test_case_one, test_case_two, test_case_three, test_case_four]
    expected_result = [1, 23, 15, 12]
    num_test_cases_matched = 0
    num_test_cases = len(test_cases)

    for i in range(num_test_cases):
        start_time = time()
        result = test_cases[i]()
        time_taken = time() - start_time

        print("     Test Case : #" + str(i + 1))
        print("Execution Time : " + str(round(time_taken, 2)) + " seconds")
        print("         Result: " + str(result))
        if result == expected_result[i]:
            print("Passed")
            num_test_cases_matched += 1
        else:
            print("Failed")

        print(
            "--------------------------------------------------------------------------"
        )

    print("Number of test cases : " + str(num_test_cases))
    print("Number of test cases with matched outcome : " + str(num_test_cases_matched))
    print("--------------------------------------------------------------------------")
