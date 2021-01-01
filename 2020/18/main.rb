class Integer
  def /(other)
    self + other
  end

  def **(other)
    self + other
  end
end

puts eval(File.read(File.join(File.dirname(__FILE__), 'input.txt')).chomp.gsub(/\+/, '/').gsub("\n", '+'))

puts eval(File.read(File.join(File.dirname(__FILE__), 'input.txt')).chomp.gsub(/\+/, '**').gsub("\n", '+'))
