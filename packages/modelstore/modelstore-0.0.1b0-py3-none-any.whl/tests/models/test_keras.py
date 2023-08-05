#    Copyright 2020 Neal Lathia
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import json
import os

import keras
import numpy as np
import pytest

from modelstore.models.keras import KerasManager, _save_model, save_json

# pylint: disable=protected-access
# pylint: disable=redefined-outer-name


@pytest.fixture()
def keras_model():
    inputs = keras.Input(shape=(10,))
    outputs = keras.layers.Dense(1)(inputs)
    model = keras.Model(inputs, outputs)
    model.compile(optimizer="adam", loss="mean_squared_error")
    return model


def test_required_kwargs():
    mngr = KerasManager()
    assert mngr._required_kwargs() == ["model"]


def test_get_functions(keras_model):
    mngr = KerasManager()
    assert len(mngr._get_functions(model=keras_model)) == 2


def test_save_model(keras_model, tmp_path):
    exp = os.path.join(tmp_path, "model")
    model_path = _save_model(tmp_path, keras_model)
    assert exp == model_path
    assert os.path.isdir(model_path)

    model = keras.models.load_model(model_path)
    test_input = np.random.random((128, 10))
    np.testing.assert_allclose(
        keras_model.predict(test_input), model.predict(test_input)
    )


def test_model_json(keras_model, tmp_path):
    exp = os.path.join(tmp_path, "model_config.json")
    file_path = save_json(tmp_path, "model_config.json", keras_model.to_json())
    assert file_path == exp
    with open(file_path, "r") as lines:
        model_json = json.loads(lines.read())
    model = keras.models.model_from_json(model_json)
    assert model.count_params() == keras_model.count_params()
    assert len(model.layers) == len(keras_model.layers)
    for i in range(len(model.layers)):
        assert (
            model.layers[i].__class__.__name__
            == keras_model.layers[i].__class__.__name__
        )
        assert model.layers[i].name == keras_model.layers[i].name
