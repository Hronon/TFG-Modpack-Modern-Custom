projects=(
)

# Change target
java -jar pakku.jar set --target "curseforge"

# Change project info
java -jar pakku.jar cfg \
  --name 'TFG-Custom'  \
  --author 'Hronon' \
  --description 'Fork of TFG-Modern with custom changes'

# Add listed mods in projects
for entry in "${projects[@]}"; do
  IFS=: read -r slug id side <<< "$entry"
  side=${side:-BOTH}

  case "$side" in
    CLIENT|SERVER|BOTH) ;;
    *)
      echo "Invalid side '$side' for $slug"
      exit 1
      ;;
  esac

  # Add mod from CF
  printf 'Y\n' | java -jar pakku.jar add prj --curseforge "$slug:$id"
  # Configure mod side
  java -jar pakku.jar cfg prj --side "$side" "$slug"
done
