## Voror
Voror is a utility used to split data file generated by LAMMPS with different frames. Then calculates each frame with voro++. Finally, renders each frame with povray.

### Usage
1. Make sure whether both of `voro++` and `povray` command is accessible.
2. Edit configurations in `config.h` with your favor.
3. Execute `make` command to re-compile project
4. Execute `./Voror.py [name of data file]` if you don't need to filter particles with their id. Execute `./Voror.py [name of data file] [start id] [end id]` if you want to filter particles with their id from `start` to `end`.
