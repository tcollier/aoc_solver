class HashMap
  Entry = Struct.new(:key, :value, :next)

  SIZES = [
    11,
    19,
    37,
    71,
    139,
    277,
    547,
    1091,
    2179,
    4357,
    8713,
    17419,
    34819,
    69623,
  ]

  def initialize
    @size_index = 0
    @size = SIZES[@size_index]
    @entries = Array.new(@size)
    @stats = Array.new(@size) { 0 }
    @num_empty = @size
  end

  def [](key)
    bucket = key.hash % @size
    curr = @entries[bucket]
    curr = curr.next while curr && curr.key != key
    curr && curr.value
  end

  def []=(key, value)
    bucket = key.hash % @size
    prev = nil
    curr = @entries[bucket]
    while curr && curr.next && curr.key != key
      prev = curr
      curr = curr.next
    end
    if curr && curr.key == key
      if !value.nil?
        curr.value = value
      elsif prev
        prev.next = curr.next
        @stats[bucket] -= 1
        @num_empty += 1 if @stats[bucket] == 0
      else
        @entries[bucket] = curr.next
        @stats[bucket] -= 1
        @num_empty += 1 if @stats[bucket] == 0
      end
    elsif !value.nil?
      entry = Entry.new(key, value, curr&.next)
      @stats[bucket] += 1
      if curr
        curr.next = entry
      else
        @entries[bucket] = entry
      end
      if @stats[bucket] == 1
        @num_empty -= 1
        resize! if @num_empty == 0
      end
    end
  end

  def to_s
    str = '{'
    first = true
    @entries.each do |entry|
      while entry
        if first
          first = false
        else
          str += ', '
        end
        str += "#{entry.key.inspect} => #{entry.value.inspect}"
        entry = entry.next
      end
    end
    str + '}'
  end

  private

  def resize!
    return if @size_index == SIZES.length - 1
    old_entries = @entries
    @size_index += 1
    @size = SIZES[@size_index]
    @entries = Array.new(@size)
    @stats = Array.new(@size) { 0 }
    @num_empty = @size
    old_entries.each do |entry|
      while entry
        self[entry.key] = entry.value
        entry = entry.next
      end
    end
  end
end
