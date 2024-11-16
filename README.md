![SnowPeak](./logostuff.jpg)

# SnowPeak: Distributed Ski Resort Monitoring System
[![Version](https://img.shields.io/badge/version-1.0.0-informational.svg)]()
[![License](https://img.shields.io/badge/License-APACHE-lightgrey.svg)](LICENSE)
[![GitHub contributors](https://img.shields.io/badge/contributors-4-orange.svg)]()

[![GitHub stars](https://img.shields.io/github/stars/Pillangocska/SnowPeak.svg)]()
[![GitHub forks](https://img.shields.io/github/forks/Pillangocska/SnowPeak.svg)]()
[![GitHub issues](https://img.shields.io/github/issues/Pillangocska/SnowPeak.svg)]()

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)]()
[![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=flat&logo=kubernetes&logoColor=white)]()
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)]()


A distributed system for real-time monitoring and control of ski resort lifts.

## Prerequisites

Before installation, ensure you have the following dependencies installed:

- Kubernetes cluster or Minikube (v1.20+)
- kubectl CLI tool
- Container runtime (Docker, containerd, or CRI-O)
- Operating System: Windows 10/11 or any modern UNIX based OS

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/snowpeak.git
   cd snowpeak
   ```

2. Deploy the application:

   **Windows**:
   ```powershell
   .\k8s\start_on_windows.ps1
   ```

   **Linux/macOS**:
   ```bash
   ./k8s/start_on_unix_based.sh
   ```

## Documentation

For detailed documentation, please visit our [Docs](./docs/).

## License

This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details.



---

© 2024 SnowPeak Team. All rights reserved.
