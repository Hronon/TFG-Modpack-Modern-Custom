from collections import defaultdict
from pathlib import Path
from typing import Callable, Dict, List
import shutil
import subprocess
import re
import json


PWD = Path(__file__).resolve().parent.parent 	# tfg_custom_dev
CWD = Path(__file__).resolve().parent 			# tfg_custom_dev/scripts
PAKKU = PWD.parent

PROJECTS = PWD / 'projects.txt'
BACKUPS = PWD / 'backups'

REPLACE = PWD / 'replace_with_original'
DATA = PWD / 'data'


class ModMeta:
	_slug: str
	_cf_id: str
	_side: str

	def __init__(self, slug: str, cf_id: str, side: str) -> None:
		self._slug = slug
		self._cf_id = cf_id
		self._side = side

	@property
	def slug(self) -> str:
		return self._slug

	@property
	def id(self) -> str:
		return self._cf_id

	@property
	def side(self) -> str:
		if self._side not in ['CLIENT', 'SERVER']:
			return 'BOTH'
		return self._side

	def project(self) -> str:
		if self._cf_id:
			return f'{self._slug}:{self._cf_id}'

		return self._slug


def backup(target: str, dest: str, override_if_exist: bool = False):
	"""
	Copy `target` to backups folder under `dest`.\n
	Example:\n
	`backup('my_file.json', 'main_backup')` -> Saves `my_file.png` under `BACKUPS_FOLDER/main_backup/my_file.json`
	"""
	backup_to = BACKUPS / dest / target
	file = PAKKU / target

	if not file.exists():
		print(f'file not exist: {file}')
		return

	if backup_to.exists() and not override_if_exist:
		print('Backup already exist! Overriding disabled.')
		return

	backup_to.parent.mkdir(parents = True, exist_ok = True)
	shutil.copy2(file, backup_to)

def restore(path: str, name: str):
	backup = BACKUPS / name / path
	restore_to = PAKKU / path

	if not backup.exists():
		print(f'no backup for file: {path}')
		return

	shutil.copy2(backup, restore_to)

def replace(path: Path, replace_with: Path):
	if not path.exists() or not replace_with.exists():
		print(f'Can\'t replace file: {path}')
		return

	shutil.copy2(replace_with, path)

def update_pakku_paths():
	path = DATA.relative_to(PAKKU) / 'modpack'
	subprocess.run([
		'java', '-jar', 'pakku.jar', 'cfg', '--mods-path', path / 'mods',
	], check = True, cwd=PAKKU)

	subprocess.run([
		'java', '-jar', 'pakku.jar', 'cfg', '--resource-packs-path', path / 'resourcepacks',
	], check = True, cwd=PAKKU)

	subprocess.run([
		'java', '-jar', 'pakku.jar', 'cfg', '--shaders-path', path / 'shaderpacks',
	], check = True, cwd=PAKKU)

def fetch():
	subprocess.run([
		'java', '-jar', 'pakku.jar', 'fetch',
	], check = True, cwd=PAKKU)

def get_mods_data() -> Dict[str, str]:
	data = {}

	pakku_lock = PAKKU / 'pakku-lock.json'
	if not pakku_lock.exists():
		print('`pakku-lock.json` not exist!!!')
		return data

	with open(pakku_lock, 'r') as f:
		pakku_data = json.load(f)

	if not pakku_data:
		print('pakku-lock.json is empty!!!')
		return data

	for project in pakku_data['projects']:
		side = project.get('side', 'BOTH')
		slug = project['slug'].get('curseforge')
		if not slug:
			continue

		data[slug] = side

	return data

def update_pakku_config():
	# Change project info
	subprocess.run([
		'java', '-jar', 'pakku.jar', 'cfg',
		'--name', 'TFG-Custom',
		'--author', 'Hronon',
		'--description', 'Fork of TFG-Modern with custom changes',
	], check = True, cwd=PAKKU)

def update_target():
	# Change target
	subprocess.run([
		'java', '-jar', 'pakku.jar', 'set', '--target', 'curseforge'
	], check = True, cwd=PAKKU)

def add_mod(mod: ModMeta):
	subprocess.run([
		'java', '-jar', 'pakku.jar',
		'add', 'prj', '--curseforge', mod.project(),
	], check = True, input="Y\n", text = True, cwd=PAKKU)

def update_mod_side(mod: ModMeta):
	subprocess.run([
		'java', '-jar', 'pakku.jar',
		'cfg', 'prj', '--side', mod.side, mod.slug
	], check = True, cwd=PAKKU)

def update_mod(mod: ModMeta):
	subprocess.run([
		'java', '-jar', 'pakku.jar',
		'update', mod.project(),
	], check = True, input="Y\n", text = True, cwd=PAKKU)

def get_files_to_replace() -> list[str]:
	files = []
	for file in REPLACE.rglob("*"):
		if not file.is_file():
			continue
		files.append(str(file.relative_to(REPLACE)))

	return files

def replace_with_original(files: list[str], base: Path):
	for file in files:
		replace(base / file, REPLACE / file)

def get_mods() -> Dict[str, List[ModMeta]]:
	mods = defaultdict[str, List[ModMeta]](list)

	with open(PROJECTS, 'r') as f:
		while line := f.readline():
			print(f'Trying to add parse {line.strip()}')
			line = re.sub(r'\s+', '', line).split(':')

			if len(line) > 4:
				line = line[:4]

			while len(line) < 4:
				line.append('')

			action, slug, cf_id, side = line

			if action not in ['add', 'update', 'remove']:
				print(f'Action value must be [add|update|remove]. You provided: `{action}`. Defaulted to `add`')
				action = 'add'

			if not slug:
				print('Slug is required! Skipping')
				continue

			if cf_id and not cf_id.isnumeric():
				print(f'Curseforge project file id is not numeric: `{cf_id}`. Ignoring id')
				cf_id = ''

			mods[action].append(ModMeta(slug, cf_id, side))

	return mods

def install_mods():
	mods_data = get_mods_data()

	for action, mods in get_mods().items():
		for mod in mods:

			if mod.slug not in mods_data and action == 'add':
				add_mod(mod)
				mods_data[mod.slug] = 'BOTH'

			if mods_data[mod.slug] != mod.side:
				update_mod_side(mod)
