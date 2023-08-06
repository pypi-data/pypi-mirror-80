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

import inspect
from functools import wraps, partial
import pkgutil
import importlib


def _is_internal_module(o, module_root: str = None) -> bool:
    return (
        inspect.ismodule(o)
        and hasattr(o, "__file__")
        and o.__file__.startswith(module_root)
    )


def _is_class_with_method(cls, method: str) -> bool:
    return (
        inspect.isclass(cls)
        and hasattr(cls, method)
        and inspect.isfunction(getattr(cls, method))
    )


def _method_decorator(method, name: str):
    @wraps(method)
    def wrapper(*args, **kwargs):
        circ = method(*args, **kwargs)
        circ.name = name
        return circ

    return wrapper


def _wrap_methods(module, method_name: str):
    for cls_name, cls in inspect.getmembers(
        module, partial(_is_class_with_method, method=method_name)
    ):
        setattr(
            cls, method_name, _method_decorator(getattr(cls, method_name), cls.__name__)
        )


def _wrap_classes(mapping: dict):
    import pkgutil
    import importlib
    import warnings
    import qiskit

    for package_info in pkgutil.walk_packages(
        path=qiskit.__path__, prefix=qiskit.__name__ + "."
    ):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                module = importlib.import_module(package_info.name)
            for cls_name, wrapper in mapping.items():
                if hasattr(module, cls_name):
                    setattr(module, cls_name, wrapper)
        except ImportError:
            pass
        except NameError:
            pass


def name_internal_routines():
    from .WrappedQuantumCircuit import WrappedQuantumCircuit

    _wrap_classes({"QuantumCircuit": WrappedQuantumCircuit})

    import qiskit.aqua.algorithms
    import qiskit.aqua.components
    import qiskit.aqua.circuits
    import qiskit.aqua.operator

    _wrap_methods(qiskit.aqua.operator, "construct_evolution_circuit")
    _wrap_methods(qiskit.aqua.algorithms, "construct_circuit")
    _wrap_methods(qiskit.aqua.circuits, "construct_circuit")
    for loader, submodule_name, ispkg in pkgutil.iter_modules(
        path=qiskit.aqua.components.__path__,
        prefix=qiskit.aqua.components.__name__ + ".",
    ):
        submodule = importlib.import_module(submodule_name)
        _wrap_methods(submodule, "construct_circuit")
