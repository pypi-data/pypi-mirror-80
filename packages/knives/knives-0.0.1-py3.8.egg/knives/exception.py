from typing import List


# recursive function, get exception chain from __cause__
def get_exception_chain(e: BaseException) -> List[BaseException]:
    return [e] if e.__cause__ is None else [e] + get_exception_chain(e.__cause__)


# return string like '[aaa] -> [bbb] -> [ccc]'
def format_exception_chain(e: BaseException):
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
    test()
