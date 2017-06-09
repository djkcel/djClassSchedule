#!/bin/bash

for migration in $(ls ${TRAVIS_BUILD_DIR}/travis/oracle/*.sql | sort --version-sort)
do
    echo "Running Migration - ${migration}"
    sqlplus -L -S ${DB_USER}/${DB_PASS} @${migration}
done