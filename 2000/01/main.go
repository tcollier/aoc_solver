package main

import (
	"os"

	"aoc.com/tcollier"
)

func part1Answer(input tcollier.Input) string {
	return input.([]string)[0]
}

func part2Answer(input tcollier.Input) string {
	return input.([]string)[1]
}

func main() {
	tcollier.Executor([]string{"Hello", "World!"}, part1Answer, part2Answer, os.Args)
}
