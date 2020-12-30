require 'benchmark'
require_relative 'hash_map'

NUM_ITERATIONS = 1_000_000

WIDTH = 20

Benchmark.bm(WIDTH) do |bm|
  bm.report('Hash init') do
    NUM_ITERATIONS.times { Hash.new }
  end
  bm.report('HashMap init') do
    NUM_ITERATIONS.times { HashMap.new }
  end
end

num_iterations = NUM_ITERATIONS
while num_iterations >= 1
  num_keys = NUM_ITERATIONS / num_iterations

  hash_map_entries = num_keys.times.map { |i| [i, i] }
  hash_entries = hash_map_entries.flatten
  Benchmark.bm(WIDTH) do |bm|
    bm.report("Hash #{num_keys}-init") do
      num_iterations.times { Hash.new[hash_entries] }
    end
    bm.report("HashMap #{num_keys}-init") do
      num_iterations.times { HashMap.new(hash_map_entries) }
    end
  end

  hash = Hash.new
  map = HashMap.new

  Benchmark.bm(WIDTH) do |bm|
    bm.report("Hash #{num_keys}-set") do
      num_iterations.times do
        num_keys.times { |i| hash[i] = i }
      end
    end
    bm.report("HashMap #{num_keys}-set") do
      num_iterations.times do
        num_keys.times { |i| map[i] = i }
      end
    end
  end

  Benchmark.bm(WIDTH) do |bm|
    bm.report("Hash #{num_keys}-get") do
      num_iterations.times do
        num_keys.times { |i| hash[i] }
      end
    end
    bm.report("HashMap #{num_keys}-get") do
      num_iterations.times do
        num_keys.times { |i| map[i] }
      end
    end
  end

  num_iterations /= 100
end
