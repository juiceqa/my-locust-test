# 🚀 Locust Performance Testing

This repository contains automated load and spike testing scripts using [Locust](https://locust.io/) and GitHub Actions. The tests simulate traffic against [JSONPlaceholder](https://jsonplaceholder.typicode.com/) as a target host, but can be customized for any API.

## 🔧 Scripts

- **`locust.py`** - Simulates a standard load test with 50 users over 2 minutes.
- **`spike_test.py`** - Simulates a spike test with 200 users spawned rapidly to test system resilience.

## 🛠️ GitHub Actions Workflow

When a push is made to the `main` branch:

1. The `locust.py` script runs a standard load test.
2. The `spike_test.py` script runs a spike test.
3. HTML reports are generated for both tests.
4. Reports are uploaded as artifacts.

## 🧪 Run Tests Locally

### Install Locust

```bash
pip install locust
```

### Run Standard Load Test

```bash
locust -f locust.py --headless --users 50 --spawn-rate 5 --host https://jsonplaceholder.typicode.com --run-time 2m --html locust_report.html
```

### Run Spike Test

```bash
locust -f spike_test.py --headless --users 200 --spawn-rate 100 --host https://jsonplaceholder.typicode.com --run-time 2m --stop-timeout 15 --html spike_report.html --reset-stats
```

### 📂 Artifacts

Download HTML reports directly from the GitHub Actions summary page under the "Artifacts" section.

### 📜 License

MIT License. Feel free to adapt these scripts for your own performance testing needs.
