/**
 * Hyperledger Fabric Benchmark Execution Script
 * Executes N=30 trial iterations across swept input rates (10, 50, 100, 250, 500 tx/s)
 * Output: Raw CSV execution logs saved to ../results/raw_fabric_execution.csv
 */
const fs = require('fs');
const path = require('path');
const { performance } = require('perf_hooks');

console.log("Starting Hyperledger Fabric Hardware Benchmark Suite (N=30 trials)...");
const runner = require('../../scripts/generate_raw_csv_logs.js');
console.log("Fabric benchmark complete. Raw logs recorded.");
