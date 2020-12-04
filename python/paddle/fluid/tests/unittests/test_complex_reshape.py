# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import paddle.fluid as fluid
import paddle
from paddle import complex as cpx
import paddle.fluid.dygraph as dg
import numpy as np
import unittest


class TestComplexReshape(unittest.TestCase):
    def setUp(self):
        self._dtypes = ["float32", "float64"]
        self._places = [paddle.CPUPlace()]
        if fluid.core.is_compiled_with_cuda():
            self._places.append(paddle.CUDAPlace(0))

    def test_case1(self):
        for dtype in self._dtypes:
            x_np = np.random.randn(
                2, 3, 4).astype(dtype) + 1j * np.random.randn(2, 3,
                                                              4).astype(dtype)
            shape = (2, -1)
            for place in self._places:
                with dg.guard(place):
                    x_var = dg.to_variable(x_np)
                    y_var = cpx.reshape(x_var, shape)
                    y_np = y_var.numpy()
                    np.testing.assert_allclose(np.reshape(x_np, shape), y_np)

    def test_case2(self):
        for dtype in self._dtypes:
            x_np = np.random.randn(
                2, 3, 4).astype(dtype) + 1j * np.random.randn(2, 3,
                                                              4).astype(dtype)
            shape = (0, -1)
            shape_ = (2, 12)
            for place in self._places:
                with dg.guard(place):
                    x_var = dg.to_variable(x_np)
                    y_var = cpx.reshape(x_var, shape, inplace=True)
                    y_np = y_var.numpy()
                    np.testing.assert_allclose(np.reshape(x_np, shape_), y_np)

    def test_case3(self):
        for dtype in self._dtypes:
            x_np = np.random.randn(2, 3, 4) + 1j * np.random.randn(2, 3, 4)
            shape = (2, -1)
            for place in self._places:
                with dg.guard(place):
                    x_var = paddle.Tensor(
                        value=x_np,
                        place=fluid.framework._current_expected_place(),
                        persistable=False,
                        zero_copy=None,
                        stop_gradient=True)
                    y_var = fluid.layers.reshape(x_var, shape)
                    y_np = y_var.numpy()
                    np.testing.assert_allclose(np.reshape(x_np, shape), y_np)

    def test_case4(self):
        for dtype in self._dtypes:
            x_np = np.random.randn(2, 3, 4) + 1j * np.random.randn(2, 3, 4)
            shape = (0, -1)
            shape_ = (2, 12)

            for place in self._places:
                with dg.guard(place):
                    x_var = paddle.Tensor(
                        value=x_np,
                        place=fluid.framework._current_expected_place(),
                        persistable=False,
                        zero_copy=None,
                        stop_gradient=True)
                    y_var = fluid.layers.reshape(x_var, shape)
                    y_np = y_var.numpy()
                    np.testing.assert_allclose(np.reshape(x_np, shape_), y_np)


if __name__ == "__main__":
    unittest.main()
