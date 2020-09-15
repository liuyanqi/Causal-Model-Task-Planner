( define ( domain tower )
	; ( :predicates
	; 	( on ?x ?y )
    ;     ( flat-top ?x )
    ;     ( flat-bottom ?x )
    ;     ( stackable ?x ?y)
    ;     ( on-floor ?x )
    ;     ( on-top ?x )
    ;     ( height ?x )
	; )

	; ( :action stack
	; 	:parameters ( ?x ?y )
	; 	:precondition ( and
    ;         ( not ( = ?x ?y ) )
	; 		( on-floor ?x )
	; 		( on-top ?y )
	; 	)
	; 	:effect ( and
	; 		( not (on-top ?y ) )
	; 		( not (on-floor ?x ) )
    ;         ( on-top ?x )
	; 		( on ?x ?y )
	; 	)
    ;     :model (stack-model ?x ?y)
	; )

    (:model stack-model
        :parameters ( ?x ?y ) ; stack x on top of y

        (:cause stackable
            :relation ( and
                ( flat-bottom ?x )
                ( flat-top ?y )
            )
        )
        (:cause stack-tall
            :relation (stackable ?x ?y)
        )
        ; (:cause stack-heavy
        ;     :relation ( add
        ;         (1.0 (stackable ?x ?y))
        ;         (0.2 (weight ?x))
        ;         (0.2 (weight ?y))
        ;     )
        ; )
    )
)

; relation words
;   and, add