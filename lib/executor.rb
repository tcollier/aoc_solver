require 'json'

class Executor
  def initialize(data, part1_proc, part2_proc)
    @data = data
    @part1_proc = part1_proc
    @part2_proc = part2_proc
  end

  def run(args)
    args[-1] == "--time" ? time : solve
  end

  def solve
    puts @part1_proc.call(@data.dup)
    puts @part2_proc.call(@data.dup)
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
    start_time = Time.now.to_f
    while continue_timing?(i, Time.now.to_f - start_time)
      fn.call(@data.dup)
      i += 1
    end
    {duration: ((Time.now.to_f - start_time) * 1_000_000).round, iterations: i}
  end
end
