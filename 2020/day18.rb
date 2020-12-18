class Integer
  def **(other)
    self + other
  end
end

total = 0
File.open('day18_input.txt', 'r').each do |line|
  total += eval(line.gsub(/\+/, '**'))
end
puts total
