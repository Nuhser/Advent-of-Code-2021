from utility.terminal_formatting import Color


class AbstractSolution:
    def __init__(
        self,
        year: int,
        day: int,
        puzzle_input: list[str],
        params: list[str] = [],
        is_test: bool = False,
        verbose: bool = False,
    ) -> None:
        self.year: int = year
        self.day: int = day
        self.is_test: bool = is_test
        self.verbose: bool = verbose
        self.params: list[str] = params

        if verbose:
            print("\nStart parsing input...\n")

        self.parse(puzzle_input)

        if verbose:
            print(f"{Color.GREEN}Parsing complete.{Color.DEFAULT}")

    def parse(self, puzzle_input: list[str]) -> None:
        raise NotImplementedError(
            f"The parser the puzzle input for day {self.day} of year {self.year} isn't implemented yet!"
        )

    def part1(self) -> tuple[str, (int | float | str | None)]:
        raise NotImplementedError(
            f"Part 1 of the solution for day {self.day} of year {self.year} isn't implemented yet!"
        )

    def part2(self) -> tuple[str, (int | float | str | None)]:
        raise NotImplementedError(
            f"Part 2 of the solution for day {self.day} of year {self.year} isn't implemented yet!"
        )

    def visualize(self) -> None:
        raise NotImplementedError(
            f"The visualization for day {self.day} of year {self.year} isn't implemented yet!"
        )


def get_puzzle_input(year: int, day: int) -> tuple[list[str], None]:
    try:
        with open(f"./{year}/input{day:02d}.txt", "r") as puzzle_input:
            return [line for line in puzzle_input.readlines()], None

    except FileNotFoundError:
        raise FileNotFoundError(
            f"There is no puzzle input for day {day} of year {year}! Create a text file named '{year}/input{day:02d}.txt'"
        )


def get_test_input(
    year: int, day: int, test_number: int
) -> tuple[list[str], dict[str, (str | None)]]:
    try:
        with open(
            f"./{year}/test{day:02d}{f'-{test_number}' if (test_number != None) else ''}.txt",
            "r",
        ) as test_input:
            expected_results = {}

            while True:
                last_position = test_input.tell()
                line = test_input.readline()

                if not line.strip().startswith("#!"):
                    break

                splitted_line = line.strip().removeprefix("#!").split(":")

                expected_results[splitted_line[0]] = (
                    splitted_line[1] if not splitted_line[1] == "?" else None
                )

            test_input.seek(last_position)

            return [line for line in test_input.readlines()], expected_results

    except FileNotFoundError:
        raise FileNotFoundError(
            f"There is no test input for day {day} of year {year}! Create a text file named '{year}/test{day:02d}{f"-{test_number}" if (test_number > -1) else ""}.txt'"
        )


def parse_input(
    puzzle_input: list[str],
    *delimiters: str,
    strip_lines: bool = True,
    cast_to: type = str,
) -> list:
    if len(delimiters) == 0:
        return [cast_to(line.strip() if strip_lines else line) for line in puzzle_input]
    else:
        return [
            _recursive_split(line.strip() if strip_lines else line, delimiters, cast_to)
            for line in puzzle_input
        ]


def parse_input_with_blocks(
    puzzle_input: list[str],
    *line_delimiters: str,
    block_delimiter: str = "",
    strip_lines: bool = True,
    cast_to: type = str,
) -> list[list]:
    blocks: list[list] = [[]]
    for line in [line.strip() if strip_lines else line for line in puzzle_input]:
        if line == block_delimiter:
            blocks.append([])
            continue

        if len(line_delimiters) == 0:
            blocks[-1].append(cast_to(line))
        else:
            blocks[-1].append(_recursive_split(line, line_delimiters, cast_to))

    return blocks


def parse_input_with_blocks_and_block_specific_line_delimiters(
    puzzle_input: list[str],
    *line_delimiters: tuple[str],
    block_delimiter: str = "",
    strip_lines: bool = True,
    cast_to: type = str,
) -> list[list]:

    block_idx = 0
    blocks: list[list] = [[]]

    if block_idx >= len(line_delimiters):
        raise ValueError(
            "There are more blocks in your puzzle input than defined groups of line delimiters."
        )

    for line in [line.strip() if strip_lines else line for line in puzzle_input]:
        if line == block_delimiter:
            blocks.append(list())
            block_idx += 1

            if block_idx >= len(line_delimiters):
                raise ValueError(
                    "There are more blocks in your puzzle input than defined groups of line delimiters."
                )

            continue

        if len(line_delimiters[block_idx]) == 0:
            blocks[-1].append(cast_to(line))
        else:
            blocks[-1].append(
                _recursive_split(line, line_delimiters[block_idx], cast_to)
            )

    return blocks


def _recursive_split(
    item: str, delimiters: tuple[str, *tuple[str, ...]], cast_to: type
) -> list:
    if len(delimiters) == 1:
        return [
            cast_to(subitem)
            for subitem in (
                item.split(delimiters[0]) if delimiters[0] != "" else item.split()
            )
        ]
    else:
        return [
            _recursive_split(subitem, delimiters[1:], cast_to)
            for subitem in (
                item.split(delimiters[0]) if delimiters[0] != "" else item.split()
            )
        ]
