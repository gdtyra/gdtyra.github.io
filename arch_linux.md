# Arch Linux

## Pacman
- `pacman -Q` - list installed packages
- `pacman -Qi` - list installed packages with detail
- `pacman -Qe` - list packages explicitly installed by the user
- `pacman -Qei` - list packages explicitly installed by the user with detail
- `pacman -Qdtq` - list installed, orphaned packages
- `pacman -Rs <package_name>` - remove package
- `pacman -Rs $(pacman -Qdtq)` - remove orphaned packages
- `pacman -Ss <search_string>` - search available packages
- `pacman -S <package_name>` - install package
- `pacman -Syu` - full system update
- `pacman -Scc` - clean package cache