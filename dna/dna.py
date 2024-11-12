import csv
import sys


def main():

    # TODO: Check for command-line usage
    if (len(sys.argv) != 3):
        print("Error")

    # TODO: Read database file into a variable
    seq_list = []
    with open(sys.argv[1], 'r') as database:
        data_read = csv.reader(database)
        first_line = next(data_read)
        for item in first_line:
            if (item != 'name'):
                seq_list.append(item)

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2], 'r') as sequence:
        seq_read = sequence.read()

    # TODO: Find longest match of each STR in DNA sequence
    matches = []
    for each in seq_list:
        matches.append(longest_match(seq_read, each))

    # TODO: Check database for matching profiles
    is_match = False
    with open(sys.argv[1], 'r') as database:
        data_read = csv.reader(database)
        next(data_read)
        for line in data_read:
            check_matches = 0
            for i in range(len(seq_list)):
                if (int(line[i+1]) == matches[i]):
                    check_matches += 1
                    if (check_matches == len(seq_list)):
                        print(line[0])
                        is_match = True
                        return
    if not is_match:
        print("No match")

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
