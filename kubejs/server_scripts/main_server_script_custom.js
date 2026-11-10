// priority: 2
"use strict";

ServerEvents.tags('item', event => {
})

ServerEvents.tags('block', event => {
	registerLivingWindTags(event)
})
