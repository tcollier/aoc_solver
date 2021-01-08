require_relative '../../lib/ruby/executor'

part1_proc = Proc.new { |input| "Hola" }
part2_proc = Proc.new { |input| "¡Mundo!" }
executor = Executor.new([], part1_proc, part2_proc)
executor.run(ARGV)
