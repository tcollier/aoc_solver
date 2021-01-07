require_relative '../../lib/ruby/executor'

def play(input, num_rounds)
  last_usage = Array.new(num_rounds) { -1 }
  (input.length - 1).times do |i|
    last_usage[input[i]] = i
  end

  prev_num = input.last
  curr_num = nil
  (input.length..(num_rounds - 1)).each do |i|
    if last_usage[prev_num] >= 0
      curr_num = i - 1 - last_usage[prev_num]
    else
      curr_num = 0
    end
    last_usage[prev_num] = i - 1
    prev_num = curr_num
  end
  curr_num
end

part1_proc = Proc.new { |input| play(input, 2020) }
part2_proc = Proc.new { |input| play(input, 30000000) }
executor = Executor.new([14, 3, 1, 0, 9, 5], part1_proc, part2_proc)
executor.run(ARGV)
