def prime?(num)
  (2..Math.sqrt(num).floor).each do |div|
    return false if num % div == 0
  end
  true
end

num = 12
while num < 1_000_000
  num -= 1 while !prime?(num)
  puts num
  num *= 2
end
