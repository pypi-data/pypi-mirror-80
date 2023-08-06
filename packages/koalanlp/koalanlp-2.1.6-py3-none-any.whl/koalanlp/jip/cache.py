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
import codecs
import os
import shutil

from koalanlp.jip.repository import MavenRepos


class CacheRepository(MavenRepos):
    def __init__(self, basepath=None):
        if basepath is None:
            basepath = os.getcwd()

        uri = os.path.expanduser(os.path.join(str(basepath), '.java', 'cache'))
        if not os.path.exists(uri):
            os.makedirs(uri)

        super(CacheRepository, self).__init__('cache', uri)

    def get_artifact_uri(self, artifact, ext):
        directory = self.get_artifact_dir(artifact)
        name = artifact.artifact + "-" + artifact.version + "." + ext

        return os.path.join(self.uri, directory, name)

    def get_artifact_dir(self, artifact):
        directory = os.path.join(self.uri, artifact.group,
                                 artifact.artifact)
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory

    def download_jar(self, artifact, local_path=None):
        path = self.get_artifact_uri(artifact, 'jar')
        shutil.copy(path, local_path)

    def download_pom(self, artifact, local_path=None):
        path = self.get_artifact_uri(artifact, 'pom')
        if os.path.exists(path):
            if local_path:
                shutil.copy(path, local_path)

            f = codecs.open(path, mode='r', encoding='utf-8')
            data = f.read()
            f.close()
            return data
        else:
            return None

    def put_pom(self, artifact, data):
        path = self.get_artifact_uri(artifact, 'pom')
        f = codecs.open(path, mode='w', encoding='utf-8')
        f.write(data)
        f.close()

    def put_jar(self, artifact, jarpath):
        path = self.get_artifact_uri(artifact, 'jar')
        shutil.copy(jarpath, path)


class CacheManager(object):
    def __init__(self, basepath):
        self.enable = True
        self.cache = CacheRepository(basepath)

    def set_enable(self, enable):
        self.enable = enable

    def get_artifact_pom(self, artifact, topath=None):
        if self.enable:
            return self.cache.download_pom(artifact, topath)
        else:
            return None

    def get_artifact_jar(self, artifact, topath):
        self.cache.download_jar(artifact, topath)

    def put_artifact_pom(self, artifact, data):
        self.cache.put_pom(artifact, data)

    def put_artifact_jar(self, artifact, jarpath):
        self.cache.put_jar(artifact, jarpath)

    def as_repos(self):
        return self.cache

    def get_cache_path(self):
        return self.cache.uri

    def get_jar_path(self, artifact, filepath=False):
        if filepath:
            return self.cache.get_artifact_uri(artifact, 'jar')
        else:
            return self.cache.get_artifact_dir(artifact)

    def is_artifact_in_cache(self, artifact, jar=True):
        pom_in_cache = os.path.exists(
            self.cache.get_artifact_uri(artifact, 'pom'))
        jar_in_cache = os.path.exists(
            self.cache.get_artifact_uri(artifact, 'jar'))
        if jar:
            return pom_in_cache and jar_in_cache
        else:
            return pom_in_cache


__all__ = ['CacheManager']
