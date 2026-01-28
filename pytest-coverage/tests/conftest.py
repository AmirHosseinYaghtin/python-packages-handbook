import pytest
import torch


@pytest.fixture
def input_tensor():
    return torch.randn(4, 10)
