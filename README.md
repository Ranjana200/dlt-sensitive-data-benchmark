# Empirical Benchmarking Suite: Ethereum vs. R3 Corda vs. Hyperledger Fabric

This repository contains the complete open-source source code, benchmark runners, and raw execution logs for the research paper:

> **"Comparative Benchmarking of Ethereum, R3 Corda, and Hyperledger Fabric for Sensitive Data Applications: Architecture, Performance, and Privacy Exposure Trade-offs"**

---

## 📌 Repository Structure

```text
.
├── ethereum/               # Ethereum Smart Contract (Solidity v0.8.20) & Hardhat benchmark
├── corda/                  # R3 Corda CorDapp (Kotlin) & MockNetwork multi-trial harness
├── fabric/                 # Hyperledger Fabric Chaincode (Go) & Execute-Order-Validate runner
├── results/                # Raw hardware execution logs (CSV format) & statistical output
├── scripts/                # Data processing script (Mean ± SD & 95% Confidence Intervals)
└── README.md               # Reproduction Guide
```

---

## 🚀 How to Reproduce Benchmarks & Verify Results

### Prerequisites
* **Node.js (v18 or v20 LTS)**
* **Java JDK 11** (Amazon Corretto or OpenJDK)
* **Python 3.8+** (pandas, numpy, scipy)

### Step 1: Clone Repository
```bash
git clone https://github.com/Ranjana200/dlt-sensitive-data-benchmark.git
cd dlt-sensitive-data-benchmark
```

### Step 2: Run Ethereum Benchmark
```bash
cd ethereum
npm install
node scripts/benchmark-eth.js
```
*Outputs raw transaction logs to `../results/raw_eth_execution.csv`.*

### Step 3: Run Corda Benchmark
```bash
cd ../corda
./gradlew test --tests com.hospital.PatientFlowBenchmark
```
*Outputs raw flow latency logs to `../results/raw_corda_execution.csv`.*

### Step 4: Process Results & Generate Tables
```bash
cd ..
python scripts/process_results.py
```
*Reads all raw hardware CSV logs and outputs Mean ± SD and 95% Confidence Interval tables.*

---

## 📊 Summary of Benchmark Findings

| Platform | Architectural Paradigm | Throughput (500 tx/s Load) | Latency (100 tx/s Load) | Privacy Exposure Model |
| :--- | :--- | :--- | :--- | :--- |
| **Ethereum** | Account-based World State | 145.16 ± 3.49 TPS | 23.39 ± 0.72 ms | Public Broadcast (All Nodes) |
| **R3 Corda** | UTXO-style Linear State | 84.87 ± 2.20 TPS | 64.88 ± 1.56 ms | Sub-Ledger Point-to-Point |
| **Hyperledger Fabric** | Channel Key-Value State | 378.17 ± 5.37 TPS | 23.74 ± 0.82 ms | Channel & Collection Gated |

---

## 📜 Citation
If you use this benchmark suite or codebase in your research, please cite our paper:

```bibtex
@article{ranjana2026dlt,
  title={Comparative Benchmarking of Ethereum, R3 Corda, and Hyperledger Fabric for Sensitive Data Applications: Architecture, Performance, and Privacy Exposure Trade-offs},
  author={Ranjana, S. and Chacko, Namrata Marium},
  journal={KSII Transactions on Internet and Information Systems},
  year={2026}
}
```
