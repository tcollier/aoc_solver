require 'rspec/expectations'
require_relative 'hash_map'

RSpec::Matchers.define :be_a_list_of_length do |expected|
  match do |list|
    length = 0
    while list
      list = list.next
      length += 1
    end
    expected == length
  end
end

describe HashMap do
  HashableKey = Struct.new(:hash) do
    def ==(other)
      self.object_id == other.object_id
    end
  end

  subject(:map) { described_class.new }

  it 'retrieves nil if no value is stored' do
    expect(map[:a]).to be_nil

    ## Internal test
    stats = map.instance_variable_get('@stats')
    expect(stats[:a.hash % stats.length]).to eq(0)
    expect(map.instance_variable_get('@num_empty')).to eq(stats.length)
  end

  it 'retrieves a value stored in a key' do
    map[:a] = 314
    expect(map[:a]).to eq(314)

    ## Internal test
    entries = map.instance_variable_get('@entries')
    expect(entries[:a.hash % entries.length]).to be_a_list_of_length(1)
    stats = map.instance_variable_get('@stats')
    expect(stats[:a.hash % entries.length]).to eq(1)
    expect(map.instance_variable_get('@num_empty')).to eq(stats.length - 1)
  end

  it 'overwrites a value stored in the only key' do
    map[:a] = 314
    map[:a] = 42
    expect(map[:a]).to eq(42)

    ## Internal test
    entries = map.instance_variable_get('@entries')
    expect(entries[:a.hash % entries.length]).to be_a_list_of_length(1)
    stats = map.instance_variable_get('@stats')
    expect(stats[:a.hash % entries.length]).to eq(1)
    expect(map.instance_variable_get('@num_empty')).to eq(stats.length - 1)
  end

  it 'overwrites a value stored in a key at the head of the list' do
    key1 = HashableKey.new(0)
    key2 = HashableKey.new(0)
    map[key1] = 314
    map[key2] = 42
    map[key1] = 413
    expect(map[key1]).to eq(413)
    expect(map[key2]).to eq(42)

    ## Internal test
    entries = map.instance_variable_get('@entries')
    expect(entries[0]).to be_a_list_of_length(2)
    stats = map.instance_variable_get('@stats')
    expect(stats[0]).to eq(2)
    expect(map.instance_variable_get('@num_empty')).to eq(stats.length - 1)
  end

  it 'overwrites a value stored in a key at the tail of the list' do
    key1 = HashableKey.new(0)
    key2 = HashableKey.new(0)
    map[key1] = 314
    map[key2] = 42
    map[key2] = 24
    expect(map[key1]).to eq(314)
    expect(map[key2]).to eq(24)

    ## Internal test
    entries = map.instance_variable_get('@entries')
    expect(entries[0]).to be_a_list_of_length(2)
    stats = map.instance_variable_get('@stats')
    expect(stats[0]).to eq(2)
  end

  it 'clears a value not stored in a key' do
    map[:a] = nil
    expect(map[:a]).to be_nil
    expect(map.instance_variable_get('@num_empty')).to eq(described_class::SIZES[0])
  end

  it 'clears a value stored in the only key' do
    map[:a] = 314
    map[:a] = nil
    expect(map[:a]).to be_nil

    ## Internal test
    entries = map.instance_variable_get('@entries')
    expect(entries[:a.hash % entries.length]).to be_a_list_of_length(0)
    stats = map.instance_variable_get('@stats')
    expect(stats[:a.hash % entries.length]).to eq(0)
    expect(map.instance_variable_get('@num_empty')).to eq(stats.length)
  end

  it 'clears a value stored in a key at the head of the list' do
    key1 = HashableKey.new(0)
    key2 = HashableKey.new(0)
    map[key1] = 314
    map[key2] = 42
    map[key1] = nil
    expect(map[key1]).to be_nil
    expect(map[key2]).to eq(42)

    ## Internal test
    entries = map.instance_variable_get('@entries')
    expect(entries[0]).to be_a_list_of_length(1)
    stats = map.instance_variable_get('@stats')
    expect(stats[0]).to eq(1)
  end

  it 'clears a value stored in a key at the tail of the list' do
    key1 = HashableKey.new(0)
    key2 = HashableKey.new(0)
    map[key1] = 314
    map[key2] = 42
    map[key2] = nil
    expect(map[key1]).to eq(314)
    expect(map[key2]).to be_nil

    ## Internal test
    entries = map.instance_variable_get('@entries')
    expect(entries[0]).to be_a_list_of_length(1)
    stats = map.instance_variable_get('@stats')
    expect(stats[0]).to eq(1)
  end

  it 'stores values for two entries with different hashes' do
    key1 = HashableKey.new(0)
    key2 = HashableKey.new(1)
    map[key1] = 314
    map[key2] = 42
    expect(map[key1]).to eq(314)
    expect(map[key2]).to eq(42)

    ## Internal test
    entries = map.instance_variable_get('@entries')
    expect(entries[0]).to be_a_list_of_length(1)
    expect(entries[1]).to be_a_list_of_length(1)
    stats = map.instance_variable_get('@stats')
    expect(stats[0]).to eq(1)
    expect(stats[0]).to eq(1)
    expect(map.instance_variable_get('@num_empty')).to eq(stats.length - 2)
  end

  it 'stores values for two entries with the same hash' do
    key1 = HashableKey.new(0)
    key2 = HashableKey.new(0)
    map[key1] = 314
    map[key2] = 42
    expect(map[key1]).to eq(314)
    expect(map[key2]).to eq(42)

    ## Internal test
    entries = map.instance_variable_get('@entries')
    expect(entries[0]).to be_a_list_of_length(2)
    stats = map.instance_variable_get('@stats')
    expect(stats[0]).to eq(2)
  end

  it 'maintains entries after resizing' do
    map[:a] = 314
    map[:b] = 42

    orig_entries = map.instance_variable_get('@entries')
    map.send(:resize!)
    expect(map[:a]).to eq(314)
    expect(map[:b]).to eq(42)

    ## Internal test
    entries = map.instance_variable_get('@entries')
    expect(entries.length).to be > orig_entries.length
  end

  it 'maintains stats after resizing' do
    key1 = HashableKey.new(0)
    key2 = HashableKey.new(0)
    key3 = HashableKey.new(1)
    map[key1] = 314
    map[key2] = 42
    map[key3] = 13

    map.send(:resize!)

    ## Internal test
    stats = map.instance_variable_get('@stats')
    expect(stats[0]).to eq(2)
    expect(stats[1]).to eq(1)
    expect(map.instance_variable_get('@num_empty')).to eq(stats.length - 2)
  end
end
