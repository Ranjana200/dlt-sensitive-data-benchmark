const fs = require('fs');
const path = require('path');

function calculateStats(values) {
    const n = values.length;
    if (n === 0) return { mean: 0, sd: 0, ci95Lower: 0, ci95Upper: 0, formatted: "N/A" };
    const mean = values.reduce((a, b) => a + b, 0) / n;
    const variance = n > 1 ? values.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / (n - 1) : 0;
    const sd = Math.sqrt(variance);
    const marginOfError = n > 1 ? 1.96 * (sd / Math.sqrt(n)) : 0;
    return {
        mean: parseFloat(mean.toFixed(2)),
        sd: parseFloat(sd.toFixed(2)),
        ci95Lower: parseFloat((mean - marginOfError).toFixed(2)),
        ci95Upper: parseFloat((mean + marginOfError).toFixed(2)),
        formatted: `${mean.toFixed(2)} ± ${sd.toFixed(2)} [95% CI: ${(mean - marginOfError).toFixed(2)} - ${(mean + marginOfError).toFixed(2)}]`
    };
}

function processCsv(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    const lines = content.trim().split('\n');
    const header = lines[0].split(',');
    
    const loads = {};
    for (let i = 1; i < lines.length; i++) {
        if (!lines[i].trim()) continue;
        const cols = lines[i].split(',');
        const load = parseInt(cols[1]);
        if (!loads[load]) loads[load] = { latencies: [], tps: [], cpu: [], ram: [] };
        loads[load].latencies.push(parseFloat(cols[3]));
        loads[load].tps.push(parseFloat(cols[4]));
        loads[load].cpu.push(parseFloat(cols[6]));
        loads[load].ram.push(parseFloat(cols[7]));
    }

    const stats = {};
    for (const load of Object.keys(loads).sort((a,b)=>a-b)) {
        stats[load] = {
            latency: calculateStats(loads[load].latencies),
            tps: calculateStats(loads[load].tps),
            cpu: calculateStats(loads[load].cpu),
            ram: calculateStats(loads[load].ram)
        };
    }
    return stats;
}

function main() {
    const resultsDir = path.join(__dirname, '..', 'results');
    const summary = {
        Ethereum: processCsv(path.join(resultsDir, 'raw_eth_execution.csv')),
        Corda: processCsv(path.join(resultsDir, 'raw_corda_execution.csv')),
        Fabric: processCsv(path.join(resultsDir, 'raw_fabric_execution.csv'))
    };

    const outputJson = path.join(resultsDir, 'summary_metrics.json');
    fs.writeFileSync(outputJson, JSON.stringify(summary, null, 2), 'utf8');
    console.log("✓ Successfully parsed raw hardware CSV logs and computed summary_metrics.json!");
}

main();
