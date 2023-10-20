#!/usr/bin/env bash
################################################################################
#
# This script verifies that test generation tools can be executed for all bugs
# for a given project.
#
# Examples for Lang:
#    ./specific_tests.sh -p Lang -b 1 -c "BRANCH" -o "300" -t 10
#
################################################################################
# Import helper subroutines and variables, and init Defects4J
source test.include
init
# Print usage message and exit
usage() {
  local known_pids=0
  known_pids=$(defects4j pids)
  echo "usage: $0 -p <project id> [-b <bug id> ... | -b <bug id range> ... ]"
  echo "Project ids:"
  for pid in $known_pids; do
    echo "  * $pid"
  done
  exit 1
}

# Check arguments
declare -a CRITERIONS=()
declare -a BUDGETS=()
declare -i NUM_TRIALS=0

while getopts ":p:b:c:o:t:" opt; do
  case $opt in
  p)
    PID="$OPTARG"
    ;;
  b)
    if [[ "$OPTARG" =~ ^[0-9]*\.\.[0-9]*$ ]]; then
      BUGS="$BUGS $(eval echo {$OPTARG})"
    else
      BUGS="$BUGS $OPTARG"
    fi
    ;;
  c)
    CRITERIONS+=("$OPTARG")
    ;;
  o)
    BUDGETS+=("$OPTARG")
    ;;
  t)
    NUM_TRIALS="$OPTARG"
    ;;
  \?)
    echo "Unknown option: -$OPTARG" >&2
    usage
    ;;
  :)
    echo "No argument provided: -$OPTARG." >&2
    usage
    ;;
  esac
done

if [ "$PID" == "" ]; then
  usage
fi

if [ ! -e "$BASE_DIR/framework/core/Project/$PID.pm" ]; then
  usage
fi

init

# Run all bugs, unless otherwise specified
if [ "$BUGS" == "" ]; then
  BUGS="$(get_bug_ids $BASE_DIR/framework/projects/$PID/$BUGS_CSV_ACTIVE)"
fi

# Create log file
script_name=$(echo $script | sed 's/\.sh$//')
LOG="$TEST_DIR/${script_name}$(printf '_%s_%s' $PID $$).log"

################################################################################
# Run all generators on the specified bugs, and determine bug detection,
# mutation score, and coverage.
################################################################################

# Reproduce all bugs (and log all results), regardless of whether errors occur
HALT_ON_ERROR=0

work_dir="$TMP_DIR/$PID"
mkdir -p $work_dir

# Clean working directory
rm -rf "$work_dir/*"

criteria=$CRITERIONS
budgets=$BUDGETS
trials=$NUM_TRIALS


      # Function to create directory if it doesn't exist
      create_dir() {
        if [ ! -d "$1" ]; then
          mkdir -p "$1"
        fi
      }

DIR="$BASE_DIR/framework/test/Experiments/data/$PID/"

# Create a timestamp
#timestamp=$(date +"%Y%m%d%H%M%S")

#if [ -d "$DIR" ]; then
  # Rename the existing directory with a timestamp
#  mv "$DIR" "${DIR}_$timestamp"
#fi

# Create a new directory for the current experiment
create_dir -p "$DIR"

for ((trial = 1; trial <= $trials; trial++)); do
  for budget in ${budgets[@]}; do
    for bid in $(echo $BUGS); do
      # Skip all bug ids that do not exist in the active-bugs csv
      if ! grep -q "^$bid," "$BASE_DIR/framework/projects/$PID/$BUGS_CSV_ACTIVE"; then
        warn "Skipping bug ID that is not listed in active-bugs csv: $PID-$bid"
        continue
      fi

      name="$BASE_DIR/framework/test/Experiments/data/"

      # Base directories
      create_dir "$name/$PID/$bid"
      create_dir "$name/$PID/$bid/budget_$budget"
      create_dir "$name/$PID/$bid/budget_$budget/trial_$trial"

      # Subdirectories that are common to all criteria
      DIR="$name/$PID/$bid/budget_$budget/trial_$trial"
      create_dir "$DIR/images"
      create_dir "$DIR/images/branch"
      create_dir "$DIR/summaries"
      create_dir "$DIR/generationData"

      # Loop through the list of criteria to create specific folders
      for criterion in ${criteria[@]}; do
        criterion_folder=${criterion/:/_} # Replace ':' with '_'
        create_dir "$DIR/generationData/$criterion_folder"
        create_dir "$DIR/generationData/$criterion_folder/tests"
      done

      i=0
      # Use the modified classes as target classes for efficiency
      target_classes="$BASE_DIR/framework/projects/$PID/modified_classes/$bid.src"
      for class in $(cat $target_classes); do
        dest=$name$PID/$bid/budget_$budget/trial_$trial/results-Class_$i
        i=$(($i + 1))
        cp "$name"results.csv "$dest".csv
        resultsData="$dest".csv
        python3 csvInit.py -f $resultsData -b $bid -p $PID
      done

      abstractPath="$BASE_DIR/framework/test/Experiments/data/$PID/$bid/budget_$budget/trial_$trial/results-Class_"
      tool="evosuite"
      vid=${bid}f
      for criterion in ${criteria[@]}; do

        failed_trials=0
        testsD="$BASE_DIR/framework/test/Experiments/data/$PID/$bid/budget_$budget/trial_$trial/generationData/${criterion/:/_}/"
        OUTd="$BASE_DIR/framework/test/Experiments/data/$PID/$bid/budget_$budget/trial_$trial/generationData/${criterion/:/_}/$PID/evosuite/1/"
        suite_dir=$OUTd
        while [ ! -f "$testsD/statistics.csv" ]; do
          if [ $failed_trials -ge 5 ]; then
            echo "Reached maximum number of failed trials. Exiting loop."
            break
          fi

          echo ""
          echo "------ Run evosuite test generator for $PID-$vid with a TOTAL budget of $budget secs - trial $trial of $trials - using $criterion -------"
          echo ""

          gen_tests.pl -g "$tool" -p "$PID" -v "$vid" -n 1 -o "$testsD" -b "$budget" -c "$target_classes" -C "$criterion" 2>&1 | tee -a "$testsD/1-EvoTranscription.log"

          # Move the statistics file if it was generated
          if [ -f "evosuite-report/statistics.csv" ]; then
            mv evosuite-report/statistics.csv "$testsD"
          else
            echo "Trial failed. Retrying..."
            ((failed_trials++))
          fi
        done
        if [ ! -f "$testsD/statistics.csv" ]; then
          echo "The file 'statistics.csv' does not exist. ---- Trial failed!"
        else
          echo ""
          echo "--- PARSING RESULTS for $PID-$vid with a TOTAL budget of $budget secs - trial $trial of $trials - using $criterion  ---"
          echo ""
          resultsEvo="$testsD/statistics.csv"
          python3 CSVParser.py -f "$resultsEvo" -o "$abstractPath" -c "$criterion" -i "$i" 2>&1 | tee -a "$testsD/2-ParserTranscription.log"

          echo ""
          echo "If any tests are broken, they need to be removed until all tests PASS."
          echo "This removal is done running them against the fully functional version of the SUT"
          # "/home/afonso/IdeaProjects/defects4j/framework/test/Experiments/data/Math/14/budget_180/trial_1/generationData/BRANCH/tests/suite_num
          fix_test_suite.pl -p $PID -d "$suite_dir" || die "fix test suite"

          echo ""
          echo "Inserting the bugs and running the test suite and determine bug detection"
          run_bug_detection.pl -a "$abstractPath" -p $PID -d "$suite_dir" -o "$testsD" -i "$i" -c "$criterion"
        fi
        rm -rf $work_dir/$tool
      done
    done
  done
done
HALT_ON_ERROR=1

# Print a summary of what went wrong
if [ $ERROR != 0 ]; then
  printf '=%.s' $(seq 1 80) 1>&2
  echo 1>&2
  echo "The following errors occurred:" 1>&2
  cat $LOG 1>&2
fi

# Indicate whether an error occurred
exit $ERROR
