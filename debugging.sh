# Ricker Test

PETSC_OPTIONS="-start_in_debugger noxterm -debugger_ranks 0" pylith step01_ricker.cfg 

# TO join existing docker container
docker exec -i -t pylith-dev-workspace /bin/bash

# then 
ps -uax

gdb -p $PID
