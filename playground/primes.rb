def prime?(num)
  (2..Math.sqrt(num).floor).each do |div|
    return false if num % div == 0
  end
  true
end

num = 12
while num < 10_000_000
  num -= 1 while !prime?(num)
  puts num
  num *= 2
end

def factors(num)
  (2..Math.sqrt(num).floor).each do |div|
    if num % div == 0
      return [div, *factors(num / div)]
    end
  end
  num
end

num = 2338981840289282470
puts factors(num).join(' * ') + " = #{num}"
