import os
import csv
import json
import math

def calculate_stats(values):
    n = len(values)
    if n == 0:
        return {"mean": 0.0, "sd": 0.0, "ci95_lower": 0.0, "ci95_upper": 0.0, "formatted": "N/A"}
    mean = sum(values) / n
    if n == 1:
        sd = 0.0
    else:
        variance = sum((x - mean) ** 2 for x in values) / (n - 1)
        sd = math.sqrt(variance)
    margin_of_error = 1.96 * (sd / math.sqrt(n)) if n > 1 else 0.0
    return {
        "mean": round(mean, 2),
        "sd": round(sd, 2),
        "ci95_lower": round(mean - margin_of_error, 2),
        "ci95_upper": round(mean + margin_of_error, 2),
        "formatted": f"{mean:.2f} ± {sd:.2f} [95% CI: {mean - margin_of_error:.2f} - {mean + margin_of_error:.2f}]"
    }

def process_csv_log(filepath):
    data_by_load = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            load = int(row['input_load_tps'])
            if load not in data_by_load:
                data_by_load[load] = {
                    'latencies': [],
                    'tps': [],
                    'cpu': [],
                    'ram': []
                }
            data_by_load[load]['latencies'].append(float(row['latency_ms']))
            data_by_load[load]['tps'].append(float(row['achieved_tps']))
            data_by_load[load]['cpu'].append(float(row['cpu_util_pct']))
            data_by_load[load]['ram'].append(float(row['ram_usage_mb']))

    stats_by_load = {}
    for load, metrics in sorted(data_by_load.items()):
        stats_by_load[load] = {
            'latency': calculate_stats(metrics['latencies']),
            'tps': calculate_stats(metrics['tps']),
            'cpu': calculate_stats(metrics['cpu']),
            'ram': calculate_stats(metrics['ram'])
        }
    return stats_by_load

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(script_dir, '..', 'results')

    eth_csv = os.path.join(results_dir, 'raw_eth_execution.csv')
    corda_csv = os.path.join(results_dir, 'raw_corda_execution.csv')
    fabric_csv = os.path.join(results_dir, 'raw_fabric_execution.csv')

    print("=" * 70)
    print("  RAW BENCHMARK CSV LOG PROCESSOR (KSII TIIS REPRODUCIBILITY)")
    print("=" * 70)

    summary = {}
    if os.path.exists(eth_csv):
        print(" Processing Ethereum raw execution CSV logs...")
        summary['Ethereum'] = process_csv_log(eth_csv)
    if os.path.exists(corda_csv):
        print(" Processing R3 Corda raw execution CSV logs...")
        summary['Corda'] = process_csv_log(corda_csv)
    if os.path.exists(fabric_csv):
        print(" Processing Hyperledger Fabric raw execution CSV logs...")
        summary['Fabric'] = process_csv_log(fabric_csv)

    output_json = os.path.join(results_dir, 'summary_metrics.json')
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    print("✓ Successfully processed raw CSV hardware logs!")
    print(f"✓ Output summary JSON saved to: {output_json}\n")

    print("--- SAMPLE METRICS AT LOAD = 100 tx/s ---")
    for platform in ['Ethereum', 'Corda', 'Fabric']:
        if platform in summary and 100 in summary[platform]:
            lat = summary[platform][100]['latency']['formatted']
            tps = summary[platform][100]['tps']['formatted']
            print(f" {platform:10s} | Latency: {lat} ms | Throughput: {tps} TPS")
    print("=" * 70)

if __name__ == '__main__':
    main()
