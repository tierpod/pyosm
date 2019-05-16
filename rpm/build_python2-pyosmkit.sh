#!/bin/bash

set -eu

SPEC=$1
VER=$(awk '/Version:/ {print $2}' $SPEC)

if ! [ -e "$HOME/rpmbuild/SOURCES/v${VER}.tar.gz" ]; then
	spectool -R -g $SPEC
fi

echo "build rpm: SPEC=$SPEC VER=$VER"
rpmbuild -ba $SPEC
