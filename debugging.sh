# Ricker Test

PETSC_OPTIONS="-start_in_debugger noxterm -debugger_ranks 0" pylith step01_ricker.cfg 

# TO join existing docker container
docker exec -i -t pylith-dev-workspace /bin/bash

# then 
ps -uax

gdb -p $PID

# Reset ptrace

# Run docker image in privileged mode as root.
docker run -ti --privileged --rm -u root ghcr.io/geodynamics/pylith_installer/pylith-devenv /bin/bash

# Verify ptrace setting needs updating
cat /proc/sys/kernel/yama/ptrace_scope
# If output is 1, then continue, if 0 then no need to change anything.

# Verify ptrace setting is correct.
cat /etc/sysctl.d/10-ptrace.conf
# Output should be 0

# Restart the procps service.
service procps restart

# Verify ptrace setting has changed
cat /proc/sys/kernel/yama/ptrace_scope
# Output should be 0
