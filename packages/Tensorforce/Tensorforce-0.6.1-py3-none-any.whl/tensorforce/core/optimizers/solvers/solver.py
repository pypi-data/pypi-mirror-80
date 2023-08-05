# Copyright 2020 Tensorforce Team. All Rights Reserved.
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
# ==============================================================================

from tensorforce.core import Module


class Solver(Module):
    """
    Generic TensorFlow-based solver which solves a not yet further specified equation/optimization
    problem.
    """

    def solve(self, *args, fn_x=None):
        """
        Solves an equation/optimization for $x$ involving an expression $f(x)$.

        Args:
            *args: Additional solver-specific arguments.
            fn_x: A callable returning an expression $f(x)$ given $x$.

        Returns:
            A solution $x$ to the problem as given by the solver.
        """
        raise NotImplementedError
