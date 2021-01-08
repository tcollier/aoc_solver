require_relative '../../lib/ruby/executor'

part1_proc = Proc.new { |input| "Fails" }
part2_proc = Proc.new { |input| "Validation" }
executor = Executor.new(%w[], part1_proc, part2_proc)
executor.run(ARGV)
