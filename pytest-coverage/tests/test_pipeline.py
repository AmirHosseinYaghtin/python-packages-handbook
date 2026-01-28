import pytest
import torch
from app.pipeline import (
    build_model,
    forward_pass,
    save_model,
    load_model,
)


# -------- build_model tests --------

def test_build_model_valid():
    model = build_model(10, 3)
    assert isinstance(model, torch.nn.Linear)
    assert model.in_features == 10
    assert model.out_features == 3


def test_build_model_invalid():
    with pytest.raises(ValueError):
        build_model(0, 3)


# -------- forward_pass tests --------

def test_forward_shape(input_tensor):
    model = build_model(10, 3)
    out = forward_pass(model, input_tensor)

    assert isinstance(out, torch.Tensor)
    assert out.shape == (4, 3)


def test_forward_no_grad(input_tensor):
    model = build_model(10, 3)
    out = forward_pass(model, input_tensor)

    assert not out.requires_grad


# -------- serialization tests --------

def test_model_save_and_load(tmp_path, input_tensor):
    model = build_model(10, 3)

    path = tmp_path / "model.pt"
    save_model(model, path)

    loaded = load_model(10, 3, path)

    out1 = forward_pass(model, input_tensor)
    out2 = forward_pass(loaded, input_tensor)

    assert out1.shape == out2.shape
