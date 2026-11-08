from pathlib import Path
from dataclasses import dataclass
import subprocess
import sys
import shutil
from typing import Optional
import re

PWD = Path(__file__).resolve().parent
PROJECTS = PWD / 'projects.txt'
BACKUPS = PWD / 'project_backups'
REPLACE = PWD / 'replace_with_original'
DATA = PWD / 'data'

@dataclass(frozen=True)
class ModMeta:
	slug: str
	cf_id: str
	side: str

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
		'add', 'prj', '--curseforge', f'{mod.slug}:{mod.cf_id}',
	], check = True, input="Y\n", text = True, cwd=PWD)

	subprocess.run([
		'java', '-jar', 'pakku.jar',
		'cfg', 'prj', '--side', f'{mod.side}', f'{mod.slug}'
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

def modify(replace: list[str], base: Path):
	mods = []
	with open(PROJECTS, 'r') as f:
		while line := f.readline():
			line = re.sub(r'\s+', '', line).split(':')
			if len(line) < 2:
				print(f'Curseforge mod slug and file id should be provided.\n You provided: {line}')
				continue

			if not line[1].isnumeric():
				print(f'Curseforge file id is not numeric: {line[1]}. Skipping')
				continue

			side = 'BOTH'
			if len(line) >= 3:
				side = line[2]
				if side not in ['CLIENT', 'SERVER', 'BOTH']:
					print(line, f'Incorrect side value: {side} [CLIENT|SERVER|BOTH]. Skipping')
					continue

			mods.append(ModMeta(line[0], line[1], side))

	subprocess.run([
		'bash', 'update_pakku.sh'
	], check = True, cwd=PWD)

	for mod in mods:
		add_mod(mod)

	replace_with_original(replace, base)

def setup_dev(modpack_location: Path):
	backup_files = [
			"pakku.json",
			"pakku-lock.json"
	]

	try:
		for file in backup_files:
			backup(file)

		modify(get_files_to_replace(), modpack_location)
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