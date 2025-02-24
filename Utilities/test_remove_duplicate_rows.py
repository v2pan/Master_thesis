from remove_duplicate_rows import remove_duplicate_rows
def test_remove_duplicate_rows():
    TOTAL_DIC = {'dog': ['chien', 'perro']}

    def run_test_case(test_num, output, expected):
        result = remove_duplicate_rows(output, TOTAL_DIC)
        print(f"Test Case {test_num}:")
        print(f"Expected: {expected}")
        print(f"Got:      {result}\n")
        assert result == expected, f"Test Case {test_num} Failed"

    # Test Case 1: Basic duplicate removal with synonyms
    output1 = [
        (3, 'Diego', 15, 3, 'chris', 'dog'),
        (4, 'Marcel', 11, 4, 'juan', 'perro'),
        (1, 'Pierre', 20, 1, 'bill', 'chien')
    ]
    expected1 = [
        (3, 'Diego', 15, 3, 'chris', 'dog'),  # One version remains
        (4, 'Marcel', 11, 4, 'juan', 'perro'),
        (1, 'Pierre', 20, 1, 'bill', 'chien')
    ]
    run_test_case(1, output1, expected1)

    # Test Case 2: Rows that are identical except for word synonyms
    output2 = [
        (3, 'dog'),
        ('perro', 3),
        ('chien', 3)
    ]
    expected2 = [(3, 'dog')]  # Only one row should remain
    run_test_case(2, output2, expected2)

    # Test Case 3: Completely unique rows should not be removed
    output3 = [
        (1, 'apple'),
        (2, 'banana'),
        (3, 'cherry')
    ]
    expected3 = output3  # No duplicates
    run_test_case(3, output3, expected3)

    # Test Case 4: Rows with different word order but equivalent content
    output4 = [
        (1, 'dog', 2),
        (2, 'chien', 1),
        (3, 'cat', 4),
        (4, 'chat', 3)
    ]
    expected4 = [
        (1, 'dog', 2),  # One version of the dog row remains
        (3, 'cat', 4),
        (4, 'chat', 3)   # One version of the cat row remains
    ]
    run_test_case(4, output4, expected4)

    # Test Case 5: Empty input
    output5 = []
    expected5 = []
    run_test_case(5, output5, expected5)

    print("All test cases passed!")


if __name__ == "__main__":
    # Run Tests
    test_remove_duplicate_rows()