(load "lib/lisp/executor.lisp")

(defun get-numbers (filename)
    (sort
        (with-open-file (stream filename)
            (loop for line = (read-line stream nil)
                while line
                collect (parse-integer line)
            )
        )
        #'<
    )
)

(defun find-pair (num remaining sum)
    (if (and num (car remaining))
        (if (= (+ num (car (last remaining))) sum)
            (list num (car (last remaining)))
            (if (< (+ num (car (last remaining))) sum)
                (find-pair (car remaining) (cdr remaining) sum)
                (find-pair num (reverse (cdr (reverse remaining))) sum)
            )
        )
    )
)

(defun find-triplet (num remaining sum)
    (if num
        (if (car (cddr remaining))
            (if (= (+ num (car remaining) (car (last remaining))) sum)
                (list num (car remaining) (car (last remaining)))
                (if (< (+ num (car remaining) (car (last remaining))) sum)
                    (find-triplet num (cdr remaining) sum)
                    (find-triplet num (reverse (cdr (reverse remaining))) sum)
                )
            )
            (find-triplet (car remaining) (cdr remaining) sum)
        )
    )
)


(defun part1 (numbers)
  (reduce #'* (find-pair (car numbers) (cdr numbers) 2020) :initial-value 1)
)

(defun part2 (numbers)
  (reduce #'* (find-triplet (car numbers) (cdr numbers) 2020) :initial-value 1)
)


(executor (get-numbers "2020/01/input.txt") #'part1 #'part2 *posix-argv*)
