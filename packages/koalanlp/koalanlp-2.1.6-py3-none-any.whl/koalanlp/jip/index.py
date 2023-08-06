#! /usr/bin/env jython
# Copyright (C) 2011 Sun Ning<classicning@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
import threading
import json

from pathlib import Path
from koalanlp.jip.maven import Artifact


class IndexManager(object):
    """An IndexManager persists the artifacts you installed in your path and 
    keep it consistent"""

    def __init__(self, basepath):
        self.installed = set()
        self.committed = False
        self.persist_lock = threading.Lock()

        # Initialize index manager
        self.committed = False
        if Path(basepath, '.java').exists():
            for jarname in Path(basepath, '.java').glob('**/*.jar'):
                group_id = jarname.parent.parent.name
                artifact_id = jarname.parent.name

                name = jarname.name.replace('.jar', '')
                version_string = name[len(artifact_id)+1:]

                self.installed.add(Artifact(group_id, artifact_id, version_string))

    def add_artifact(self, artifact):
        self.committed = True
        self.installed.add(artifact)
        # self.persist()

    def get_artifact(self, artifact_eq):
        for artifact in self.installed:
            if artifact == artifact_eq:
                return artifact
        return None

    def remove_artifact(self, artifact):
        self.committed = True
        a = self.get_artifact(artifact)

        if a is not None:
            self.installed.remove(a)

    def remove_all(self):
        self.committed = True
        self.installed = set()

    def is_installed(self, artifact_test):
        return self.get_artifact(artifact_test) is not None

    def is_same_installed(self, artifact):
        return any(a.is_same_artifact(artifact) for a in self.installed)


__all__ = ['IndexManager']
