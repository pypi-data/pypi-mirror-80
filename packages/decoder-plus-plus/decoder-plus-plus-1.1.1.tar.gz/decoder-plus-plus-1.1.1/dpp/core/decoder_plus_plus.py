# vim: ts=8:sts=8:sw=8:noexpandtab
#
# This file is part of Decoder++
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

class DecoderPlusPlus(object):
    """ The interface of DecoderPlusPlus which is used within the python interactive console. """

    def __init__(self, input: str):
        """
        Initializes DecoderPlusPlus with the specified input.
        :param input: the input which should be transformed.
        """
        self._input = input

    def decode(self) -> 'DecoderPlusPlus':
        """ Returns the decoder interface which encapsulates all possible decoding methods. """
        return Decoder(self._input)

    def encode(self) -> 'DecoderPlusPlus':
        """ Returns the encoder interface which encapsulates all possible encoding methods. """
        return Encoder(self._input)

    def hash(self) -> 'DecoderPlusPlus':
        """ Returns the hash interface which encapsulates all possible hashing methods. """
        return Hasher(self._input)

    def script(self) -> 'DecoderPlusPlus':
        """ Returns the script interface which encapsulates all possible scripting methods. """
        return Script(self._input)

    def run(self):
        """ Starts the transformation process and returns the transformed input. """
        return self._input


Encoder = type('obj', (DecoderPlusPlus,), {})
Decoder = type('obj', (DecoderPlusPlus,), {})
Hasher = type('obj', (DecoderPlusPlus,), {})
Script = type('obj', (DecoderPlusPlus,), {})