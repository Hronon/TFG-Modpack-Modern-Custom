"use strict";

let ZIPLINES = [
	"tfc:metal/chain/bismuth_bronze",
	"tfc:metal/chain/black_bronze",
	"tfc:metal/chain/bronze",
	"tfc:metal/chain/copper",
	"tfc:metal/chain/wrought_iron",
	"tfc:metal/chain/steel",
	"tfc:metal/chain/black_steel",
	"tfc:metal/chain/blue_steel",
	"tfc:metal/chain/red_steel",
]

function registerZiplines(event) {
	ZIPLINES.forEach(item => {
		event.add('c:chains', item)	
	})
}

const removeSupplementariesItems = (event) => {	
	event.add('c:hidden_from_recipe_viewers', /supplementaries.*/)
	event.remove('c:hidden_from_recipe_viewers', 'supplementaries:rope')
	event.remove('c:hidden_from_recipe_viewers', 'supplementaries:slice_map')
}

ServerEvents.tags('item', event => {
	registerZiplines(event)
	removeSupplementariesItems(event)
})