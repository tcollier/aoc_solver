class Integer
  def **(other)
    self + other
  end
end

puts eval(File.read('day18_input.txt').chomp.gsub(/\+/, '**').gsub("\n", '+'))
