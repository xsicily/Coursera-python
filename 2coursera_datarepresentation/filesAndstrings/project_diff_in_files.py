"""
Project for Week 4 of "Python Data Representations".
Find differences in file contents.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

IDENTICAL = -1


def singleline_diff(line1, line2):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
    Output:
      Returns the index where the first difference between
      line1 and line2 occurs.

      Returns IDENTICAL if the two lines are the same.
        singleline_diff('first', 'first')
    >>> singleline_diff('first', 'first')
    -1
    >>> singleline_diff('first', 'First')
    0
    >>> singleline_diff('first', 'fires')
    3
    >>> singleline_diff('first is', 'first is not second')
    8
    >>> singleline_diff('first', 'the first one')
    0
    >>> singleline_diff('today is cold', 'today is hot')
    9
    >>> singleline_diff('abc', 'abd')
    2
    >>> singleline_diff('', 'a')
    0
    """
    if line1 == line2:
        return IDENTICAL

    len_1 = len(line1)
    len_2 = len(line2)
    smaller_len = min(len_1, len_2)

    for idx in range(smaller_len):
        if line1[idx] != line2[idx]:
            return idx

    return smaller_len


def singleline_diff_format(line1, line2, idx):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
      idx   - index at which to indicate difference
    Output:
      Returns a three line formatted string showing the location
      of the first difference between line1 and line2.

      If either input line contains a newline or carriage return,
      then returns an empty string.

      If idx is not a valid index, then returns an empty string.

    >>> singleline_diff_format('abcd', 'abef', 2)
    'abcd\\n==^\\nabef\\n'

    >>> singleline_diff_format('today is cold', 'today is hot', 9)
    'today is cold\\n=========^\\ntoday is hot\\n'

    >>> singleline_diff_format('abc', 'abd', 1)
    'abc\\n=^\\nabd\\n'

    >>> singleline_diff_format('', 'a', 0)
    '\\n^\\na\\n'

    """
    invalid_string = "'\n', '\r'"

    len_1 = len(line1)
    len_2 = len(line2)
    smaller_len = min(len_1, len_2)

    if invalid_string in line1:
        return ""
    elif invalid_string in line2:
        return ""
    elif idx not in range(smaller_len + 1):
        return ""
    else:
        return line1 + "\n" + '=' * idx + '^' + "\n" + line2 + "\n"


def multiline_diff(lines1, lines2):
    """
    Inputs:
      lines1 - list of single line strings
      lines2 - list of single line strings
    Output:
      Returns a tuple containing the line number (starting from 0) and
      the index in that line where the first difference between lines1
      and lines2 occurs.

      Returns (IDENTICAL, IDENTICAL) if the two lists are the same.
    >>> multiline_diff(['ab', 'abcd'], ['ab', 'abcd'])
    (-1, -1)
    >>> multiline_diff(['ab', 'abcd'], ['ad', 'abef'])
    (0, 1)
    >>> multiline_diff(['ab', 'abcd'], ['ab', 'abef'])
    (1, 2)
    >>> multiline_diff(['ab', 'abcd'], ['ab', 'abefgh'])
    (1, 2)
    >>> multiline_diff(['ab', 'abcd'], ['ab', 'abef', 'efg'])
    (1, 2)
    >>> multiline_diff(['line1', 'line2'], ['line1', 'line2', 'line3'])
    (2, 0)
    >>> multiline_diff(['', ''], ['a', 'b'])
    (0, 0)
    """
    if lines1 == lines2:
        return IDENTICAL, IDENTICAL

    lens_1 = len(lines1)
    lens_2 = len(lines2)
    smaller_lens = min(lens_1, lens_2)

    for idx in range(smaller_lens):
        diff_index = singleline_diff(lines1[idx], lines2[idx])
        if diff_index > -1:
            return idx, diff_index

    return smaller_lens, 0


def get_file_lines(filename):
    """
    Inputs:
      filename - name of file to read
    Output:
      Returns a list of lines from the file named filename.  Each
      line will be a single line string with no newline ('\n') or
      return ('\r') characters.

      If the file does not exist or is not readable, then the
      behavior of this function is undefined.
    >>> test='C:/Users/Sicil/PycharmProjects/pythonbasic/2coursera_datarepresentation/w4/test'
    >>> test3='C:/Users/Sicil/PycharmProjects/pythonbasic/2coursera_datarepresentation/w4/test3'
    >>> get_file_lines(test)
    ['what they are?', 'how to create them?', 'when to use them?']
    >>> get_file_lines(test3)
    []
    """

    datafile = open(filename, 'rt')
    data = datafile.read().splitlines()
    datafile.close()

    return data


def file_diff_format(filename1, filename2):
    """
    Inputs:
      filename1 - name of first file
      filename2 - name of second file
    Output:
      Returns a four line string showing the location of the first
      difference between the two files named by the inputs.

      If the files are identical, the function instead returns the
      string "No differences\n".

      If either file does not exist or is not readable, then the
      behavior of this function is undefined.
    >>> test1 = "C:/Users/Sicil/PycharmProjects/pythonbasic/2coursera_datarepresentation/w4/test1"
    >>> test2 = "C:/Users/Sicil/PycharmProjects/pythonbasic/2coursera_datarepresentation/w4/test2"
    >>> file_diff_format(test1, test2)
    'Line 0:\\n\\n^\\nn\\n'
    """
    file_lines_1 = get_file_lines(filename1)
    file_lines_2 = get_file_lines(filename2)

    if file_lines_1 == file_lines_2:
        return 'No differences\n'

    diff_tup = multiline_diff(file_lines_1, file_lines_2)
    idx = diff_tup[0]
    diff_index = diff_tup[1]

    if len(file_lines_1) != 0:
        if len(file_lines_2) != 0:
            result = "Line " + str(idx) + ":" + "\n"
            result += str(singleline_diff_format(file_lines_1[idx], file_lines_2[idx], diff_index))
            return result
        else:
            result = "Line 0:" + "\n"
            result += file_lines_1[idx] + "\n" + '^' + "\n" + "\n"
            return result
    else:
        result = "Line 0:" + "\n"
        result += "\n" + '^' + "\n" + file_lines_2[idx] + "\n"
        return result



if __name__ == "__main__":
    import doctest
    doctest.testmod()

