#!/bin/bash

set -o errexit
set -o nounset

pyclean() {
  # Cleaning cache:
  find . |
    grep -E '(__pycache__|\.hypothesis|\.perm|\.cache|\.static|\.py[cod]$)' |
    xargs rm -rf
}
run_checks(){
    echo 'Running checks...'

    strategies=("stochrsi" "bband" "adx" "macd")

    for startegy in ${strategies[@]}; do
        echo 'running for: '$startegy
        python3 main.py --strategy $startegy --data yfinance --ticker MSFT --start 2017-01-01 --end 2022-01-01 
    done

    echo 'Done!'
}

pyclean

trap pyclean EXIT INT TERM

run_checks
