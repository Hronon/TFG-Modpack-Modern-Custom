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

const removeCustomItems = (event) => {	
	event.add('c:hidden_from_recipe_viewers', /supplementaries.*/)
	event.remove('c:hidden_from_recipe_viewers', 'supplementaries:rope')
	event.remove('c:hidden_from_recipe_viewers', 'supplementaries:slice_map')

	// Mech Trowel
	event.add('c:hidden_from_recipe_viewers', 'mechtrowel:reach_upgrade_template')
	event.add('c:hidden_from_recipe_viewers', 'mechtrowel:variant_conversion_template')

	event.add('c:hidden_from_recipe_viewers', 'tfg:trowel')
}

ServerEvents.tags('item', event => {
	registerZiplines(event)
	removeCustomItems(event)
})