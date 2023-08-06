import unittest
from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic, Optional, List

from pedantic import overrides, pedantic
from pedantic.class_decorators import pedantic_class
from pedantic.basic_helpers import TYPE_VAR_METHOD_NAME


class TestPedanticClass(unittest.TestCase):
    def test_constructor(self):
        @pedantic_class
        class MyClass:
            def __init__(self, a: int) -> None:
                self.a = a

        MyClass(a=42)

    def test_constructor_param_without_type_hint(self):
        @pedantic_class
        class MyClass:
            def __init__(self, a) -> None:
                self.a = a

        with self.assertRaises(expected_exception=AssertionError):
            MyClass(a=42)

    def test_constructor_without_return_type(self):
        @pedantic_class
        class MyClass:
            def __init__(self, a: int):
                self.a = a

        with self.assertRaises(expected_exception=AssertionError):
            MyClass(a=42)

    def test_constructor_wrong_return_type(self):
        @pedantic_class
        class MyClass:
            def __init__(self, a: int) -> int:
                self.a = a

        with self.assertRaises(expected_exception=AssertionError):
            MyClass(a=42)

    def test_constructor_must_be_called_with_kwargs(self):
        @pedantic_class
        class MyClass:
            def __init__(self, a: int) -> None:
                self.a = a

        with self.assertRaises(expected_exception=AssertionError):
            MyClass(42)

    def test_multiple_methods(self):
        @pedantic_class
        class MyClass:
            def __init__(self, a: int) -> None:
                self.a = a

            def calc(self, b: int) -> int:
                return self.a - b

            def print(self, s: str) -> None:
                print(f'{self.a} and {s}')

        m = MyClass(a=5)
        m.calc(b=42)
        m.print(s='Hi')
        with self.assertRaises(expected_exception=AssertionError):
            m.calc(45)
        with self.assertRaises(expected_exception=AssertionError):
            m.calc(b=45.0)
        with self.assertRaises(expected_exception=AssertionError):
            m.print('Hi')

    def test_multiple_methods_with_missing_and_wrong_type_hints(self):
        @pedantic_class
        class MyClass:
            def __init__(self, a: int) -> None:
                self.a = a

            def calc(self, b: int) -> float:
                return self.a - b

            def dream(self, b) -> int:
                return self.a * b

            def print(self, s: str):
                print(f'{self.a} and {s}')

        m = MyClass(a=5)
        with self.assertRaises(expected_exception=AssertionError):
            m.calc(b=42)
        with self.assertRaises(expected_exception=AssertionError):
            m.print(s='Hi')
        with self.assertRaises(expected_exception=AssertionError):
            m.dream(b=2)

    def test_type_annotation_string(self):
        @pedantic_class
        class MyClass:
            def __init__(self, s: str) -> None:
                self.s = s

            @staticmethod
            def generator() -> 'MyClass':
                return MyClass(s='generated')

        MyClass.generator()

    def test_typo_in_type_annotation_string(self):
        @pedantic_class
        class MyClass:
            def __init__(self, s: str) -> None:
                self.s = s

            @staticmethod
            def generator() -> 'MyClas':
                return MyClass(s='generated')

        with self.assertRaises(expected_exception=AssertionError):
            MyClass.generator()

    def test_overriding_contains(self):
        @pedantic_class
        class MyClass(list):
            def __contains__(self, item: int) -> bool:
                return True

        m = MyClass()
        print(42 in m)
        with self.assertRaises(expected_exception=AssertionError):
            print('something' in m)

    def test_type_annotation_string_typo(self):
        @pedantic_class
        class MyClass:
            def compare(self, other: 'MyClas') -> bool:
                return self == other

            def fixed_compare(self, other: 'MyClass') -> bool:
                return self == other

        m = MyClass()
        m.fixed_compare(other=m)
        with self.assertRaises(expected_exception=AssertionError):
            m.compare(other=m)

    def test_docstring_not_required(self):
        @pedantic_class
        class Foo:
            def __init__(self, a: int) -> None:
                self.a = a

            def bunk(self) -> int:
                '''
                Function with correct docstring. Yes, single-quoted docstrings are allowed too.
                Returns:
                    int: 42
                '''
                return self.a

        foo = Foo(a=10)
        foo.bunk()

    def test_overrides(self):
        @pedantic_class
        class Abstract:
            def func(self, b: str) -> str:
                pass

            def bunk(self) -> int:
                pass

        @pedantic_class
        class Foo(Abstract):
            def __init__(self, a: int) -> None:
                self.a = a

            @overrides(Abstract)
            def func(self, b: str) -> str:
                return b

            @overrides(Abstract)
            def bunk(self) -> int:
                return 42

        f = Foo(a=42)
        f.func(b='Hi')
        f.bunk()

    def test_overrides_abc(self):
        @pedantic_class
        class Abstract(ABC):
            @abstractmethod
            def func(self, b: str) -> str:
                pass

            @abstractmethod
            def bunk(self) -> int:
                pass

        @pedantic_class
        class Foo(Abstract):
            def __init__(self, a: int) -> None:
                self.a = a

            @overrides(Abstract)
            def func(self, b: str) -> str:
                return b

            @overrides(Abstract)
            def bunk(self) -> int:
                return 42

        f = Foo(a=42)
        f.func(b='Hi')
        f.bunk()

    def test_overrides_with_type_errors_and_call_by_args3(self):
        @pedantic_class
        class Abstract:
            def func(self, b: str) -> str:
                pass

            def bunk(self) -> int:
                pass

        @pedantic_class
        class Foo(Abstract):
            def __init__(self, a: int) -> None:
                self.a = a

            @overrides(Abstract)
            def func(self, b: str) -> str:
                return b

            @overrides(Abstract)
            def bunk(self) -> int:
                return self.a

        f = Foo(a=42)
        f.func(b='Hi')
        f.bunk()
        with self.assertRaises(expected_exception=AssertionError):
            f.func('Hi')
        with self.assertRaises(expected_exception=AssertionError):
            Foo(a=3.1415)
        f.a = 3.145
        with self.assertRaises(expected_exception=AssertionError):
            f.bunk()

    def test_overrides_goes_wrong(self):
        @pedantic_class
        class Parent:
            def func(self, b: str) -> str:
                return b + b + b

            def bunk(self) -> int:
                return 42

        with self.assertRaises(expected_exception=AssertionError):
            @pedantic_class
            class Foo(Parent):
                def __init__(self, a: int) -> None:
                    self.a = a

                @overrides(Parent)
                def funcy(self, b: str) -> str:
                    return b

                @overrides(Parent)
                def bunk(self) -> int:
                    return self.a

            f = Foo(a=40002)
            f.func(b='Hi')
            f.bunk()

        p = Parent()
        p.func(b='Hi')
        p.bunk()

    def test_static_method_with_sloppy_type_annotation(self):
        @pedantic_class
        class MyStaticClass:
            @staticmethod
            def double_func(a: int) -> int:
                x, y = MyStaticClass.static_bar()
                return x

            @staticmethod
            def static_bar() -> (int, int):  # this is wrong. Correct would be Tuple[int, int]
                return 0, 1

        with self.assertRaises(expected_exception=AssertionError):
            print(MyStaticClass.double_func(a=0))

    def test_property(self):
        @pedantic_class
        class MyClass(object):
            def __init__(self, some_arg: Any) -> None:
                self._some_attribute = some_arg

            @property
            def some_attribute(self) -> int:
                return self._some_attribute

            @some_attribute.setter
            def some_attribute(self, value: str) -> None:
                self._some_attribute = value

            def calc(self, value: float) -> float:
                return 2 * value

        with self.assertRaises(expected_exception=AssertionError):
            MyClass(42)

        m = MyClass(some_arg=42)
        self.assertEqual(m.some_attribute, 42)
        with self.assertRaises(expected_exception=AssertionError):
            m.some_attribute = 100
        self.assertEqual(m.some_attribute, 42)
        m.some_attribute = '100'
        self.assertEqual(m._some_attribute, '100')
        m.calc(value=42.0)
        with self.assertRaises(expected_exception=AssertionError):
            print(m.some_attribute)

    def test_property_getter_and_setter_misses_type_hints(self):
        @pedantic_class
        class MyClass(object):
            def __init__(self, some_arg: int) -> None:
                self._some_attribute = some_arg

            @property
            def some_attribute(self):
                return self._some_attribute

            @some_attribute.setter
            def some_attribute(self, value: int):
                self._some_attribute = value

            def calc(self, value: float) -> float:
                return 2 * value

        with self.assertRaises(expected_exception=AssertionError):
            MyClass(42)

        m = MyClass(some_arg=42)
        with self.assertRaises(expected_exception=AssertionError):
            m.some_attribute = 100

        with self.assertRaises(expected_exception=AssertionError):
            print(m.some_attribute)
        m.calc(value=42.0)
        with self.assertRaises(expected_exception=AssertionError):
            m.calc(value=42)

    def test_pedantic_generic_class(self):
        T = TypeVar('T')

        @pedantic_class
        class LoggedVar(Generic[T]):
            def __init__(self, value: T, name: str, logger: Any) -> None:
                self.name = name
                self.logger = logger
                self.value = value

            def set(self, new: T) -> None:
                self.log(message='Set ' + repr(self.value))
                self.value = new

            def get(self) -> T:
                self.log(message='Get ' + repr(self.value))
                return self.value

            def log(self, message: str) -> None:
                self.logger = self.name + message

        o = LoggedVar(value=42, name='hi', logger='test')
        o.set(new=57)
        self.assertTrue(isinstance(o.get(), int))

        with self.assertRaises(expected_exception=AssertionError):
            o.set(new=3.14)

    def test_stack(self):
        T = TypeVar('T')

        @pedantic_class
        class Stack(Generic[T]):
            def __init__(self) -> None:
                self.items: List[T] = []

            def push(self, item: T) -> None:
                self.items.append(item)

            def pop(self) -> T:
                return self.items.pop()

            def empty(self) -> bool:
                return not self.items

            def top(self) -> Optional[T]:
                if len(self.items) > 0:
                    return self.items[len(self.items) - 1]
                else:
                    return None

        my_stack = Stack()
        get_type_vars = getattr(my_stack, TYPE_VAR_METHOD_NAME)
        self.assertEqual(get_type_vars(), {})
        with self.assertRaises(expected_exception=IndexError):
            my_stack.pop()
        self.assertIsNone(my_stack.top())
        self.assertIsNone(my_stack.top())
        self.assertFalse(T in get_type_vars())
        my_stack.push(item='hi')
        self.assertTrue(T in get_type_vars())
        my_stack.push(item='world')
        self.assertTrue(T in get_type_vars())
        self.assertTrue(len(get_type_vars()), 1)
        self.assertEqual(my_stack.pop(), 'world')
        self.assertEqual(my_stack.pop(), 'hi')
        self.assertIsNone(my_stack.top())
        with self.assertRaises(expected_exception=AssertionError):
            my_stack.push(item=42)

        my_other_stack = Stack()
        get_type_vars = getattr(my_other_stack, TYPE_VAR_METHOD_NAME)
        self.assertEqual(get_type_vars(), {})
        with self.assertRaises(expected_exception=IndexError):
            my_other_stack.pop()
        self.assertIsNone(my_other_stack.top())
        self.assertIsNone(my_other_stack.top())
        my_other_stack.push(item=100)
        self.assertTrue(len(get_type_vars()), 1)
        my_other_stack.push(item=142)
        self.assertTrue(len(get_type_vars()), 1)
        self.assertEqual(my_other_stack.pop(), 142)
        self.assertEqual(my_other_stack.pop(), 100)
        self.assertIsNone(my_other_stack.top())
        with self.assertRaises(expected_exception=AssertionError):
            my_other_stack.push(item='42')

    def test_double_pedantic(self):
        @pedantic_class
        class MyClass:
            @pedantic
            def __init__(self, a: int) -> None:
                self.a = a

        MyClass(a=42)
        with self.assertRaises(expected_exception=AssertionError):
            MyClass(42)
        with self.assertRaises(expected_exception=AssertionError):
            MyClass(a=42.0)

    def test_default_constructor(self):
        @pedantic_class
        class MyClass:
            def fun(self) -> int:
                return 42
        m = MyClass()
        m.fun()


if __name__ == '__main__':
    t = TestPedanticClass()
    t.test_stack()
