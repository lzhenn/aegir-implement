#mpirun --hostfile ./mpihosts --rankfile ./mpirank -n 96 ./coawstM ./Projects/GBA/coupling_gba.in >& cwstv3..log
mpirun -np 78 ./coawstM ./Projects/Njord/coupling.in >& cwstv3.20160723.log
#mpirun -hostfile ./mpihosts -n 96 ./coawstM ./Projects/GBA/coupling_gba.in >& cwstv3..log
