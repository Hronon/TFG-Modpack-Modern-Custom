# backup old pakku
cp ./pakku.json ./pakku.json.bak
cp ./pakku-lock.json ./pakku-lock.json.bak

# perform and fetch changes
bash ./modify_pakku.sh
java -jar pakku.jar cfg --mods-path "modpack/minecraft/mods/"
java -jar pakku.jar cfg --resource-packs-path "modpack/minecraft/resourcepacks/"
java -jar pakku.jar cfg --shaders-path "modpack/minecraft/shaderpacks/"
java -jar pakku.jar fetch

# restore
mv ./pakku.json.bak ./pakku.json
mv ./pakku-lock.json.bak ./pakku-lock.json
