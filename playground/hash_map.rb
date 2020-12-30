# It's like a Hash, but slower!
class HashMap
  # A linked list item that stores the entry
  Entry = Struct.new(:key, :value, :next)
  private_constant :Entry

  # Each item is a tuple where the first value is the size of an entries array
  # and the second value is the number of entries to pre-allocate. The first
  # entry array size is a good overall default value and each subsequent value
  # is the first prime number less than twice its previous.
  SIZES = [
    [11, 3],
    [19, 5],
    [37, 8],
    [71, 10],
    [139, 15],
    [277, 20],
    [547, 25],
    [1091, 30],
    [2179, 30],
    [4357, 30],
    [8713, 50],
    [17419, 100],
    [34819, 200],
    [69623, 400],
  ]
  private_constant :SIZES

  def initialize
    @size_index = 0
    @size = SIZES[@size_index][0]
    @entries = Array.new(@size)

    # Pre-allocated a bunch of entries so that they are more likely to be in
    # contiguous memory and thus reads should be faster.
    @prealloc_entries = Array.new(SIZES[@size_index][1]) { Entry.new }
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
      # If an existing entry with the same key was found
      if !value.nil?
        # If the value is getting overwritten
        curr.value = value
      elsif prev
        # If the value is getting removed from the cdr of the list
        prev.next = curr.next
        @prealloc_entries.push(curr)
      else
        # If the value is getting removed from the head of the list
        @entries[bucket] = curr.next
        @prealloc_entries.push(curr)
      end
    elsif !value.nil?
      # If we're setting a new value, use on the of pre-allocated entries
      entry = @prealloc_entries.pop
      entry.key = key
      entry.value = value
      entry.next = curr&.next
      if curr
        # If the value is getting set at the tail of the list
        curr.next = entry
      else
        # If this is the first entry for the bucket
        @entries[bucket] = entry
      end
      resize! if @prealloc_entries.empty?
    end
    value
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
      # If we've run out of sizes to grow into, simply refill the pre-allocated
      # entries and return
      @prealloc_entries = Array.new(SIZES[@size_index][1]) { Entry.new }
      return
    end

    # Save these for later, since we'll overwrite `@entries`
    old_entries = @entries
    @size_index += 1
    @size = SIZES[@size_index][0]
    @prealloc_entries = Array.new(SIZES[@size_index][1]) { Entry.new }
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
