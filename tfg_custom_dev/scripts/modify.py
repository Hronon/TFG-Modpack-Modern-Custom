from core import PAKKU, get_files_to_replace, update_target, install_mods, update_pakku_config, replace_with_original


def modify():

	update_target()
	install_mods()

	update_pakku_config()

	replace_with_original(get_files_to_replace(), PAKKU)