(defun time-one (input fn iterations duration)
  (if (or (and (< iterations 100) (< duration < 30000)) (< duration 100))
    (progn
      (set' start-time (get-internal-real-time))
      (call-with-timing fn input)
      (time-one input fn (+ iterations 1) (+ duration (- (now) start-time))
    )
    (list iterations duration)
  )
)

(defun time-both (input part1-fn part2-fn)
  (list '("part1" part1-fn) '("part2" part2-fn))
)

(defun executor (input part1-fn part2-fn args)
  (if (string= "--time" (car (reverse *posix-argv*)))
    (progn (princ (time-both input part1-fn part-2fn)) (terpri))
    (mapcar (lambda (fn) (progn (princ (funcall fn input)) (terpri))) (list part1-fn part2-fn))
  )
)

(set 'input (list "Hello" "World!"))

(defun part1 (input)
  (car input)
)

(defun part2 (input)
  (car (cdr input))
)


(executor input #'part1 #'part2 *posix-argv*)
