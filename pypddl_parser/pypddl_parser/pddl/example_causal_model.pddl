( define  ( domain tower )
	(:model stack
		:parameters (?blockone ?blocktwo)

		(:cause stackable 
			:relation ( and 
					( flat_top ?blockone )
					( flat_bottom ?blocktwo )
				)
		)
	)
)