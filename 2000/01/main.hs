part1 input = "Hello"
part2 input = "World!"

-- executor :: [String] -> ([String] -> String) -> ([String] -> String) -> void
-- executor input part1Fn part2Fn args = do
--   part1Output <- part1Fn input
--   putStrLn part1Output
--   part2Output <- part2Fn input
--   putStrLn part2Output

main = do
  -- input <- ["Hello", "World!"]
  -- part1Output <- part1 input
  putStrLn "Hello"
  -- part2Output <- part2 input
  putStrLn "World!"
  -- executor ["Hello", "World!"] part1 part2
