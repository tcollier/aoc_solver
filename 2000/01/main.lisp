(load "ext/lisp/executor.lisp")

(set 'input (list "Hello" "World!"))

(defun part1 (input)
  (car input)
)

(defun part2 (input)
  (car (cdr input))
)


(executor input #'part1 #'part2 *posix-argv*)
