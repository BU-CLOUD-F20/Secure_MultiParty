#!/bin/bash

# Command to launch test/experiment

HOST_ACTUAL=`hostname`
HOST_WANT="party-0"

echo "Does $HOST_ACTUAL == $HOST_WANT ?"

if [[ $HOST_ACTUAL == $HOST_WANT ]]; then
  mpirun --mca btl_vader_single_copy_mechanism none --host localhost,party-1,party-2 -np 3 exp-exchange 1000
  sleep infinity
else
  sleep infinity
fi
