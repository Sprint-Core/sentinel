#!/bin/bash
set -evx

mkdir ~/.sprintcore

# safety check
if [ ! -f ~/.sprintcore/.sprint.conf ]; then
  cp share/sprint.conf.example ~/.sprintcore/sprint.conf
fi
