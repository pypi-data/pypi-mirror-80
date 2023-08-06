#!/usr/bin/env python3
# thoth-adviser
# Copyright(C) 2020 Fridolin Pokorny
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Test wrap adding information about Intel's MKL env variable configuration."""

import jsonpatch
import yaml

from thoth.adviser.state import State
from thoth.adviser.wraps import MKLThreadsWrap

from ...base import AdviserTestCase


class TestMKLThreadsWrap(AdviserTestCase):
    """Test Intel's MKL thread env info wrap."""

    _DEPLOYMENT_CONFIG = """\
apiVersion: apps.openshift.io/v1
kind: DeploymentConfig
metadata:
  name: foo
  namespace: some-namespace
spec:
  replicas: 1
  selector:
    service: foo
  template:
    spec:
      containers:
      - image: "foo:latest"
        env:
        - name: APP_MODULE
          value: "foo"
"""

    def test_run_justification_noop(self) -> None:
        """Test no operation when PyTorch is not present."""
        state = State()
        state.add_resolved_dependency(("micropipenv", "0.1.4", "https://pypi.org/simple"))
        assert not state.justification

        unit = MKLThreadsWrap()
        unit.run(state)

        assert len(state.justification) == 0

    @classmethod
    def _check_advised_manifest_changes(cls, state: State) -> None:
        """Check correctness of the advised manifest changes returned."""
        assert len(state.advised_manifest_changes) == 1
        assert state.advised_manifest_changes[0] == [
            {
                "apiVersion:": "apps.openshift.io/v1",
                "kind": "DeploymentConfig",
                "patch": {
                    "op": "add",
                    "path": "/spec/template/spec/containers/0/env/0",
                    "value": {"name": "OMP_NUM_THREADS", "value": "1"},
                },
            }
        ]
        patch = jsonpatch.JsonPatch(obj["patch"] for obj in state.advised_manifest_changes[0])
        deployment_config = yaml.safe_load(cls._DEPLOYMENT_CONFIG)
        assert jsonpatch.apply_patch(deployment_config, patch) == {
            "apiVersion": "apps.openshift.io/v1",
            "kind": "DeploymentConfig",
            "metadata": {"name": "foo", "namespace": "some-namespace"},
            "spec": {
                "replicas": 1,
                "selector": {"service": "foo"},
                "template": {
                    "spec": {
                        "containers": [
                            {
                                "env": [
                                    {"name": "OMP_NUM_THREADS", "value": "1"},
                                    {"name": "APP_MODULE", "value": "foo"},
                                ],
                                "image": "foo:latest",
                            }
                        ]
                    }
                },
            },
        }

    def test_run_add_justification(self) -> None:
        """Test adding information Intel's MKL environment variable."""
        state = State()
        state.add_resolved_dependency(("pytorch", "1.4.0", "https://pypi.org/simple"))
        assert len(state.advised_manifest_changes) == 0
        assert not state.justification

        unit = MKLThreadsWrap()
        unit.run(state)

        assert len(state.justification) == 1
        assert set(state.justification[0].keys()) == {"type", "message", "link"}
        assert state.justification[0]["type"] == "WARNING"
        assert state.justification[0]["link"], "Empty link to justification document provided"

        self._check_advised_manifest_changes(state)

    def test_run_add_justification_intel_tf(self) -> None:
        """Test adding information Intel's MKL environment variable."""
        state = State()
        state.add_resolved_dependency(("intel-tensorflow", "2.2.0", "https://pypi.org/simple"))
        assert len(state.advised_manifest_changes) == 0
        assert not state.justification

        unit = MKLThreadsWrap()
        unit.run(state)

        assert len(state.justification) == 2

        for i in range(2):
            assert set(state.justification[i].keys()) == {"type", "message", "link"}
            assert state.justification[i]["type"] == "WARNING"
            assert state.justification[i]["link"], "Empty link to justification document provided"

        self._check_advised_manifest_changes(state)
