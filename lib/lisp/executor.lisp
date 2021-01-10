(defun time-fn (input fn iterations start-time duration)
  (if (or (and (< iterations 100) (< duration 30000)) (< duration 100))
    (progn
      (funcall fn input)
      (time-fn input fn (+ iterations 1) start-time (- (get-internal-real-time) start-time))
    )
    (list iterations duration)
  )
)

(defun print-timing (part1-results part2-results)
  (progn
    (princ
      (concatenate 'string
        "{\"part1\":{\"iterations\":"
        (write-to-string (car part1-results))
        ",\"duration\":"
        (write-to-string (car (cdr part1-results)))
        "},\"part2\":{\"iterations\":"
        (write-to-string (car part2-results))
        ",\"duration\":"
        (write-to-string (car (cdr part2-results)))
        "}}"
      )
    )
    (terpri)
  )
)

(defun executor (input part1-fn part2-fn args)
  (if (string= "--time" (car (reverse *posix-argv*)))
    (print-timing
      (time-fn input part1-fn 0 (get-internal-real-time) 0)
      (time-fn input part2-fn 0 (get-internal-real-time) 0)
    )
    (mapcar (lambda (fn) (progn (princ (funcall fn input)) (terpri))) (list part1-fn part2-fn))
  )
)
