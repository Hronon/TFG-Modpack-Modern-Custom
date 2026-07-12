// priority: 0
"use strict";


const registerCustomRecipes = (event) => 
{
	// Supplementaries
	event.remove({ id: 'supplementaries:rope' })
	event.remove({ id: 'supplementaries:slice_map' })

	//# rope
	event.shapeless('3x supplementaries:rope', ['firmaciv:rope_coil']).id('tfg:shapeless/firmaciv_rope_to_supplementaries_rope')
	event.shaped('firmaciv:rope_coil', [
		'AAA',
	], {
		A: 'supplementaries:rope',
	}).id('tfg:shaped/supplementaries_rope_to_firmaciv_rope')

	//# slice map
	event.shapeless('supplementaries:slice_map', ['minecraft:map']).id('tfg:shapeless/supplementaries_slice_map')
	event.shapeless('minecraft:map', ['supplementaries:slice_map']).id('tfg:shapeless/supplementaries_slice_map_to_map')


	// Map Atlases 
	event.remove({ mod: 'map_atlases' })
	event.shapeless('map_atlases:atlas', [
		'minecraft:writable_book', 
		'tfc:glue',
		'minecraft:map'
	]).id('tfg:shapeless/map_atlas')


	// Mech Trowel

	//# Trowel
	event.remove({ id: 'mechtrowel:mech_trowel' })
	event.remove({ input: 'mechtrowel:reach_upgrade_template' })
	event.remove({ input: 'mechtrowel:variant_conversion_template' })
	event.remove({ output: 'mechtrowel:wand_template' })

	event.shapeless('mechtrowel:mech_trowel', [
		'tfg:trowel',
		'#gtceu:circuits/lv',
		'#forge:cogwheels',
		'#forge:tools/wrenches'
	]).id('tfg:shapeless/mechtrowel')

	//# Templates
	event.shaped('mechtrowel:wand_template', [
		' A ',
		' PA',
		'S  '
	], {
		A: 'constructionwand:diamond_wand',
		P: '#forge:ender_pearls',
		S: 'minecraft:stick'
	}).id('tfg:shaped/trowel/wand_template')

	event.shaped('mechtrowel:wand_capacity_template', [
		' A ',
		' PA',
		'S  '
	], {
		A: 'constructionwand:infinity_wand',
		P: '#forge:ender_pearls',
		S: 'minecraft:stick'
	}).id('tfg:shaped/trowel/wand_capacity_template')

	// Simple Voice Radio
	event.remove({ mod: 'simpleradio' })

	//# Speaker
	event.shaped('simpleradio:speaker', [
		' A ',
		'BCB',
		' D '
	], {
		A: 'minecraft:note_block',
		B: 'simpleradio:copper_wire',
		C: 'gtceu:mv_machine_casing',
		D: '#gtceu:circuits/mv',
	}).id('tfg:shaped/simpleradio/speaker')

	//# Speaker Module
	event.shapeless('simpleradio:speaker_module', [
		"minecraft:note_block",
		"create:electron_tube"
	]).id('tfg:shapeless/simpleradio/speaker_module')

	//# Listener Module
	event.shapeless('simpleradio:listener_module', [
		"minecraft:jukebox",
		"create:electron_tube"
	]).id('tfg:shapeless/simpleradio/listener_module')

	//# Antenna
	event.shaped('simpleradio:antenna', [
		'TAT',
		' A ',
		' A '
	], {
		A: 'minecraft:iron_ingot',
		T: 'create:transmitter',
	}).id('tfg:shaped/simpleradio/antenna')

	//# Wire
	event.shapeless('simpleradio:copper_wire', [
		"gtceu:fine_copper_wire",
	]).id('tfg:shapeless/simpleradio/wire')

	//# Microphone
	event.shaped('simpleradio:microphone', [
		' A ',
		'BCD',
		' E '
	], {
		A: '#minecraft:wool',
		B: 'create:electron_tube',
		C: 'simpleradio:listener_module',
		D: 'simpleradio:copper_wire',
		E: '#gtceu:circuits/lv',
	}).id('tfg:shaped/simpleradio/microphone')

	//# Radio
	event.shaped('simpleradio:radio', [
		' TA',
		'EIW',
		' S '
	], {
		A: 'simpleradio:antenna',
		T: 'create:transmitter',
		S: 'simpleradio:speaker_module',
		W: 'simpleradio:copper_wire',
		E: 'create:electron_tube',
		I: '#gtceu:circuits/lv'
	}).id('tfg:shaped/simpleradio/radio')

	//# Transmitter
	event.shaped('simpleradio:transmitter', [
		' AB',
		'QIT',
		' W '
	], {
		A: 'simpleradio:antenna',
		T: 'create:transmitter',
		W: 'simpleradio:copper_wire',
		Q: 'minecraft:quartz',
		I: 'minecraft:iron_block',
		B: '#forge:tools/wrenches'
	}).id('tfg:shaped/simpleradio/transmitter')
	event.shapeless('simpleradio:transmitter', [
		"simpleradio:receiver",
	]).id('tfg:shapeless/simpleradio/transmitter')

	//# Receiver
	event.shaped('simpleradio:receiver', [
		'BA ',
		'QIT',
		' W '
	], {
		A: 'simpleradio:antenna',
		T: 'create:transmitter',
		W: 'simpleradio:copper_wire',
		Q: 'minecraft:quartz',
		I: 'minecraft:iron_block',
		B: '#forge:tools/wrenches'
	}).id('tfg:shaped/simpleradio/receiver')
	event.shapeless('simpleradio:receiver', [
		"simpleradio:transmitter",
	]).id('tfg:shapeless/simpleradio/receiver')

	//# Transceiver
	event.shaped('simpleradio:transceiver', [
		'AL ',
		'TIT',
		' S '
	], {
		A: 'simpleradio:antenna',
		T: 'create:transmitter',
		L: 'simpleradio:listener_module',
		S: 'simpleradio:speaker_module',
		I: '#gtceu:circuits/lv',
	}).id('tfg:shaped/simpleradio/transceiver')
}