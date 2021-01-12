require 'aoc_executor'

part1_proc = Proc.new { |input| input[0] }
part2_proc = Proc.new { |input| input[1] }
executor = AocExecutor.new(%w[Hello World!], part1_proc, part2_proc)
executor.run(ARGV)
