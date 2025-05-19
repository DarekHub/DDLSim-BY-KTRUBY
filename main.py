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

from tqdm import tqdm  # Assume installed


def init_logging(rank: int) -> None:
    """Initialize logging for each node with file handler."""
    logging.basicConfig(
        filename=f"ddlsim_node{rank}.log",
        level=logging.INFO,
        format="%(asctime)s [Node %(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def setup(rank: int, world_size: int) -> None:
    """Set up distributed environment and logging."""
    os.environ["MASTER_ADDR"] = "127.0.0.1"
    os.environ["MASTER_PORT"] = "29500"
    dist.init_process_group("gloo", rank=rank, world_size=world_size)
    init_logging(rank)
    logging.info("Initialized node %d/%d", rank, world_size)


def cleanup() -> None:
    """Clean up distributed environment."""
    dist.destroy_process_group()


def simulate_network(epoch: int, rank: int) -> bool:
    """Simulate network latency and possible packet drop."""
    latency = random.uniform(0.01, 0.25)
    time.sleep(latency)
    if random.random() < 0.03:
        logging.warning("Epoch %d: Packet dropped on node %d", epoch, rank)
        return False
    return True


class SimpleModel(nn.Module):
    """A simple feedforward neural network model."""

    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(10, 50)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(50, 10)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass."""
        return self.fc2(self.relu(self.fc1(x)))


def train_node(rank: int, world_size: int) -> None:
    """Training process for each distributed node."""
    setup(rank, world_size)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = SimpleModel().to(device)
    ddp_model = DDP(model)

    optimizer = optim.Adam(ddp_model.parameters(), lr=0.001)
    criterion = nn.MSELoss()

    logging.info("Training started on device: %s", device)

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

        logging.info("[Epoch %d] Loss: %.5f", epoch, loss.item())
        if rank == 0:
            print("[Node %d] Epoch %d | Loss: %.5f", rank, epoch, loss.item())

    logging.info("Training completed.")
    cleanup()


def main() -> None:
    """Main entry point for launching the distributed simulation."""
    world_size = 4  # Number of nodes
    print("[%s] Launching DDLSim with %d nodes..." % (datetime.now(), world_size))
    mp.spawn(train_node, args=(world_size,), nprocs=world_size, join=True)
    print("[%s] Simulation complete." % datetime.now())


if __name__ == "__main__":
    main()
