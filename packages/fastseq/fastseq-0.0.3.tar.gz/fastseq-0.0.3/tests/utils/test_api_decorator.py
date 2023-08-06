# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Test the API decorators."""

from absl.testing import absltest, parameterized
from fastseq.utils.api_decorator import get_class, override_method, add_method, export_api, replace
from fastseq.utils.test_utils import TestCaseBase


class A:
    def name(self):
        return 'A'

def func_a():
    return 'a'

class Base:
    def name(self):
        return 'Base'

class Child(Base):
    pass

class APIDecoratorTest(TestCaseBase):
    """ Test the API decorators."""

    def disable_test_get_class(self):
        """Test `get_class`"""
        self.assertEqual(get_class(A.name), A)

        class B:
            def name(self):
                return 'B'
        # TODO: enable this case to work as expected.
        self.assertEqual(get_class(B.name), B)

    def test_override_method(self):
        """Test override_method() decorator."""

        @override_method(A.name)
        def name_c(self):
            return 'B'

        a = A()
        self.assertEqual(a.name(), 'B')

    def test_add_method(self):
        """Test add_method() decorator."""

        class A:
            def name(self):
                return 'A'

        @add_method(A)
        def area(self):
            return 1

        a = A()
        self.assertEqual(a.area(), 1)

    def test_export_api(self):
        """Test export_method() decorator."""
        # export a new api.
        @export_api("test.export.api", "B")
        class B:
            def name(self):
                return 'B'

        from test.export.api import B  # pylint: disable=import-error,import-outside-toplevel
        b = B()
        self.assertEqual(b.name(), 'B')

        # the export api already exists.
        @export_api("test.export.api", "B")
        class C:
            def name(self):
                return 'C'

        from test.export.api import B  # pylint: disable=import-error,import-outside-toplevel
        b = B()
        self.assertEqual(b.name(), 'C')

    def test_replace_class(self):
        """Test replace() decorator for class."""
        @replace(A)
        class B:
            def name(self):
                return 'test_replace_B'

        a = A()
        self.assertEqual(a.name(), 'test_replace_B')

    def test_replace_func(self):
        """Test replace() decorator for function."""
        @replace(func_a)
        def func_b():
            return 'b'

        self.assertEqual(func_a(), 'b')

    def test_replace_baseclass(self):
        """Test replace() decorator for the base class."""
        @replace(Base)
        class BaseV2(Base):
            def name(self):
                return 'BaseV2'

        child = Child()
        self.assertEqual(child.name(), 'BaseV2')


if __name__ == "__main__":
    absltest.main()
