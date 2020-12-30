require 'benchmark'
require_relative 'hash_map'

NUM_ITERATIONS = 100_000

hash = Hash.new
map = HashMap.new

Benchmark.bm(10) do |bm|
  bm.report('Hash set') { NUM_ITERATIONS.times { |i| hash[0] = i } }
  bm.report('HashMap set') { NUM_ITERATIONS.times { |i| map[0] = i } }
end

hash = Hash.new
hash[0] = :a
map = HashMap.new
map[0] = :a

Benchmark.bm(10) do |bm|
  bm.report('Hash get') { NUM_ITERATIONS.times { hash[0] } }
  bm.report('HashMap get') { NUM_ITERATIONS.times { map[0] } }
end

hash = Hash.new
map = HashMap.new

Benchmark.bm(16) do |bm|
  bm.report('Hash multi-set') { NUM_ITERATIONS.times { |i| hash[i] = i } }
  bm.report('HashMap multi-set') { NUM_ITERATIONS.times { |i| map[i] = i } }
end
