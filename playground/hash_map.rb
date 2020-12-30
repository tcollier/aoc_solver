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
    139241,
    278479,
  ]

  def initialize
    @size_index = 0
    @size = SIZES[@size_index]
    @entries = Array.new(@size)
    @prealloc_entries = Array.new(3 * @size) { Entry.new }
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
        @prealloc_entries.push(curr)
      else
        @entries[bucket] = curr.next
        @prealloc_entries.push(curr)
      end
    elsif !value.nil?
      entry = @prealloc_entries.pop
      entry.key = key
      entry.value = value
      entry.next = curr&.next
      if curr
        curr.next = entry
      else
        @entries[bucket] = entry
      end
      resize! if @prealloc_entries.empty?
    end
  end

  def inspect
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
    if @size_index == SIZES.length - 1
      @prealloc_entries = Array.new(@size * 5) { Entry.new }
      return
    end
    old_entries = @entries
    @size_index += 1
    @size = SIZES[@size_index]
    @prealloc_entries = Array.new(@size * 2) { Entry.new }
    @entries = Array.new(@size)
    old_entries.each do |entry|
      while entry
        old_next = entry.next
        new_bucket = entry.key.hash % @size
        entry.next = @entries[new_bucket]
        @entries[new_bucket] = entry
        entry = old_next
      end
    end
  end
end
