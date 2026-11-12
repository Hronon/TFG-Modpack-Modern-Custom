from pathlib import Path
import shutil
from typing import Dict, Optional, List
import click
import json

from core import (
	DATA, BACKUPS, PWD,
	backup as core_backup,
	restore as core_restore,
	install_mods,
	update_target,
	update_pakku_paths,
	fetch,
	replace_with_original,
	get_files_to_replace,
)

CONFIG = PWD / 'config.json'

def load_config() -> Dict:
	cfg = {}

	if not CONFIG.exists():
		return cfg

	try:
		with open(CONFIG, 'r') as f:
			cfg = json.load(f)
	except json.JSONDecodeError:
		...

	return cfg

def save_config(cfg: Dict):
	CONFIG.parent.mkdir(parents = True, exist_ok = True)

	data = load_config()
	data.update(cfg)

	with open(CONFIG, 'w+') as f:
		json.dump(data, f, indent = 4)

def create_soft_links(target: Path):
	mp = DATA / 'modpack'
	mods = mp / 'mods'
	rp = mp / 'resourcepacks'
	sp = mp / 'shaderpacks'

	if mp.exists():
		shutil.rmtree(mp)

	mp.mkdir(parents = True, exist_ok = True)

	mods.symlink_to(target / 'mods', True)
	rp.symlink_to(target / 'resourcepacks', True)
	sp.symlink_to(target / 'shaderpacks', True)

def copy_to_modpack():
	...

def check_for_pakku_backup() -> bool:
	files = [
		"pakku.json",
		"pakku-lock.json"
	]

	for file in files:
		if not (BACKUPS / 'original' / file).exists():
			return False

	return True

@click.group()
@click.pass_context
def cli(ctx: click.Context):
	ctx.ensure_object(dict)

	ctx.obj['config'] = {}
	ctx.obj['config'].update(load_config())

@cli.command()
@click.pass_context
@click.option('--modpack-loc', type = click.Path(path_type = Path))
def setup_dev(ctx: click.Context, modpack_loc: Optional[Path]):
	if not check_for_pakku_backup():
		click.echo('Pakku files backups not found. Use `backup` command before using `setup-dev`')
		return

	if not modpack_loc:
		modpack_loc = ctx.obj['config'].get('modpack_location')

	if not modpack_loc:
		click.echo('Modpack location not set. Stopping.\nConsider using `--modpack-loc` option only for current execution or `config` command for every execution')
		return

	modpack_loc = Path(modpack_loc).expanduser().resolve()

	if not modpack_loc.is_dir():
		click.echo(f'Provided modpack location is not a directory: {modpack_loc}. Stopping.')
		return

	if not modpack_loc.exists():
		click.echo(f'Provided modpack location not exist: {modpack_loc}. Stopping.')
		return

	update_target()
	replace_with_original(get_files_to_replace(), modpack_loc)
	create_soft_links(modpack_loc)
	update_pakku_paths()

@cli.command()
@click.option('-n', '--name', type = str, default = 'original')
def restore(name: str):
	backup_files = [
		"pakku.json",
		"pakku-lock.json"
	]

	if not name:
		click.echo("Name must be non empty string. Aborting")
		return

	for file in backup_files:
		core_restore(file, name)

@cli.command()
@click.option('-n', '--name', type = str, default = 'original')
@click.option('-o', '--override-exist', is_flag = True, default = False)
def backup(name: str, override_exist: bool):
	backup_files = [
		"pakku.json",
		"pakku-lock.json"
	]

	if not name:
		click.echo("Name must be non empty string. Aborting")
		return

	for file in backup_files:
		core_backup(file, name, override_exist)

@cli.command()
def install():
	install_mods()
	fetch()

@cli.command()
@click.option('--modpack-loc', type = click.Path(path_type = Path))
def config(modpack_loc: Optional[Path]):
	cfg = {}

	if modpack_loc:
		cfg['modpack_location'] = str(modpack_loc.expanduser().resolve())

	save_config(cfg)

if __name__ == "__main__":
	cli()