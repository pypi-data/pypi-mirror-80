# ======================================================================
# Copyright CERFACS (August 2019)
# Contributor: Adrien Suau (adrien.suau@cerfacs.fr)
#
# This software is governed by the CeCILL-B license under French law and
# abiding  by the  rules of  distribution of free software. You can use,
# modify  and/or  redistribute  the  software  under  the  terms  of the
# CeCILL-B license as circulated by CEA, CNRS and INRIA at the following
# URL "http://www.cecill.info".
#
# As a counterpart to the access to  the source code and rights to copy,
# modify and  redistribute granted  by the  license, users  are provided
# only with a limited warranty and  the software's author, the holder of
# the economic rights,  and the  successive licensors  have only limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using, modifying and/or  developing or reproducing  the
# software by the user in light of its specific status of free software,
# that  may mean  that it  is complicated  to manipulate,  and that also
# therefore  means that  it is reserved for  developers and  experienced
# professionals having in-depth  computer knowledge. Users are therefore
# encouraged  to load and  test  the software's  suitability as  regards
# their  requirements  in  conditions  enabling  the  security  of their
# systems  and/or  data to be  ensured and,  more generally,  to use and
# operate it in the same conditions as regards security.
#
# The fact that you  are presently reading this  means that you have had
# knowledge of the CeCILL-B license and that you accept its terms.
# ======================================================================

from qiskit.circuit.instruction import Instruction

from ._interfaces import interfaces


class NamedRoutine(Instruction, interfaces.NamedRoutine):
    def __init__(self, name: str, num_qubits: int, num_clbits: int, params):
        super().__init__(
            name=name, num_qubits=num_qubits, num_clbits=num_clbits, params=params
        )
        self.name = name

    @staticmethod
    def from_Routine(rout: Instruction) -> "NamedRoutine":
        named_routine = NamedRoutine(
            rout.name, rout.num_qubits, rout.num_clbits, rout.params
        )
        named_routine.definition = rout.definition
        return named_routine

    @staticmethod
    def from_Routine_and_name(rout: Instruction, name: str) -> "NamedRoutine":
        named_routine = NamedRoutine(
            name, rout.num_qubits, rout.num_clbits, rout.params
        )
        named_routine.definition = rout.definition
        return named_routine

    def inverse(self) -> "NamedRoutine":
        return NamedRoutine.from_Routine_and_name(
            super().inverse(), name="D-" + self.name
        )
