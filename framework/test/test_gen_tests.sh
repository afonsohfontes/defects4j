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
    local known_pids=$(defects4j pids)
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

for bid in $(echo $BUGS); do
    # Skip all bug ids that do not exist in the active-bugs csv
    if ! grep -q "^$bid," "$BASE_DIR/framework/projects/$PID/$BUGS_CSV_ACTIVE"; then
        warn "Skipping bug ID that is not listed in active-bugs csv: $PID-$bid"
        continue
    fi

    # Use the modified classes as target classes for efficiency
    target_classes="$BASE_DIR/framework/projects/$PID/modified_classes/$bid.src"
    name="$BASE_DIR/framework/test/Experiments/data/results"

    if [[ -e $name.csv || -L $name.csv ]] ; then
        i=0
        while [[ -e $name-$i.csv || -L $name-$i.csv ]] ; do
            let i++
        done
        dest=$name-$i
    fi
    cp "$name".csv "$dest".csv
    resultsData="$dest".csv
    #echo $resultsData
    python3 csvInit.py -f $resultsData -b $bid -p $PID
    #"-f <path to file> -c <column name> -v <value> -r <row (criterion)> -p <project name> -b <bug name>"
    #python3 csvInit.py -f $resultsData -c "Bug_Detection" -v 1 -r "BRANCH"

    # Iterate over all supported generators and generate regression tests
    #for tool in $($BASE_DIR/framework/bin/gen_tests.pl -g help | grep \- | tr -d '-'); do
        # Directory for generated test suites
        tool="evosuite"
        suite_src="$tool"
        #suite_src=$evosuite
        #echo $suite_src
        suite_num=1
        suite_dir="$work_dir/$tool/$suite_num"
	      #echo $suite_dir
        # Generate (regression) tests for the fixed version
        vid=${bid}f

        rm -rf evosuite-report/statistics.csv
	      echo ""

        echo "Run evosuite test generator for $PID with a TOTAL budget of 15 secs"
	      echo ""
        if ! gen_tests.pl -g "$tool" -p $PID -v $vid -n 1 -o "$TMP_DIR" -b 60 -c "$target_classes" -C "METHOD"; then
            die "run $tool (regression) on $PID-$vid"
            # Skip any remaining analyses (cannot be run), even if halt-on-error is false
            continue
        fi

        #parsing the SEARCH RESULTS
        echo "--- START PARSING ---"
        resultsEvo="$BASE_DIR/framework/test/evosuite-report/statistics.csv"
        python3 CSVParser.py -f $resultsEvo -o $resultsData -c "BRANCH"

        echo ""
        echo "If any tests are broken, they need to be removed until all tests PASS."
        echo "This removal is done running them against the fully functional version of the SUT"
        #fix_test_suite.pl -p $PID -d "$suite_dir" || die "fix test suite"
	
	      echo ""
	      echo "Now its time to insert the bugs and run test suite and determine bug detection"
        #run_bug_detection.pl -a "$resultsData" -p $PID -d "$suite_dir" -o "$name/logs"

	      #echo ""
        #echo "After running the tests, its time to analyse them and determine mutation score"
        #test_mutation $PID "$suite_dir"

	      echo ""
        echo "Run test suite again and determine code coverage"
        #test_coverage $PID "$suite_dir" 0

	      echo "Removing the folders created"
        rm -rf $work_dir/$tool
    #done

    #vid=${bid}b
    # Run Randoop to generate error-revealing tests (other tools cannot do so)
    #gen_tests.pl -g randoop -p $PID -v $vid -n 1 -o "$TMP_DIR" -b 30 -c "$target_classes" -E
    # We expect Randoop to not crash; it may or may not create an error-revealing test for this version
    #ret=$?
    #[ $ret -eq 0 ] || [ $ret -eq 127 ] || die "run $tool (error-revealing) on $PID-$vid"

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
