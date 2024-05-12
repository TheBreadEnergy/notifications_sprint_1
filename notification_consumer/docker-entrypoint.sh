#!/bin/sh

set -o errexit
set -o nounset

readonly cmd="$*"

# Evaluating passed command (do not touch):
# shellcheck disable=SC2086
exec $cmd

python -m src.main