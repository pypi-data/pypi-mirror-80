# -*- encoding: utf-8 -*-
# ShiftDivMod v0.4.3
# Implement faster divmod() for moduli with trailing 0 bits
# Copyright © 2020, Shlomi Fish.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions, and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions, and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the author of this software nor the names of
#    contributors to this software may be used to endorse or promote
#    products derived from this software without specific prior written
#    consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Implement faster divmod() for moduli with trailing 0 bits

:Copyright: © 2020, Shlomi Fish.
:License: BSD (see /LICENSE).
"""

__title__ = 'ShiftDivMod'
__version__ = '0.4.3'
__author__ = 'Shlomi Fish'
__license__ = '3-clause BSD'
__docformat__ = 'restructuredtext en'

__all__ = ()

# import gettext
# G = gettext.translation('shift_divmod', '/usr/share/locale', fallback='C')
# _ = G.gettext
# The Expat License
#
# Copyright (c) 2020, Shlomi Fish
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

class ShiftDivMod:
    """Implement faster divmod() (and mod()) for moduli with trailing 0 bits"""
    def __init__(self, base, shift):
        """Initialize with n = (base << shift)"""
        self.base = base
        self.shift = shift
        self.mask = (1 << shift) - 1
        self.n = base << shift

    @classmethod
    def from_int(cls, n):
        """Initialize with base n"""
        s = 0
        for offset in (200000, 20000, 2000, 200, 20, 1):
            bits_mask = (1 << offset) - 1
            while n & bits_mask == 0:
                s += offset
                n >>= offset
        return cls(n, s)

    def divmod(self, inp):
        """calculate divmod(inp, self.n)"""
        if inp < self.n:
            return 0, inp
        div, mod = divmod((inp >> self.shift), self.base)
        return div, ((mod << self.shift) | (inp & self.mask))

    def mod(self, inp):
        """calculate inp % self.n . Uses .divmod() ."""
        return self.divmod(inp)[1]

    def div(self, inp):
        """calculate inp // self.n . Uses .divmod() ."""
        return self.divmod(inp)[0]
