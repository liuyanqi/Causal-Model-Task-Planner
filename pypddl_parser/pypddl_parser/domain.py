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

class Domain(object):

    def __init__(self, name, causals):
        self._name = name
        self._causals = causals

    @property
    def name(self):
        return self._name

    @property
    def causals(self):
        return self._causals[:]

    def __str__(self):
        domain_str  = '@ Domain: {0}\n'.format(self._name)
        domain_str += '>> causals graph:\n    {0}\n'.format(
            '\n    '.join(str(op).replace('\n', '\n    ') for op in self._causals))
        return domain_str
