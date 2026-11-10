from pathlib import Path
import subprocess
import sys
import shutil
from typing import List, Optional
import re

PWD = Path(__file__).resolve().parent
PROJECTS = PWD / 'projects.txt'
BACKUPS = PWD / 'project_backups'
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

def backup(path: str):
	backup_to = BACKUPS / path
	backup_to = backup_to.with_suffix(backup_to.suffix + '.bak')
	file = PWD / path

	if not file.exists():
		print(f'file not exist: {file}')
		return

	backup_to.parent.mkdir(parents = True, exist_ok = True)
	shutil.copy2(file, backup_to)

def restore(path: str):
	backup = BACKUPS / path
	backup = backup.with_suffix(backup.suffix + '.bak')
	restore_to = PWD / path

	if not backup.exists():
		print(f'no backup for file: {restore_to}')
		return

	shutil.move(backup, restore_to)

def replace(path: Path, replace_with: Path):
	if not path.exists() or not replace_with.exists():
		print(f'Can\'t replace file: {path}')
		return

	shutil.copy2(replace_with, path)

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

def add_mod(mod: ModMeta):
	subprocess.run([
		'java', '-jar', 'pakku.jar',
		'add', 'prj', '--curseforge', mod.project(),
	], check = True, input="Y\n", text = True, cwd=PWD)

	if mod.side == 'BOTH':
		return

	subprocess.run([
		'java', '-jar', 'pakku.jar',
		'cfg', 'prj', '--side', mod.side, mod.slug
	], check = True, cwd=PWD)

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

def fetch():
	subprocess.run([
		'java', '-jar', 'pakku.jar', 'cfg', '--mods-path', 'data/modpack/mods/',
	], check = True, cwd=PWD)

	subprocess.run([
		'java', '-jar', 'pakku.jar', 'cfg', '--resource-packs-path', 'data/modpack/resourcepacks/',
	], check = True, cwd=PWD)

	subprocess.run([
		'java', '-jar', 'pakku.jar', 'cfg', '--shaders-path', 'data/modpack/shaderpacks/',
	], check = True, cwd=PWD)

	subprocess.run([
		'java', '-jar', 'pakku.jar', 'fetch',
	], check = True, cwd=PWD)

def update_pakku_config():
	# Change project info
	subprocess.run([
		'java', '-jar', 'pakku.jar', 'cfg',
		'--name', 'TFG-Custom',
		'--author', 'Hronon',
		'--description', 'Fork of TFG-Modern with custom changes',
	], check = True, cwd=PWD)

def update_target():
	# Change target
	subprocess.run([
		'java', '-jar', 'pakku.jar', 'set', '--target', 'curseforge'
	], check = True, cwd=PWD)

def get_mods() -> List[ModMeta]:
	mods = []
	with open(PROJECTS, 'r') as f:
		while line := f.readline():
			print(f'Trying to add parse {line.strip()}')
			line = re.sub(r'\s+', '', line).split(':')

			if len(line) > 3:
				line = line[:3]

			while len(line) < 3:
				line.append('')

			slug, cf_id, side = line
			if not slug:
				print('Slug is required! Skipping')
				continue

			if cf_id and not cf_id.isnumeric():
				print(f'Curseforge project file id is not numeric: {cf_id}. Skipping')
				continue

			mods.append(ModMeta(slug, cf_id, side))
	return mods

def modify(replace: list[str], base: Path):

	update_target()
	for mod in get_mods():
		add_mod(mod)

	update_pakku_config()

	replace_with_original(replace, base)

def setup_dev(modpack_location: Path):
	backup_files = [
		"pakku.json",
		"pakku-lock.json"
	]

	try:
		for file in backup_files:
			backup(file)

		update_target()
		for mod in get_mods():
			add_mod(mod)
			
		replace_with_original(get_files_to_replace(), modpack_location)

		create_soft_links(modpack_location)
		fetch()

	finally:
		for file in backup_files:
			restore(file)

		if BACKUPS.exists():
			shutil.rmtree(BACKUPS)

def get_dev_modpack_location() -> Optional[Path]:
	mld = DATA / 'modpack_location_dev'

	if not mld.exists():
		print('dev modpack location not set.\nUse `dev.py set "path_to_modpack"` (where folders like "mods" located)')
		return

	with open(mld, 'r') as f:
		modpack_folder = f.read().strip()

	if not modpack_folder:
		print('dev modpack location not set.\nUse `dev.py set "path_to_modpack"` (where folders like "mods" located)')
		return

	modpack_folder = Path(modpack_folder).expanduser().resolve()
	if not (modpack_folder.exists() and modpack_folder.is_dir()):
		print(f'Path not exist or Path is not directory. You provided: {modpack_folder}\nRerun `set` command with correct path')
		return

	return modpack_folder

def set_dev_modpack_location(path: str):
	mld = DATA / 'modpack_location_dev'

	modpack_dir = Path(path).expanduser().resolve()
	if not modpack_dir.exists():
		print("Provided modpack location not exist:\n", modpack_dir)
		return

	if not modpack_dir.is_dir():
		print("Provided modpack location should be directory:\n", modpack_dir)
		return

	DATA.mkdir(parents = True, exist_ok = True)

	with open(mld, 'w') as f:
		f.write(str(modpack_dir))

def main():
	args = sys.argv[1:]

	if len(args) < 1:
		print('use [setup_dev|modify|set]')
		return 1

	match args[0]:
		case 'setup_dev':
			modpack_location = get_dev_modpack_location()
			if modpack_location is None:
				return 1
			setup_dev(modpack_location)
			return 0

		case 'modify':
			modify(get_files_to_replace(), PWD)
			return 0

		case 'set':
			if len(args) < 2:
				print('Use `dev.py set "path_to_modpack"` (where folders like "mods" located)')
				return 1
			set_dev_modpack_location(args[1])
			return 0

	print('use [setup_dev|modify|set]')
	return 1


if __name__ == "__main__":
	sys.exit(main())