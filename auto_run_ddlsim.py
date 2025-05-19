import os
import time
import random
from datetime import datetime
import torch
import torch.distributed as dist
import torch.multiprocessing as mp
from torch import nn, optim
from torch.nn.parallel import DistributedDataParallel as DDP

def setup(rank, world_size):
    os.environ["MASTER_ADDR"] = "127.0.0.1"
    os.environ["MASTER_PORT"] = "29500"
    dist.init_process_group("gloo", rank=rank, world_size=world_size)

def cleanup():
    dist.destroy_process_group()

class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.fc = nn.Linear(10, 10)

    def forward(self, x):
        return self.fc(x)

def simulate_network(epoch, rank):
    delay = random.uniform(0.01, 0.1)
    time.sleep(delay)
    return True

def train(rank, world_size, log_file):
    setup(rank, world_size)
    device = torch.device("cpu")
    model = SimpleModel().to(device)
    ddp_model = DDP(model)
    optimizer = optim.SGD(ddp_model.parameters(), lr=0.01)
    loss_fn = nn.MSELoss()

    for epoch in range(1, 6):
        if not simulate_network(epoch, rank):
            continue
        inputs = torch.randn(32, 10).to(device)
        targets = torch.randn(32, 10).to(device)
        optimizer.zero_grad()
        outputs = ddp_model(inputs)
        loss = loss_fn(outputs, targets)
        loss.backward()
        optimizer.step()

        if rank == 0:
            log_file.write(f"Epoch {epoch} | Loss: {loss.item():.4f}\n")
            print(f"[Epoch {epoch}] Loss: {loss.item():.4f}")
    cleanup()

def run_auto_ddlsim():
    world_size = 2
    os.makedirs("logs", exist_ok=True)
    log_name = datetime.now().strftime("ddlsim_%Y%m%d_%H%M%S.log")
    log_path = os.path.join("logs", log_name)

    with open(log_path, "w") as log_file:
        mp.spawn(train, args=(world_size, log_file), nprocs=world_size, join=True)

if __name__ == "__main__":
    run_auto_ddlsim()
