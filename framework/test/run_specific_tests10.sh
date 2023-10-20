#!/usr/bin/env bash

# Read the list of configurations line by line
while IFS=',' read -r project bug criterion budget extra_trials; do
    # Skip the header line
    if [ "$project" != "Project" ]; then
        # Convert extra_trials to an integer
        extra_trials=$(printf "%.0f" "$extra_trials")
        # Run specific_tests.sh for each configuration
        echo " >> Running specific test for Project: $project, Bug: $bug, Criterion: $criterion, Budget: $budget, Extra_Trials: $extra_trials <<"
        sudo ./specific_tests.sh -p "$project" -b "$bug" -c "$criterion" -o "$budget" -t "$extra_trials"
    fi
done < More_Trials_Needed_Corrected_Part_10.txt
