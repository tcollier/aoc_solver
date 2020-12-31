require 'set'

INPUT = File.readlines('day01_input.txt').map(&:to_i)

def pair_with_sum(numbers, sum)
  others = Set.new(numbers[1..-1])
  numbers.each do |number|
    if others.include?(sum - number)
      return [number, sum - number]
    end
  end
  raise "No pair with sum #{sum} found"
end

def triplet_with_sum(numbers, sum)
  numbers.sort!
  (numbers.length - 2).times do |i|
    j = i + 1
    k = numbers.length - 1
    while j < k
      total = numbers[i] + numbers[j] + numbers[k]
      if total == sum
        return [numbers[i], numbers[j], numbers[k]]
      elsif total < sum
        j += 1
      else
        k -= 1
      end
    end
  end
  raise "No triplet with sum #{sum} found"
end

pair = pair_with_sum(INPUT, 2020)
puts pair[0] * pair[1]

triplet = triplet_with_sum(INPUT, 2020)
puts triplet[0] * triplet[1] * triplet[2]
