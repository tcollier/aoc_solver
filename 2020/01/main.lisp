(defun get-numbers (filename)
    (sort
        (with-open-file (stream filename)
            (loop for line = (read-line stream nil)
                while line
                collect (parse-integer line)))
        #'<))

(defun find-pair (num remaining sum)
    (if (and num (first remaining))
        (if (= (+ num (first (last remaining))) sum)
            (list num (first (last remaining)))
            (if (< (+ num (first (last remaining))) sum)
                (find-pair (first remaining) (cdr remaining) sum)
                (find-pair num (reverse (cdr (reverse remaining))) sum)
                ))))

(defun find-triplet (num remaining sum)
    (if num
        (if (first (cdr (cdr remaining)))
            (if (= (+ num (first remaining) (first (last remaining))) sum)
                (list num (first remaining) (first (last remaining)))
                (if (< (+ num (first remaining) (first (last remaining))) sum)
                    (find-triplet num (cdr remaining) sum)
                    (find-triplet num (reverse (cdr (reverse remaining))) sum)
                )
            )
            (find-triplet (first remaining) (cdr remaining) sum)
        )
    )
)

(defun print-results (numbers sum)
    (format t "~D"
        (reduce #'* (find-pair (first numbers) (cdr numbers) sum) :initial-value 1))
    (fresh-line)
    (format t "~D"
        (reduce #'* (find-triplet (first numbers) (cdr numbers) sum) :initial-value 1))
    (fresh-line)
)
(print-results (get-numbers "2020/01/input.txt") 2020)
