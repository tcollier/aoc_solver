package main

import (
	"bufio"
	"errors"
	"log"
	"os"
	"sort"
	"strconv"

	"aoc.com/tcollier"
)

type pair struct {
	a, b int
}

type triplet struct {
	a, b, c int
}

func pairWithSum(numbers []int, sum int) (pair, error) {
	others := make(map[int]bool)
	for i := 1; i < len(numbers); i++ {
		others[numbers[i]] = true
	}
	for i := 0; i < len(numbers)-1; i++ {
		if others[sum-numbers[i]] {
			return pair{numbers[i], sum - numbers[i]}, nil
		}
	}
	return pair{0, 0}, errors.New("Pair not found")
}

func tripletWithSum(numbers []int, sum int) (triplet, error) {
	sort.Ints(numbers)
	for i := 0; i < len(numbers)-2; i++ {
		for j, k := i+1, len(numbers)-1; j < k; {
			total := numbers[i] + numbers[j] + numbers[k]
			if total == sum {
				return triplet{numbers[i], numbers[j], numbers[k]}, nil
			} else if total < sum {
				j++
			} else {
				k--
			}
		}
	}
	return triplet{0, 0, 0}, errors.New("Triplet not found")
}

func loadNumbers(fn string) ([]int, error) {
	file, err := os.Open(fn)
	defer file.Close()
	if err != nil {
		return nil, err
	}

	var numbers = make([]int, 200)
	scanner := bufio.NewScanner(file)
	var index = 0
	for scanner.Scan() {
		number, err := strconv.Atoi(scanner.Text())
		if err != nil {
			return nil, err
		}
		if err := scanner.Err(); err != nil {
			return nil, err
		}

		numbers[index] = number
		index++
	}

	return numbers, nil
}

func part1Answer(input tcollier.Input) string {
	pair, err := pairWithSum(input.([]int), 2020)
	if err == nil {
		return strconv.Itoa(pair.a * pair.b)
	}
	return err.Error()
}

func part2Answer(input tcollier.Input) string {
	triplet, err := tripletWithSum(input.([]int), 2020)
	if err == nil {
		return strconv.Itoa(triplet.a * triplet.b * triplet.c)
	}
	return err.Error()
}

func main() {
	numbers, err := loadNumbers("2020/01/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	tcollier.Executor(numbers, part1Answer, part2Answer, os.Args)
}
