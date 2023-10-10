#!/usr/bin/env bash

while IFS=',' read -r project bug criterion budget extra_trials; do
    if [ "$project" != "Project" ]; then
        echo ">>Running specific test for Project: $project, Bug: $bug, Criterion: $criterion, Budget: $budget, Extra_Trials: $extra_trials"
        sudo ./specific_tests.sh -p "$project" -b "$bug" -c "$criterion" -o "$budget" -t "$extra_trials"
        #wait  # this should not be necessary but you can try adding it if you are having issues
    fi
done < configurations_to_run.txt
