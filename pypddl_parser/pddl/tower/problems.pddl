(define (problem tower-1)
(:domain tower)
; (:objects
; 	block1
;     block2
;     block3
; )
; (:init ( and
; 	(on-floor block1)
;     (on-floor block2)
;     (on-floor block3)
;     (height 1.0 block1)
;     (height 1.0 block2)
;     (height 1.5 block3) )
; )
(:goal (> 3 
    (+ (height block1) (height block2) (height block3))
))
(:hint stack-tall)

)
