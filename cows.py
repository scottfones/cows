"""CISC 320 - Programming Assignment 1 - Scott Fones."""
from functools import total_ordering
import sys
import numpy as np
from pathlib import Path


@total_ordering
class Cow:
    """Cow class."""

    def __init__(self, cow_id: str = ""):
        """Initialize cow record."""
        self.cow_id = cow_id
        self.avg_milk: float = -1
        self.tot_milk: int = 0
        self.num_milk: float = 0.0
        self.temp: int = -1
        self.cur_weight: int = -1
        self.low_weight: int = -1

    def add_milk(self, m: int) -> None:
        """Update milk metrics.

        Average milk is kept as a float for sorting, truncated to int for output.
        """
        self.tot_milk += m
        self.num_milk += 1.0
        self.avg_milk = self.tot_milk / self.num_milk

    def add_temp(self, t: int) -> None:
        """Update temperature metrics. Not used in this assignment."""
        self.temp = t

    def add_weight(self, w: int) -> None:
        """Update weight metrics.

        Ignoring timestamps. Problem statement specifies record times are monotonically increasing.
        """
        self.cur_weight = w
        if self.low_weight > w or self.low_weight == -1:
            self.low_weight = w

    def is_valid_record(self) -> bool:
        """Check if record contains a weighing and milking."""
        return self.avg_milk > 0 and self.cur_weight > 0

    def __eq__(self, other) -> bool:
        """Cow records are equal if all their measurement fields are equal."""
        return (
            self.avg_milk == other.avg_milk
            and self.cur_weight == other.cur_weight
            and self.low_weight == other.low_weight
        )

    def __lt__(self, obj):
        """Order by Lowest Weight, Latest Weight, Highest Avg Milk."""
        if self.low_weight == obj.low_weight:
            if self.cur_weight == obj.cur_weight:
                return self.avg_milk < obj.avg_milk
            return self.cur_weight < obj.cur_weight
        return self.low_weight < obj.low_weight

    def __repr__(self):
        """Return the problem statment's definition for cow record output."""
        return f"{self.cow_id} {self.low_weight} {self.cur_weight} {self.avg_milk.__floor__()}"


def main() -> int:
    """Process cow data."""
    filename = Path(sys.argv[1])

    with filename.open() as f:
        f_len = int(f.readline())

        i = 0
        index_map = {}
        cow_arr = np.empty(f_len, dtype=Cow)

        # Process status reports
        while i < f_len:
            cow_id, act_code, act_data, t_stamp = f.readline().split()

            arr_id = -1
            if cow_id in index_map:
                arr_id = index_map[cow_id]
            else:
                arr_id = index_map.__len__()
                index_map[cow_id] = arr_id
                cow_arr[arr_id] = Cow(cow_id)

            act_data = int(act_data)
            match act_code:
                case "M":
                    cow_arr[arr_id].add_milk(act_data)
                case "T":
                    cow_arr[arr_id].add_temp(act_data)
                case "W":
                    cow_arr[arr_id].add_weight(act_data)
                case _:
                    raise ValueError(f"Not an action code: {act_code}")

            i += 1

    sort_arr = np.sort(cow_arr[:len(index_map)], kind="mergesort")
    for cow in sort_arr:
        if cow.is_valid_record():
            print(cow)

    return 0


if __name__ == "__main__":
    sys.exit(main())
