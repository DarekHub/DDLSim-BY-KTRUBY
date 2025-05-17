"""
DDLSim: Distributed Deep Learning Infrastructure Simulator
==========================================================
Main Simulation Script (Advanced Edition)

Author: Kaitlyn Brishae Truby
Project: DDLSim-BY-KTRUBY
Version: 0.2.0
License: MIT
"""

import os
import time
import random
import logging
from datetime import datetime

import torch
import torch.distributed as dist
import torch.multiprocessing as mp
from torch import nn, optim
from torch.nn.parallel import DistributedDataParallel as DDP

# Optional visualization and tracking tools
try:
    from tqdm import tqdm
except ImportError:
    tqdm = lambda x: x


# === Logging Setup ===
def init_logging(rank):
    logging.basicConfig(
        filename=f"ddlsim_node{rank}.log",
        level=logging.INFO,
        format="%(asctime)s [Node %(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


# === Distributed Setup and Cleanup ===
def setup(rank, world_size):
    os.environ["MASTER_ADDR"] = "127.0.0.1"
    os.environ["MASTER_PORT"] = "29500"
    dist.init_process_group("gloo", rank=rank, world_size=world_size)
    init_logging(rank)
    logging.info(f"Initialized node {rank}/{world_size}")


def cleanup():
    dist.destroy_process_group()


# === Simulate Network Behavior ===
def simulate_network(epoch, rank):
    latency = random.uniform(0.01, 0.25)
    time.sleep(latency)
    if random.random() < 0.03:
        logging.warning(f"Epoch {epoch}: Packet dropped on node {rank}")
        return False
    return True


# === Define Neural Model (Extendable) ===
class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.fc1 = nn.Linear(10, 50)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(50, 10)

    def forward(self, x):
        return self.fc2(self.relu(self.fc1(x)))


# === Training Logic ===
def train_node(rank, world_size):
    setup(rank, world_size)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = SimpleModel().to(device)
    ddp_model = DDP(model)

    optimizer = optim.Adam(ddp_model.parameters(), lr=0.001)
    criterion = nn.MSELoss()

    logging.info(f"Training started on device: {device}")

    for epoch in range(1, 11):
        if not simulate_network(epoch, rank):
            continue

        inputs = torch.randn(32, 10).to(device)
        targets = torch.randn(32, 10).to(device)

        optimizer.zero_grad()
        outputs = ddp_model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()

        logging.info(f"[Epoch {epoch}] Loss: {loss.item():.5f}")
        if rank == 0:
            print(f"[Node {rank}] Epoch {epoch} | Loss: {loss.item():.5f}")

    logging.info("Training completed.")
    cleanup()


# === Main Entry ===
def main():
    WORLD_SIZE = 4  # Number of nodes
    print(f"[{datetime.now()}] Launching DDLSim with {WORLD_SIZE} nodes...")
    mp.spawn(train_node, args=(WORLD_SIZE,), nprocs=WORLD_SIZE, join=True)
    print(f"[{datetime.now()}] Simulation complete.")


if __name__ == "__main__":
    main()