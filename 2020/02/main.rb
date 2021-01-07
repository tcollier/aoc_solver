require_relative '../../lib/ruby/executor'

module Part1Validator
  def self.valid?(min, max, char, pwd)
    num_chars = pwd.chars.count { |c| c == char }
    num_chars >= min && num_chars <= max
  end
end

module Part2Validator
  def self.valid?(pos1, pos2, char, pwd)
    (pwd[pos1 - 1] == char) != (pwd[pos2 - 1] == char)
  end
end

def count_valid(input, validator)
  input.count do |line|
    match = line.match(/^(\d+)-(\d+) (\w): (\w+)$/)
    validator.valid?(Integer(match[1]), Integer(match[2]), match[3], match[4])
  end
end

part1_proc = Proc.new { |input| count_valid(input, Part1Validator) }
part2_proc = Proc.new { |input| count_valid(input, Part2Validator) }
executor = Executor.new(
  File.readlines(File.join(File.dirname(__FILE__), 'input.txt')).map(&:rstrip),
  part1_proc,
  part2_proc
)
executor.run(ARGV)
