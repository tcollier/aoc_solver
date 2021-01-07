require 'json'

class Executor
  def initialize(input, part1_proc, part2_proc)
    @input = input
    @part1_proc = part1_proc
    @part2_proc = part2_proc
  end

  def run(args)
    args[-1] == "--time" ? time : solve
  end

  def solve
    puts @part1_proc.call(@input.dup)
    puts @part2_proc.call(@input.dup)
  end

  private

  def time
    puts JSON.generate({
      part1: time_proc(@part1_proc),
      part2: time_proc(@part2_proc)
    })
  end

  def continue_timing?(iterations, duration)
    if iterations < 100
      return duration < 30
    else
      return duration < 0.1
    end
  end

  def time_proc(fn)
    i = 0
    running_time = 0
    while continue_timing?(i, running_time)
      input = @input.dup
      start_time = Time.now.to_f
      fn.call(input)
      running_time += Time.now.to_f - start_time
      i += 1
    end
    {duration: running_time * 1_000_000, iterations: i}
  end
end
