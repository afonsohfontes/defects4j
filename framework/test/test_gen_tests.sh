#!/usr/bin/env bash
################################################################################
#
# This script verifies that test generation tools can be executed for all bugs
# for a given project. 
#
# Examples for Lang:
#   * Generate for all bugs:         ./test_generate_suites.sh -pLang
#   * Generate for bugs 1-10:        ./test_generate_suites.sh -pLang -b1..10
#   * Generate for bugs 1 and 3:     ./test_generate_suites.sh -pLang -b1 -b3
#   * Generate for bugs 1-10 and 20: ./test_generate_suites.sh -pLang -b1..10 -b20
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
while getopts ":p:b:" opt; do
    case $opt in
        p) PID="$OPTARG"
            ;;
        b) if [[ "$OPTARG" =~ ^[0-9]*\.\.[0-9]*$ ]]; then
                BUGS="$BUGS $(eval echo {$OPTARG})"
           else
                BUGS="$BUGS $OPTARG"
           fi
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

#run_bug_detection.pl -a "$BASE_DIR/framework/test/Experiments/data/$PID/14/budget_300/trial_1/results-Class_" -p $PID -d "$BASE_DIR/framework/test/Experiments/data/$PID/14/budget_300/trial_1/generationData/BRANCH/tests" -o "$BASE_DIR/framework/test/Experiments/data/logs" -i "0" -c "BRANCH"
#read -p "Press any key to resume ..."
#Clusure 1, 4

# criteria=("BRANCH" "BRANCH:EXCEPTION" "BRANCH:PRIVATEMETHOD" "BRANCH:EXECUTIONTIME" "BRANCH:OUTPUT")
criteria=("BRANCH" "BRANCH:EXCEPTION" "BRANCH:EXECUTIONTIME" "BRANCH:OUTPUT")
budgets=(180 300)
trials=10
maxTrials=1

DIR="$BASE_DIR/framework/test/Experiments/data/$PID"
if [ -d "$DIR" ];
then
  rm -rf "$DIR"_old
  mkdir "$DIR"_old
  mv "$DIR" "$DIR"_old
  rm -rf "$DIR"
  mkdir $DIR
else
  mkdir $DIR
fi

for (( trial=1; trial<=$trials; trial++ )) do
  for budget in ${budgets[@]}; do
    for bid in $(echo $BUGS); do
        # Skip all bug ids that do not exist in the active-bugs csv
        if ! grep -q "^$bid," "$BASE_DIR/framework/projects/$PID/$BUGS_CSV_ACTIVE"; then
            warn "Skipping bug ID that is not listed in active-bugs csv: $PID-$bid"
            continue
        fi

        # Use the modified classes as target classes for efficiency
        target_classes="$BASE_DIR/framework/projects/$PID/modified_classes/$bid.src"

        name="$BASE_DIR/framework/test/Experiments/data/"
        #rm -rf "$name$PID-bug_$bid-budget_$budget-trial_$trial"


        DIR=$name/$PID/$bid/
        if [ -d "$DIR" ];
        then
          echo ""
        else
        	mkdir $DIR
        fi
        DIR=$name/$PID/$bid/budget_$budget
        if [ -d "$DIR" ];
        then
          echo ""
        else
        	mkdir $DIR
        fi

        DIR=$name/$PID/$bid/budget_$budget/trial_$trial/
        if [ -d "$DIR" ];
        then
          echo ""
        else
        	mkdir $DIR
        	mkdir $DIR/images
        	mkdir $DIR/images/branch
        	mkdir $DIR/summaries
        	mkdir $DIR/generationData
        	mkdir $DIR/generationData/BRANCH
        	mkdir $DIR/generationData/BRANCH_EXCEPTION
        	mkdir $DIR/generationData/BRANCH_EXECUTIONTIME
        	mkdir $DIR/generationData/BRANCH_PRIVATEMETHOD
        	mkdir $DIR/generationData/BRANCH_OUTPUT
        	mkdir $DIR/generationData/BRANCH/tests
        	mkdir $DIR/generationData/BRANCH_EXCEPTION/tests
        	mkdir $DIR/generationData/BRANCH_PRIVATEMETHOD/tests
        	mkdir $DIR/generationData/BRANCH_EXECUTIONTIME/tests
        	mkdir $DIR/generationData/BRANCH_OUTPUT/tests
        fi

        #mkdir $name$PID-bug_$bid-budget_$budget-trial_$trial
        #mkdir $name$PID-bug_$bid-budget_$budget-trial_$trial/images
        #mkdir $name$PID-bug_$bid-budget_$budget-trial_$trial/summaries


        i=0
        for class in $(cat $target_classes); do
          dest=$name$PID/$bid/budget_$budget/trial_$trial/results-Class_$i
          i=$(($i+1))
          cp "$name"results.csv "$dest".csv
          resultsData="$dest".csv
          python3 csvInit.py -f $resultsData -b $bid -p $PID
        done

        abstractPath="$BASE_DIR/framework/test/Experiments/data/$PID/$bid/budget_$budget/trial_$trial/results-Class_"
        #"-f <path to file> -c <column name> -v <value> -r <row (criterion)> -p <project name> -b <bug name>"
        #python3 csvInit.py -f $resultsData -c "Bug_Detection" -v 1 -r "BRANCH"

        # Iterate over all supported generators and generate regression tests
        #for tool in $($BASE_DIR/framework/bin/gen_tests.pl -g help | grep \- | tr -d '-'); do
            # Directory for generated test suites
            tool="evosuite"
            vid=${bid}f
            for criterion in ${criteria[@]}; do
              echo ""
              echo "------ Run evosuite test generator for $PID-$vid with a TOTAL budget of $budget secs - trial $trial of $trials - using $criterion -------"
              echo ""
              testsD="$BASE_DIR/framework/test/Experiments/data/$PID/$bid/budget_$budget/trial_$trial/generationData/${criterion/:/_}/"
              OUTd="$BASE_DIR/framework/test/Experiments/data/$PID/$bid/budget_$budget/trial_$trial/generationData/${criterion/:/_}/$PID/evosuite/1/"
              suite_dir=$OUTd
              gen_tests.pl -g "$tool" -p "$PID" -v "$vid" -n 1 -o "$testsD" -b "$budget" -c "$target_classes" -C "$criterion" 2>&1 | tee -a "$testsD/1-EvoTranscription.log"

              mv evosuite-report/statistics.csv "$testsD"
              echo "--- PARSING RESULTS ---"
              resultsEvo="$testsD/statistics.csv"
              python3 CSVParser.py -f "$resultsEvo" -o "$abstractPath" -c "$criterion" -i "$i" 2>&1 | tee -a "$testsD/2-ParserTranscription.log"
              #if [ $? -eq 0 ]; then
              #    echo "Generation succeeded"
              #else
              #    echo "Generation failed.. trying again."
              #    rm -rf $OUTd
              #    gen_tests.pl -g "$tool" -p "$PID" -v "$vid" -n 1 -o "$testsD" -b "$budget" -c "$target_classes" -C "$criterion" 2>&1 | tee -a "$testsD/1-EvoTranscription_ERROR.log"
              #    rm -rf $testsD/statistics.csv
              #    mv evosuite-report/statistics.csv "$testsD"
              #    echo "--- PARSING RESULTS ---"
              #    resultsEvo="$testsD/statistics.csv"
              #    python3 CSVParser.py -f "$resultsEvo" -o "$abstractPath" -c "$criterion" -i "$i" 2>&1 | tee -a "$testsD/2-ParserTranscription_ERROR.log"
              #fi

              echo ""
              echo "If any tests are broken, they need to be removed until all tests PASS."
              echo "This removal is done running them against the fully functional version of the SUT"
              # "/home/afonso/IdeaProjects/defects4j/framework/test/Experiments/data/Math/14/budget_180/trial_1/generationData/BRANCH/tests/suite_num
              fix_test_suite.pl -p $PID -d "$suite_dir" || die "fix test suite"

              echo ""
              echo "Inserting the bugs and running the test suite and determine bug detection"

              run_bug_detection.pl -a "$abstractPath" -p $PID -d "$suite_dir" -o "$testsD" -i "$i" -c "$criterion"


              #echo ""
              #echo "After running the tests, its time to analyse them and determine mutation score"
              #test_mutation $PID "$suite_dir"

              #echo ""
              #echo "Run test suite again and determine code coverage"
              #test_coverage $PID "$suite_dir" 0

              #echo "Removing the folders created"
              rm -rf $work_dir/$tool
            done
        #done

        #vid=${bid}b
        # Run Randoop to generate error-revealing tests (other tools cannot do so)
        #gen_tests.pl -g randoop -p $PID -v $vid -n 1 -o "$TMP_DIR" -b 30 -c "$target_classes" -E
        # We expect Randoop to not crash; it may or may not create an error-revealing test for this version
        #ret=$?
        #[ $ret -eq 0 ] || [ $ret -eq 127 ] || die "run $tool (error-revealing) on $PID-$vid"

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
