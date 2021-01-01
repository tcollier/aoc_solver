INPUT = [14, 3, 1, 0, 9, 5]


def print_ans(input, num_rounds)
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
  puts curr_num
end

print_ans(INPUT, 30000000)
