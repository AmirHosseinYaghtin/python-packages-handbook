"""
Typed registry example using Protocols.

This demonstrates how to make dynamic ML patterns
understandable to static analyzers like Pylint.
this is the correct ML/MLOps pattern
"""

from typing import Dict, Protocol, Type


class Model(Protocol):
    """
    Behavioral contract for models.
    """

    def fit(self) -> None:
        ...


class ModelRegistry:
    """
    Registry mapping names to model classes
    that satisfy the Model protocol.
    """

    def __init__(self) -> None:
        self._models: Dict[str, Type[Model]] = {}

    def register(self, name: str, model_cls: Type[Model]) -> None:
        self._models[name] = model_cls

    def create(self, name: str) -> Model:
        return self._models[name]()


class LinearModel:
    """
    Concrete model implementation.
    """

    def fit(self) -> None:
        print("fitting linear model")


registry = ModelRegistry()
registry.register("linear", LinearModel)

model = registry.create("linear")
model.fit()
