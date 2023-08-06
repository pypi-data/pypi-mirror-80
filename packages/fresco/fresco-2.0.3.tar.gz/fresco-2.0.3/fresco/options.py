# Copyright 2015 Oliver Cope
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
import inspect
from typing import Any
from typing import Dict


class Options(dict):
    """\
    Options dictionary. An instance of this is attached to each
    :class:`fresco.core.FrescoApp` instance, as a central store for
    configuration options.
    """

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, key, value):
        self[key] = value

    def copy(self):
        return self.__class__(super().copy())

    def update_from_file(self, path, load_all=False):
        """
        Update the instance with any symbols found in the python source file at
        `path`.

        :param path: The path to a python source file
        :param load_all: If true private symbols will also be loaded into the
                         options object.
        """
        ns: Dict[str, Any] = dict()
        with open(path) as f:
            exec(f.read(), ns)
        self.update_from_dict(ns, load_all)

    def update_from_dict(self, d, load_all=False):
        """
        Update from the given list of key-value pairs.

        If ``load_all`` is True, all key-value pairs will be loaded.

        Otherwise, if the special key '__all__' is present, only those keys
        listed in __all__ will be loaded (same semantics as `from … import *`)

        Otherwise only those NOT beginning with ``_`` will be loaded.
        """
        if load_all:
            self.update(d)
        elif "__all__" in d:
            self.update((k, d[k]) for k in d["__all__"])
        else:
            self.update(
                (k, v)
                for k, v in d.items()
                if isinstance(k, str) and k and k[0] != "_"
            )

    def update_from_object(self, ob, load_all=False):
        """
        Update the instance with any symbols listed in object `ob`
        :param load_all: If true private symbols will also be loaded into the
                         options object.
        """
        self.update_from_dict(dict(inspect.getmembers(ob)), load_all)
