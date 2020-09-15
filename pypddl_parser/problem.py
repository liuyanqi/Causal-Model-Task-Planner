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

import itertools


class Problem(object):

    def __init__(self, name, domain, goal, hint):
        self._name = name
        self._domain = domain
        self._goal = set(map(str, goal))
        self._hint = hint

    @property
    def name(self):
        return self._name

    @property
    def domain(self):
        return self._domain

    @property
    def goal(self):
        return self._goal.copy()

    @property
    def hint(self):
        return self._hint

    def __str__(self):
        problem_str  = '@ Problem: {0}\n'.format(self._name)
        problem_str += '>> domain: {0}\n'.format(self._domain)
        problem_str += '>> goal:\n{0}\n'.format(', '.join(sorted(self._goal)))
        problem_str += '>> hint: {0}\n'.format(self._hint)
        return problem_str
