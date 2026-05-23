#!/bin/bash

# Ansible Playbook Performance Benchmarking Script
set -e

RESULTS_DIR="/tmp/ansible-benchmarks"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT_FILE="${RESULTS_DIR}/benchmark_report_${TIMESTAMP}.txt"

# Create results directory
mkdir -p "$RESULTS_DIR"

echo "Ansible Playbook Performance Benchmark - $(date)" > "$REPORT_FILE"
echo "=================================================" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Function to run benchmark
run_benchmark() {
    local playbook=$1
    local description=$2
    local iterations=${3:-3}
    
    echo "Testing: $description" | tee -a "$REPORT_FILE"
    echo "Playbook: $playbook" | tee -a "$REPORT_FILE"
    echo "Iterations: $iterations" | tee -a "$REPORT_FILE"
    echo "----------------------------------------" | tee -a "$REPORT_FILE"
    
    local total_time=0
    local successful_runs=0
    
    for i in $(seq 1 $iterations); do
        echo "  Run $i of $iterations..."
        start_time=$(date +%s)
        
        if ansible-playbook "$playbook" --check -v > "${RESULTS_DIR}/run_${i}_output.log" 2>&1; then
            end_time=$(date +%s)
            run_time=$((end_time - start_time))
            total_time=$((total_time + run_time))
            successful_runs=$((successful_runs + 1))
            echo "    Completed in ${run_time}s" | tee -a "$REPORT_FILE"
        else
            echo "    FAILED" | tee -a "$REPORT_FILE"
        fi
    done
    
    if [ $successful_runs -gt 0 ]; then
        avg_time=$((total_time / successful_runs))
        echo "  Average execution time: ${avg_time}s" | tee -a "$REPORT_FILE"
        echo "  Successful runs: $successful_runs/$iterations" | tee -a "$REPORT_FILE"
    else
        echo "  All runs failed!" | tee -a "$REPORT_FILE"
    fi
    
    echo "" >> "$REPORT_FILE"
}

# Run benchmarks
echo "Starting Ansible playbook benchmarks..."

run_benchmark "large-playbook.yml" "Original Monolithic Playbook" 3
run_benchmark "optimized-playbook.yml" "Role-based Optimized Playbook" 3
run_benchmark "async-optimization.yml" "Asynchronous Execution Playbook" 3

echo "Benchmark completed. Results saved to: $REPORT_FILE"
echo "Individual run logs saved to: $RESULTS_DIR"
EOF
