# CISC 320 - Programming Assignment 1 - COWS!!!

## Usage

```bash
python cows.py [file]
```

### Examples

```bash
$ python cows.py ./my_data.txt
7 1000 2000 3
1 1000 2000 3
9 1000 2000 8
2 1000 2001 4
4 1001 2000 6
8 1500 2000 5
3 1500 2001 4
5 1501 2001 5
```

```bash
$ python cows.py ./example_data.txt
507 1000 1000 6
1 1400 1700 7
```

## Formal Specification

### Problem

Calculate, sort, and report minimum, most recent, and average of a sequence of records.

### Input

The filename of a local file containing a sequence of cow records, each on their own line. The first line will be the number of records to read, and is not included in the number of records. You can assume that each line will only contain one record. The records will come in ordered by the time they were collected.

A cow record consists of three numbers and a letter, separated by spaces (in the form "Number, Letter, Number, Number"). All numbers will be 32-bit integers (i.e., no more than 2^31).

- The first element is the Cow ID, a unique number representing that cow inside the dataset.
- The second element is the Action Code, and will be either the letter "W", "M", or "T"
- If the letter is "W", for "Weighing", then the third element will be the latest Weight of the cow (a number in pounds).
- If the letter is "M", for "Milking", then the third element will be the amount of the Milk produced by the cow (a number in pounds).
- If the letter is "T", for "Temperature", then the third element will be the current Temperature of the cow (a number in Fahrenheit).
- The fourth element is the Timestamp, a number representing when the record was made.

An example of several records are below:

```Text
507 W 1000 1
1 M 6 2
1 W 1400 3
1 M 8 8
1 T 101 10
507 M 4 12
1 W 1700 15
1 M 7 16
507 M 8 20
```

### Output

A series of sorted cow status reports. Each line of output will contain four numbers:

- The cow's ID
- The cow's lowest weight
- The cow's latest weight
- The cow's average milk production (the sum of all the milkings divided by the number of milkings).

If a cow doesn't have at least one weighing and at least one milking, then you should exclude it from the output. The cows should be sorted in ascending order based the status results: first by their lowest weight, than their latest weight, and finally by their highest average milk production. Truncate any decimals to become integers.

An example of output is below:

```Text
507 1000 1000 6
1 1400 1700 7
```

## Runtime Analysis

I believe that the runtime of this program satisfies the `O(c*log(c)+r)` time requirement, where `c` is the number of cows and `r` is the number of records. The program accomplishes this via a hash map, an array, and a built-in sort. This can be further broken down into input parsing and sorting/output.

### Input Parsing - `O(r)`

As we trace the path of the input, we need to ensure that the overall process has linear complexity.

Line 79: `index_map = {}`

- Initializes a hash map to associate a cow ID with an array index. Cow ID's are kept as str values to benefit from hash map [optimizations](https://wiki.python.org/moin/TimeComplexity#:~:text=Note%20that%20there%20is%20a%20fast%2Dpath%20for%20dicts%20that%20(in%20practice)%20only%20deal%20with%20str%20keys%3B%20this%20doesn%27t%20affect%20the%20algorithmic%20complexity%2C%20but%20it%20can%20significantly%20affect%20the%20constant%20factors%3A%20how%20quickly%20a%20typical%20program%20finishes.).

Line 80:  `cow_arr = np.empty(f_len, dtype=Cow)`

- Initializes an empty array to store the records. A numpy array was chosen over a list to avoid the underlying black box. This is [expected](https://pypi.org/project/big-O/#:~:text=big_o.big_o.Linear%27%3E%2C%20...)-,numpy.empty,-instead%20just%20allocates) to run in `O(1)` time.

Line 84: `cow_id, act_code, act_data, t_stamp = line.split()`

- The `split()` method is used to facilitate variable assignments. With no parameters, the `split()` method is expected to run in `O(w)` time, where w is the width of the line.

Line 87: `if cow_id in index_map:`

- Determining whether a key exists in the hash map is [expected](https://wiki.python.org/moin/TimeComplexity) to run in `O(1)` time.

Line 88: `arr_id = index_map[cow_id]`

- Retrieving a value from the hash map is [expected](https://wiki.python.org/moin/TimeComplexity) to run in `O(1)` time.

Line 90: `arr_id = len(index_map)`

- The length of the hash map is a [stored value](https://wiki.python.org/moin/TimeComplexity) and is expected to run in `O(1)` time.

Line 92: `cow_arr[arr_id] = Cow(cow_id)`

- Associating an array index with a new `Cow` object should run in `O(1)` in the average case.

Lines 94-103:

- The input data is processed by calling an associated method on the `Cow` object. These methods manipulate properties of the `Cow` object and are expected to run in `O(1)` time.

From line 84, the above is repeated for each line of input. The resulting complexity is `O(r*w)`. However, `w` can be treated as a constant, which allows us to simplify the complexity to `O(r)`. In other words, the complexity per line of input is `O(1)`, as required in the problem statement.

### Sorting/Output  - `O(c*log(c))`

There are only two chunks of code to consider in this section and both have are straightforward.

Line 107: `sort_arr = np.sort(cow_arr[: len(index_map)], kind="mergesort")`

- The cow array elements are isolated by using the length of the hash map to create a view. This is [expected](https://wiki.python.org/moin/TimeComplexity) to run in `O(1)` time.
- The [view](https://numpy.org/doc/stable/user/basics.copies.html#indexing-operations) of the array is `O(1)` as we are modifying how the array is [addressed](https://numpy.org/doc/stable/user/basics.copies.html#view) and not modifying the underlying data.
- Numpy's `sort()` method is used. While `mergesort` is passed as a parameter, the [documentation](https://numpy.org/doc/stable/reference/generated/numpy.sort.html#:~:text=yes-,Note,-The%20datatype%20determines) states `timsort` might be used instead. Regardless, we're guaranteed a worst case complexity of `O(c*log(c))`.

Lines 108-110:

- A for loop is used to iterate through the array of `Cow` objects. So long as the record is valid, as defined by the problem statement, it is printed. This loop adds a complexity of `O(c)`, but is insignificant next to ~~the power of the force~~ `O(c*log(c))`.

### Conclusion

There are two main parts to this program. The first is input parsing, which is `O(r)`. The second is the sorting/output, which is `O(c*log(c))`. The combination yields an overall, average-case complexity of `O(c*log(c)+r)`, as required.
