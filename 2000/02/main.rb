require_relative '../../ext/ruby/executor'

part1_proc = Proc.new { |input| "Hello" }
part2_proc = Proc.new { |input| "World" }
executor = Executor.new(%w[], part1_proc, part2_proc)
executor.run(ARGV)
