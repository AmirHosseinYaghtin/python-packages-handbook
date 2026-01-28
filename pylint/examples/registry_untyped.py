"""
Untyped registry example.

This file intentionally omits type hints to demonstrate
why static analyzers struggle with dynamic ML patterns.
"""

class ModelRegistry:
    """
    Simple registry mapping string names to model classes.
    """

    def __init__(self):
        self._models = {}

    def register(self, name, model_cls):
        """
        Register a model class under a string name.
        """
        self._models[name] = model_cls

    def create(self, name):
        """
        Create an instance of the registered model.
        """
        return self._models[name]()


class LinearModel:
    """
    Example model with a fit method.
    """

    def fit(self):
        print("fitting linear model")


registry = ModelRegistry()
registry.register("linear", LinearModel)

model = registry.create("linear")
model.fit()
