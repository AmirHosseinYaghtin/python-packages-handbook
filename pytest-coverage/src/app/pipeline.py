import torch
import torch.nn as nn


def build_model(input_dim: int, output_dim: int):
    if input_dim <= 0:
        raise ValueError("input_dim must be positive")
    return nn.Linear(input_dim, output_dim)


def forward_pass(model, x):
    model.eval()
    with torch.no_grad():
        return model(x)


def save_model(model, path):
    torch.save(model.state_dict(), path)


def load_model(input_dim, output_dim, path):
    model = build_model(input_dim, output_dim)
    state = torch.load(path)
    model.load_state_dict(state)
    return model
