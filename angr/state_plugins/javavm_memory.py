
from ..engines.soot.values import SimSootValue_Local, SimSootValue_ArrayRef

from ..storage.memory import SimMemory
from .keyvalue_memory import SimKeyValueMemory
from .plugin import SimStatePlugin

MAX_ARRAY_SIZE = 1000


class SimJavaVmMemory(SimMemory):
    def __init__(self, memory_id="mem", stack=None):
        super(SimJavaVmMemory, self).__init__()

        self.id = memory_id

        self._stack = [ ] if stack is None else stack
        self.heap = SimKeyValueMemory("mem")

        # Heap helper
        # TODO: ask someone how we want to manage this
        # TODO: Manage out of memory allocation
        self.max_array_size = MAX_ARRAY_SIZE

    def store(self, addr, data, size=None, condition=None, add_constraints=None, endness=None, action=None,
              inspect=True, priv=None, disable_actions=False, frame=0):

        if type(addr) is SimSootValue_Local:
            cstack = self._stack[-1+(-1*frame)]
            # A local variable
            # TODO: Implement the stacked stack frames model
            cstack.store(addr.name, data, type_=addr.type)
        elif type(addr) is SimSootValue_ArrayRef:
            reference_name = "%s[%d]" % (addr.base.name, addr.index)
            self.heap.store(reference_name, data, type_=addr.type)
        else:
            import ipdb; ipdb.set_trace()

    def load(self, addr, size=None, condition=None, fallback=None, add_constraints=None, action=None, endness=None,
             inspect=True, disable_actions=False, ret_on_segv=False, none_if_missing=False, frame=0):

        if type(addr) is SimSootValue_Local:
            cstack = self._stack[-1+(-1*frame)]
            # Load a local variable
            # TODO: Implement the stacked stack frames model
            return cstack.load(addr.name, none_if_missing)
        elif type(addr) is SimSootValue_ArrayRef:
            self.heap.load(addr.ref)
        else:
            import ipdb; ipdb.set_trace()

    @SimStatePlugin.memo
    def copy(self, memo):  # pylint: disable=unused-argument
        return SimJavaVmMemory(
            memory_id=self.id,
            stack=self._stack[::],
        )

    def push_stack_frame(self):
        self._stack.append(SimKeyValueMemory("mem"))

    def pop_stack_frame(self):
        self._stack = self._stack[:-1]

    @property
    def stack(self):
        return self._stack[-1]


from angr.sim_state import SimState
SimState.register_default('javavm_memory', SimJavaVmMemory)