import ast
from collections import ChainMap
from inspect import getclosurevars, getsource
from textwrap import dedent
from typing import List


def list_explicit_exceptions(f):
    # Ref: https://stackoverflow.com/a/32560287/14292354
    def get_exceptions(func, ids=set()):
        '''
        import os

        class MyException(Exception):
            pass

        def g():
            raise Exception

        class A():
            def method():
                raise OSError
            
        def f(x):
            int()
            A.method()
            os.makedirs()
            g()
            raise MyException
            raise ValueError('argument')

        for e in get_exceptions(f):
            print(e)
        '''
        try:
            vars = ChainMap(*getclosurevars(func)[:3]) # type: ignore
            source = dedent(getsource(func))
        except TypeError:
            return

        class _visitor(ast.NodeTransformer):
            def __init__(self):
                self.nodes = []
                self.other = []

            def visit_Raise(self, n):
                self.nodes.append(n.exc)

            def visit_Expr(self, n):
                if not isinstance(n.value, ast.Call):
                    return
                c, ob = n.value.func, None
                if isinstance(c, ast.Attribute):
                    parts = []
                    while getattr(c, 'value', None):
                        parts.append(c.attr) # type: ignore
                        c = c.value # type: ignore
                    if c.id in vars: # type: ignore
                        ob = vars[c.id] # type: ignore
                        for name in reversed(parts):
                            ob = getattr(ob, name)
                elif isinstance(c, ast.Name):
                    if c.id in vars:
                        ob = vars[c.id]
                if ob is not None and id(ob) not in ids:
                    self.other.append(ob)
                    ids.add(id(ob))

        v = _visitor()
        v.visit(ast.parse(source))
        for n in v.nodes:
            if isinstance(n, (ast.Call, ast.Name)):
                name = n.id if isinstance(n, ast.Name) else n.func.id # type: ignore
                if name in vars:
                    yield vars[name]
        for o in v.other:
            yield from get_exceptions(o)

    print(f'List Explicit Exceptions: function {f.__name__}()')
    for e in get_exceptions(f):
        print(e)


# return string like '[aaa] -> [bbb] -> [ccc]'
def format_exception_chain(e: BaseException):
    # recursive function, get exception chain from __cause__
    def get_exception_chain(e: BaseException) -> List[BaseException]:
        return [e] if e.__cause__ is None else [e] + get_exception_chain(e.__cause__)

    return ''.join(f'[{exc}]' if i == 0 else f' -> [{exc}]' for i, exc in enumerate(reversed(get_exception_chain(e))))


def test():
    try:
        try:
            try:
                try:
                    raise Exception('aaa') from None
                except Exception as e:
                    raise Exception('bbb') from e
            except Exception as e:
                raise Exception('ccc') from e
        except Exception as e:
            raise Exception('ddd') from e
    except Exception as e:
        print(f'出错：{format_exception_chain(e)}')


if __name__ == '__main__':
    # test()
    # list_explicit_exceptions(test)
    # list_explicit_exceptions(format_exception_chain)
    source = dedent(getsource(test))
    print(source)
    source_ast = ast.parse(source)
    print(source_ast)
