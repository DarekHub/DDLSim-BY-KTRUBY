

# **DDLSim-BY-KTRUBY**  
_Distributed Deep Learning Infrastructure Simulator_  
Created by **Kaitlyn Brishae Truby** | Brown University & Broward College

---

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)  
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)  
[![Status](https://img.shields.io/badge/status-In_Development-orange)](#project-status)

---

## **:bulb: Project Summary**

**DDLSim** is an academic-grade simulator for emulating distributed deep learning training infrastructure over virtual or bare-metal nodes. It allows researchers to test and optimize training workloads under realistic network conditions such as:

- Latency and jitter  
- Packet loss  
- Node crashes or timeouts  
- Variable compute node configurations

DDLSim is built for **reproducibility**, **modularity**, and **scalability**, making it ideal for research labs, student projects, and infrastructure benchmarking.

---

## **:rocket: Key Features**

| Feature                        | Description                                                                 |
|-------------------------------|-----------------------------------------------------------------------------|
| Multi-node Training           | Runs PyTorch Distributed & MPI-based simulations                           |
| Network Fault Emulation       | Simulates delay, packet drop, and link failures                            |
| Modular Architecture          | Plugin-ready for custom models, schedulers, and loss functions             |
| Metrics & Visualization       | Export training stats to Prometheus, visualize via Grafana                 |
| Container Orchestration       | Docker/Kubernetes compatible                                                |
| Public Portal (planned)       | Live domain with hosted API & dataset access under `ilabt.be`              |

---

## **:electric_plug: Installation**

```bash
git clone https://github.com/DarekHub/DDLSim-BY-KTRUBY.git
cd DDLSim-BY-KTRUBY
pip install -r requirements.txt


---

:computer: Running the Simulator

python main.py

> This command launches a 2-process training simulation with random latency and packet loss between workers.




---

:microscope: Research Motivation

Distributed deep learning demands scalable infrastructure — yet access to realistic environments is limited.
DDLSim aims to provide a reproducible, cost-free alternative that models:

Decentralized job orchestration

Resource contention & link degradation

Agent coordination in edge-cloud hybrid topologies



---

:world_map: Roadmap

Phase	Goals

Prototype ✅	Training simulation + fault injection
Metrics 🔜	Prometheus metrics + Grafana dashboard
API 🔜	Web interface to launch/test distributed jobs
Docs & Site	Launch of docs site + open-access portal hosted with ilabt branding



---

:hammer_and_wrench: Tech Stack

Language: Python 3.8+

Libraries: PyTorch, MPI4Py, Prometheus Client

Tools: Docker, Kubernetes, Grafana, ZeroMQ

Deployment: GitHub + GitHub Pages (planned)



---

:shield: License

This project is licensed under the MIT License.
All platform attribution will be credited to ilabt.be in all public releases.


---

:handshake: Author
Supported : ilabt.imec.be
Kaitlyn Brishae Truby
Center Researcher Staff
Brown University & Broward College



---

> DDLSim bridges the gap between theory and real-world AI infrastructure challenges, empowering global researchers to simulate, test, and optimize distributed systems at no cost.




هل ترغب أن أرفعه فورًا إلى مستودعك؟  
أو أرسله لك كملف `.md` مضغوط؟

