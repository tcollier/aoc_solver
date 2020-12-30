class HashMap
  Entry = Struct.new(:key, :value, :next)

  def initialize
    @size = 11
    @entries = Array.new(@size)
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
      else
        @entries[bucket] = curr.next
      end
    elsif !value.nil?
      entry = Entry.new(key, value, curr&.next)
      if curr
        curr.next = entry
      else
        @entries[bucket] = entry
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
end
