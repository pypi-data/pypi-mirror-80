# ======================================================================
# Copyright CERFACS (July 2019)
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

from typing import Union, Iterable

from ._interfaces import interfaces

from qiskit.circuit import QuantumCircuit, Instruction


class RoutineWrapper(interfaces.RoutineWrapper):
    def __init__(self, qcirc_or_instr: Union[QuantumCircuit, Instruction]):
        super().__init__()
        self._main_instruction: Instruction = qcirc_or_instr
        if isinstance(self._main_instruction, QuantumCircuit):
            self._main_instruction = self._main_instruction.to_instruction()
        self._main_quantum_circuit: QuantumCircuit = self._main_instruction.definition

    def __iter__(self) -> Iterable["RoutineWrapper"]:
        for instr, qubits, clbits in self._main_quantum_circuit.data:
            yield RoutineWrapper(instr)

    @property
    def ops(self):
        return list(self)

    @property
    def is_base(self):
        return self._main_quantum_circuit is None

    @property
    def name(self):
        return self._main_instruction.name

    def __hash__(self):
        """Get the hash of the wrapped instruction

        :return: hash of the wrapped instruction
        """
        instr = self._main_instruction
        return hash((instr.name, tuple(instr.params)))

    def __eq__(self, other: "RoutineWrapper"):
        """Equality testing.

        :param other: right-hand side of the equality operator
        :return: True if self and other are equal, else False
        """
        sinstr: Instruction = self._main_instruction
        oinstr: Instruction = other._main_instruction
        return (
            sinstr.name == oinstr.name
            and len(sinstr.params) == len(oinstr.params)
            and all(sp == op for sp, op in zip(sinstr.params, oinstr.params))
        )
