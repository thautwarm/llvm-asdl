import rbnf.zero as ze

ze_exp = ze.compile('import mlisp.mlisp.[*]', use='grammar')

s = ze_exp.match("""
(def f 
    (lambda (x, y) 
            (+ x y))
)

(let s 1)
(let f 1.0)
""")

print(s.result)
