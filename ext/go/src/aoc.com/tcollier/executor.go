package tcollier

import (
	"fmt"
	"time"
)

type Input interface{}

type solverFunc func(Input) string

type timingInfo struct {
	Iterations uint32
	Duration   int64
}

func continueTiming(iterations uint32, duration int64) bool {
	if iterations < 100 {
		return duration < 30000000
	} else {
		return duration < 100000
	}
}
func timeFn(input Input, fn solverFunc) timingInfo {
	var i uint32
	var runningTime int64
	for continueTiming(i, runningTime) {
		var startTime = time.Now().UnixNano()
		fn(input)
		runningTime += (time.Now().UnixNano() - startTime) / 1000
		i++
	}
	return timingInfo{Iterations: i, Duration: runningTime}
}

// Executor runs the solver code
func Executor(input Input, part1 solverFunc, part2 solverFunc, args []string) {
	if len(args) >= 1 && args[len(args)-1] == "--time" {
		var part1Time = timeFn(input, part1)
		var part2Time = timeFn(input, part2)
		fmt.Printf("{\"part1\":{\"iterations\":%d,\"duration\":%d},\"part2\":{\"iterations\":%d,\"duration\":%d}}\n", part1Time.Iterations, part1Time.Duration, part2Time.Iterations, part2Time.Duration)
	} else {
		fmt.Println(part1(input))
		fmt.Println(part2(input))
	}
}
