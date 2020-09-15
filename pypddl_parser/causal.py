# This file is part of pypddl-parser.

# pypddl-parser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pypddl-parser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pypddl-parser.  If not, see <http://www.gnu.org/licenses/>.

class CausalGraph(object):
    def __init__(self, name, params, nodes):
        self._name    = name
        self._params   = params
        self._nodes = nodes

    @property
    def name(self):
        return self._name

    @property
    def params(self):
        return self._params[:]

    @property
    def nodes(self):
        return self._nodes[:]

    def __str__(self):
        operator_str  = '{0}({1})\n'.format(self._name, ', '.join(map(str, self._params)))
        operator_str += '>> nodes:\n    {0}\n'.format(
            '\n    '.join(str(op).replace('\n', '\n    ') for op in self._nodes))
        return operator_str

class CausalNode(object):

    def __init__(self, name, relation):
        self._name    = name
        self._relation = relation

    @property
    def name(self):
        return self._name

    @property
    def relation(self):
        return self._relation[:]

    def __str__(self):
        operator_str  = '{0}\n'.format(self._name)
        operator_str += '>> relation: {0}\n'.format(', '.join(map(str, self._relation)))
        return operator_str