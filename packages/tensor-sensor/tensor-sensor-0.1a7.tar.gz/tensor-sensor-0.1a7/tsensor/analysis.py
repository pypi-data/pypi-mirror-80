import os
import sys
import traceback
import torch
import inspect
import graphviz
import tempfile

from IPython.display import display, SVG
from IPython import get_ipython
import matplotlib.pyplot as plt

import tsensor

class clarify:
    def __init__(self):
        pass

    def __enter__(self):
        self.frame = sys._getframe().f_back # where do we start tracking
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is not None:
            if not self.is_interesting_exception(exc_value):
                return
            # print("exception:", exc_value, exc_traceback)
            # traceback.print_tb(exc_traceback, limit=5, file=sys.stdout)
            exc_frame = self.deepest_frame(exc_traceback)
            module, name, filename, line, code = self.info(exc_frame)
            # print('info', module, name, filename, line, code)
            if code is not None:
                # could be internal like "__array_function__ internals" in numpy
                self.process_exception(code, exc_frame, exc_value)

    def process_exception(self, code, exc_frame, exc_value):
        augment = ""
        try:
            p = tsensor.parsing.PyExprParser(code)
            t = p.parse()
            if t is None: # Couldn't parse the code; must ignore
                return
            try:
                t.eval(exc_frame)
            except tsensor.ast.IncrEvalTrap as exc:
                subexpr = exc.offending_expr
                # print("trap evaluating:\n", repr(subexpr), "\nin", repr(t))
                explanation = subexpr.clarify()
                if explanation is not None:
                    augment = explanation
        except BaseException as e:
            print(f"exception while eval({code})", e)
            traceback.print_tb(e.__traceback__, limit=5, file=sys.stdout)
        # Reuse exception but overwrite the message
        if len(exc_value.args)==0:
            exc_value._message = exc_value.message + "\n" + augment
        else:
            exc_value.args = [exc_value.args[0] + "\n" + augment]

    def is_interesting_exception(self, e):
        sentinels = {'matmul', 'THTensorMath', 'tensor', 'tensors', 'dimension',
                     'not aligned', 'size mismatch', 'shape', 'shapes'}
        if len(e.args)==0:
            msg = e.message
        else:
            msg = e.args[0]
        return sum([s in msg for s in sentinels])>0

    def deepest_frame(self, exc_traceback):
        """
        Don't trace into internals of numpy/torch/tensorflow; we want to reset frame
        to where in the user's python code it asked the tensor lib to perform an
        invalid operation.

        To detect libraries, look for code whose filename has "site-packages/{package}"
        """
        tb = exc_traceback
        packages = ['numpy','torch','tensorflow']
        packages = [os.path.join('site-packages',p) for p in packages]
        packages += ['<__array_function__'] # numpy seems to not have real filename
        prev = tb
        while tb != None:
            filename = tb.tb_frame.f_code.co_filename
            reached_lib = [p in filename for p in packages]
            if sum(reached_lib)>0:
                break
            prev = tb
            tb = tb.tb_next
        return prev.tb_frame

    def info(self, frame):
        if hasattr(frame, '__name__'):
            module = frame.f_globals['__name__']
        else:
            module = None
        info = inspect.getframeinfo(frame)
        if info.code_context is not None:
            code = info.code_context[0].strip()
        else:
            code = None
        filename, line = info.filename, info.lineno
        name = info.function
        return module, name, filename, line, code

class TensorTracer:
    def __init__(self, savefig:str=None, format="svg", modules=['__main__'], filenames=[]):
        self.savefig = savefig
        self.format = format
        self.modules = modules
        self.filenames = filenames
        self.exceptions = set()
        self.linecount = 0
        self.views = []

    def listener(self, frame, event, arg):
        module = frame.f_globals['__name__']
        if module not in self.modules:
            return

        info = inspect.getframeinfo(frame)
        filename, line = info.filename, info.lineno
        name = info.function
        if len(self.filenames)>0 and filename not in self.filenames:
            return

        if event=='call':
            self.call_listener(module, name, filename, line)
            return self.listener

        # TODO: ignore c_call etc...

        if event=='line':
            self.line_listener(module, name, filename, line, info, frame)

        return None

    def call_listener(self, module, name, filename, line):
        # print(f"A call encountered in {module}.{name}() at {filename}:{line}")
        pass

    def line_listener(self, module, name, filename, line, info, frame):
        code = info.code_context[0].strip()
        if code.startswith("sys.settrace(None)"):
            return
        self.linecount += 1
        p = tsensor.parsing.PyExprParser(code)
        t = p.parse()
        if t is not None:
            # print(f"A line encountered in {module}.{name}() at {filename}:{line}")
            # print("\t", code)
            # print("\t", repr(t))
            g = tsensor.viz.pyviz(code, frame)
            self.views.append(g)
            if self.savefig is not None:
                svgfilename = f"{self.savefig}-{self.linecount}.svg"
                g.savefig(svgfilename)
                g.filename = svgfilename
            else:
                if get_ipython() is None:
                    svgfilename = f"tsensor-{self.linecount}.svg"
                    g.savefig(svgfilename)
                    g.filename = svgfilename
                    plt.show()
                else:
                    svg = g.svg()
                    display(SVG(svg))
            plt.close()


class explain:
    def __init__(self, savefig=None):
        self.savefig = savefig

    def __enter__(self, format="svg"):
        # print("ON trace")
        self.tracer = TensorTracer(self.savefig,format=format)
        sys.settrace(self.tracer.listener)
        frame = sys._getframe()
        prev = frame.f_back # get block wrapped in "with"
        prev.f_trace = self.tracer.listener
        return self.tracer

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.settrace(None)
        # print("OFF trace")


def eval(statement:str, frame=None) -> (tsensor.ast.ParseTreeNode, object):
    """
    Parse statement and return ast. Evaluate ast in context of
    frame if available, which sets the value field of all ast nodes.
    Overall result is in root.value.
    """
    p = tsensor.parsing.PyExprParser(statement)
    root = p.parse()
    if frame is None: # use frame of caller
        frame = sys._getframe().f_back
    root.eval(frame)
    return root, root.value


def smallest_matrix_subexpr(t):
    """
    During visualization, we need to find the smallest expression
    that evaluates to a non-scalar. That corresponds to the deepest subtree
    that evaluates to a non-scalar. Because we do not have parent pointers,
    we cannot start at the leaves and walk upwards. Instead, set a Boolean
    in each node to indicate whether one of the descendents (but not itself)
    evaluates to a non-scalar.  Nodes in the tree that have matrix values and
    not matrix_below are the ones to visualize.

    This routine modifies the tree nodes to turn on matrix_below where appropriate.
    """
    nodes = []
    _smallest_matrix_subexpr(t, nodes)
    return nodes

def _smallest_matrix_subexpr(t, nodes) -> bool:
    if t is None: return False  # prevent buggy code from causing us to fail
    if len(t.kids)==0: # leaf node
        if _nonscalar(t.value):
            nodes.append(t)
        return _nonscalar(t.value)
    n_matrix_below = 0 # once this latches true, it's passed all the way up to the root
    for sub in t.kids:
        matrix_below = _smallest_matrix_subexpr(sub, nodes)
        n_matrix_below += matrix_below # how many descendents evaluated two non-scalar?
    # If current node is matrix and no descendents are, then this is smallest
    # sub expression that evaluates to a matrix; keep track
    if _nonscalar(t.value) and n_matrix_below==0:
        nodes.append(t)
    # Report to caller that this node or some descendent is a matrix
    return _nonscalar(t.value) or n_matrix_below>0


def _nonscalar(x):
    return tsensor.analysis._shape(x) is not None


def _shape(v):
    if hasattr(v, "shape"):
        if isinstance(v.shape, torch.Size):
            if len(v.shape)==0:
                return None
            return list(v.shape)
        return v.shape
    return None
