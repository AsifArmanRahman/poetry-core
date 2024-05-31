from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from poetry.core.constraints.generic import AnyConstraint
from poetry.core.constraints.generic import Constraint
from poetry.core.constraints.generic import EmptyConstraint
from poetry.core.constraints.generic import MultiConstraint
from poetry.core.constraints.generic import UnionConstraint


if TYPE_CHECKING:
    from poetry.core.constraints.generic import BaseConstraint


@pytest.mark.parametrize(
    ("constraint1", "constraint2", "expected"),
    [
        (Constraint("win32"), Constraint("win32"), True),
        (Constraint("win32"), Constraint("linux"), False),
        (Constraint("win32", "!="), Constraint("win32"), False),
        (Constraint("win32", "!="), Constraint("linux"), True),
    ],
)
def test_allows(
    constraint1: Constraint, constraint2: Constraint, expected: bool
) -> None:
    assert constraint1.allows(constraint2) is expected


@pytest.mark.parametrize(
    ("constraint1", "constraint2", "expected_any", "expected_all"),
    [
        (Constraint("win32"), EmptyConstraint(), False, True),
        (Constraint("win32"), AnyConstraint(), True, False),
        (Constraint("win32"), Constraint("win32"), True, True),
        (Constraint("win32"), Constraint("linux"), False, False),
        (Constraint("win32"), Constraint("win32", "!="), False, False),
        (Constraint("win32"), Constraint("linux", "!="), True, False),
        (
            Constraint("win32"),
            UnionConstraint(Constraint("win32"), Constraint("linux")),
            True,
            False,
        ),
        (
            Constraint("win32"),
            UnionConstraint(Constraint("darwin"), Constraint("linux")),
            False,
            False,
        ),
        (
            Constraint("win32"),
            UnionConstraint(Constraint("win32", "!="), Constraint("linux", "!=")),
            True,
            False,
        ),
        (
            Constraint("win32"),
            UnionConstraint(Constraint("darwin", "!="), Constraint("linux", "!=")),
            True,
            False,
        ),
        (
            Constraint("win32"),
            MultiConstraint(Constraint("win32", "!="), Constraint("linux", "!=")),
            False,
            False,
        ),
        (
            Constraint("win32"),
            MultiConstraint(Constraint("darwin", "!="), Constraint("linux", "!=")),
            True,
            False,
        ),
        (Constraint("win32", "!="), EmptyConstraint(), False, True),
        (Constraint("win32", "!="), AnyConstraint(), True, False),
        (Constraint("win32", "!="), Constraint("win32"), False, False),
        (Constraint("win32", "!="), Constraint("linux"), True, True),
        (Constraint("win32", "!="), Constraint("win32", "!="), True, True),
        (Constraint("win32", "!="), Constraint("linux", "!="), True, False),
        (
            Constraint("win32", "!="),
            UnionConstraint(Constraint("win32"), Constraint("linux")),
            True,
            False,
        ),
        (
            Constraint("win32", "!="),
            UnionConstraint(Constraint("darwin"), Constraint("linux")),
            True,
            True,
        ),
        (
            Constraint("win32", "!="),
            UnionConstraint(Constraint("win32", "!="), Constraint("linux", "!=")),
            True,
            False,
        ),
        (
            Constraint("win32", "!="),
            UnionConstraint(Constraint("darwin", "!="), Constraint("linux", "!=")),
            True,
            False,
        ),
        (
            Constraint("win32", "!="),
            MultiConstraint(Constraint("win32", "!="), Constraint("linux", "!=")),
            True,
            True,
        ),
        (
            Constraint("win32", "!="),
            MultiConstraint(Constraint("darwin", "!="), Constraint("linux", "!=")),
            True,
            False,
        ),
    ],
)
def test_allows_any_and_allows_all(
    constraint1: Constraint,
    constraint2: BaseConstraint,
    expected_any: bool,
    expected_all: bool,
) -> None:
    assert constraint1.allows_any(constraint2) is expected_any
    assert constraint1.allows_all(constraint2) is expected_all


@pytest.mark.parametrize(
    ("constraint", "inverted"),
    [
        (EmptyConstraint(), AnyConstraint()),
        (Constraint("foo"), Constraint("foo", "!=")),
        (
            MultiConstraint(Constraint("foo", "!="), Constraint("bar", "!=")),
            UnionConstraint(Constraint("foo"), Constraint("bar")),
        ),
    ],
)
def test_invert(constraint: BaseConstraint, inverted: BaseConstraint) -> None:
    assert constraint.invert() == inverted
    assert inverted.invert() == constraint


@pytest.mark.parametrize(
    ("constraint1", "constraint2", "expected"),
    [
        (
            EmptyConstraint(),
            Constraint("win32"),
            EmptyConstraint(),
        ),
        (
            EmptyConstraint(),
            MultiConstraint(Constraint("darwin", "!="), Constraint("linux", "!=")),
            EmptyConstraint(),
        ),
        (
            EmptyConstraint(),
            UnionConstraint(Constraint("win32"), Constraint("linux")),
            EmptyConstraint(),
        ),
        (
            AnyConstraint(),
            Constraint("win32"),
            Constraint("win32"),
        ),
        (
            AnyConstraint(),
            MultiConstraint(Constraint("darwin", "!="), Constraint("linux", "!=")),
            MultiConstraint(Constraint("darwin", "!="), Constraint("linux", "!=")),
        ),
        (
            AnyConstraint(),
            UnionConstraint(Constraint("win32"), Constraint("linux")),
            UnionConstraint(Constraint("win32"), Constraint("linux")),
        ),
        (
            EmptyConstraint(),
            AnyConstraint(),
            EmptyConstraint(),
        ),
        (
            EmptyConstraint(),
            EmptyConstraint(),
            EmptyConstraint(),
        ),
        (
            AnyConstraint(),
            AnyConstraint(),
            AnyConstraint(),
        ),
        (
            Constraint("win32"),
            Constraint("win32"),
            Constraint("win32"),
        ),
        (
            Constraint("win32"),
            Constraint("linux"),
            EmptyConstraint(),
        ),
        (
            Constraint("win32"),
            MultiConstraint(Constraint("darwin", "!="), Constraint("linux", "!=")),
            Constraint("win32"),
        ),
        (
            Constraint("win32"),
            MultiConstraint(Constraint("win32", "!="), Constraint("linux", "!=")),
            EmptyConstraint(),
        ),
        (
            Constraint("win32"),
            UnionConstraint(Constraint("win32"), Constraint("linux")),
            Constraint("win32"),
        ),
        (
            Constraint("win32"),
            UnionConstraint(Constraint("linux"), Constraint("linux2")),
            EmptyConstraint(),
        ),
        (
            Constraint("win32"),
            Constraint("linux", "!="),
            Constraint("win32"),
        ),
        (
            Constraint("win32", "!="),
            Constraint("linux"),
            Constraint("linux"),
        ),
        (
            Constraint("win32", "!="),
            Constraint("linux", "!="),
            (
                MultiConstraint(Constraint("win32", "!="), Constraint("linux", "!=")),
                MultiConstraint(Constraint("linux", "!="), Constraint("win32", "!=")),
            ),
        ),
        (
            Constraint("win32", "!="),
            MultiConstraint(Constraint("win32", "!="), Constraint("linux", "!=")),
            MultiConstraint(Constraint("win32", "!="), Constraint("linux", "!=")),
        ),
        (
            Constraint("darwin", "!="),
            MultiConstraint(Constraint("win32", "!="), Constraint("linux", "!=")),
            MultiConstraint(
                Constraint("win32", "!="),
                Constraint("linux", "!="),
                Constraint("darwin", "!="),
            ),
        ),
        (
            Constraint("win32", "!="),
            UnionConstraint(Constraint("win32"), Constraint("linux")),
            Constraint("linux"),
        ),
        (
            Constraint("win32", "!="),
            UnionConstraint(
                Constraint("win32"), Constraint("linux"), Constraint("darwin")
            ),
            UnionConstraint(Constraint("linux"), Constraint("darwin")),
        ),
        (
            Constraint("win32", "!="),
            UnionConstraint(Constraint("linux"), Constraint("linux2")),
            UnionConstraint(Constraint("linux"), Constraint("linux2")),
        ),
        (
            UnionConstraint(Constraint("win32"), Constraint("linux")),
            UnionConstraint(Constraint("win32"), Constraint("darwin")),
            Constraint("win32"),
        ),
        (
            UnionConstraint(
                Constraint("win32"), Constraint("linux"), Constraint("darwin")
            ),
            UnionConstraint(
                Constraint("win32"), Constraint("cygwin"), Constraint("darwin")
            ),
            UnionConstraint(
                Constraint("win32"),
                Constraint("darwin"),
            ),
        ),
        (
            UnionConstraint(Constraint("win32"), Constraint("linux")),
            MultiConstraint(Constraint("win32", "!="), Constraint("darwin", "!=")),
            Constraint("linux"),
        ),
        (
            UnionConstraint(Constraint("win32"), Constraint("linux")),
            MultiConstraint(Constraint("win32", "!="), Constraint("linux", "!=")),
            EmptyConstraint(),
        ),
        (
            MultiConstraint(Constraint("win32", "!="), Constraint("linux", "!=")),
            MultiConstraint(Constraint("win32", "!="), Constraint("darwin", "!=")),
            (
                MultiConstraint(
                    Constraint("win32", "!="),
                    Constraint("linux", "!="),
                    Constraint("darwin", "!="),
                ),
                MultiConstraint(
                    Constraint("win32", "!="),
                    Constraint("darwin", "!="),
                    Constraint("linux", "!="),
                ),
            ),
        ),
    ],
)
def test_intersect(
    constraint1: BaseConstraint,
    constraint2: BaseConstraint,
    expected: BaseConstraint | tuple[BaseConstraint, BaseConstraint],
) -> None:
    if not isinstance(expected, tuple):
        expected = (expected, expected)
    assert constraint1.intersect(constraint2) == expected[0]
    assert constraint2.intersect(constraint1) == expected[1]


@pytest.mark.parametrize(
    ("constraint1", "constraint2", "expected"),
    [
        (
            EmptyConstraint(),
            Constraint("win32"),
            Constraint("win32"),
        ),
        (
            EmptyConstraint(),
            MultiConstraint(Constraint("darwin", "!="), Constraint("linux", "!=")),
            MultiConstraint(Constraint("darwin", "!="), Constraint("linux", "!=")),
        ),
        (
            EmptyConstraint(),
            UnionConstraint(Constraint("win32"), Constraint("linux")),
            UnionConstraint(Constraint("win32"), Constraint("linux")),
        ),
        (
            AnyConstraint(),
            Constraint("win32"),
            AnyConstraint(),
        ),
        (
            AnyConstraint(),
            MultiConstraint(Constraint("darwin", "!="), Constraint("linux", "!=")),
            AnyConstraint(),
        ),
        (
            AnyConstraint(),
            UnionConstraint(Constraint("win32"), Constraint("linux")),
            AnyConstraint(),
        ),
        (
            EmptyConstraint(),
            AnyConstraint(),
            AnyConstraint(),
        ),
        (
            EmptyConstraint(),
            EmptyConstraint(),
            EmptyConstraint(),
        ),
        (
            AnyConstraint(),
            AnyConstraint(),
            AnyConstraint(),
        ),
        (
            Constraint("win32"),
            Constraint("win32"),
            Constraint("win32"),
        ),
        (
            Constraint("win32"),
            Constraint("linux"),
            (
                UnionConstraint(Constraint("win32"), Constraint("linux")),
                UnionConstraint(Constraint("linux"), Constraint("win32")),
            ),
        ),
        (
            Constraint("win32"),
            MultiConstraint(Constraint("darwin", "!="), Constraint("linux", "!=")),
            MultiConstraint(Constraint("darwin", "!="), Constraint("linux", "!=")),
        ),
        (
            Constraint("win32"),
            MultiConstraint(Constraint("win32", "!="), Constraint("linux", "!=")),
            Constraint("linux", "!="),
        ),
        (
            Constraint("win32"),
            MultiConstraint(
                Constraint("win32", "!="),
                Constraint("linux", "!="),
                Constraint("darwin", "!="),
            ),
            MultiConstraint(Constraint("linux", "!="), Constraint("darwin", "!=")),
        ),
        (
            Constraint("win32"),
            UnionConstraint(Constraint("win32"), Constraint("linux")),
            UnionConstraint(Constraint("win32"), Constraint("linux")),
        ),
        (
            Constraint("win32"),
            UnionConstraint(Constraint("linux"), Constraint("linux2")),
            (
                UnionConstraint(
                    Constraint("win32"), Constraint("linux"), Constraint("linux2")
                ),
                UnionConstraint(
                    Constraint("linux"), Constraint("linux2"), Constraint("win32")
                ),
            ),
        ),
        (
            Constraint("win32"),
            Constraint("linux", "!="),
            Constraint("linux", "!="),
        ),
        (
            Constraint("win32", "!="),
            Constraint("linux"),
            Constraint("win32", "!="),
        ),
        (
            Constraint("win32", "!="),
            Constraint("linux", "!="),
            AnyConstraint(),
        ),
        (
            Constraint("win32", "!="),
            MultiConstraint(Constraint("win32", "!="), Constraint("linux", "!=")),
            Constraint("win32", "!="),
        ),
        (
            Constraint("darwin", "!="),
            MultiConstraint(Constraint("win32", "!="), Constraint("linux", "!=")),
            AnyConstraint(),
        ),
        (
            Constraint("win32", "!="),
            UnionConstraint(Constraint("win32"), Constraint("linux")),
            AnyConstraint(),
        ),
        (
            Constraint("win32", "!="),
            UnionConstraint(Constraint("linux"), Constraint("linux2")),
            Constraint("win32", "!="),
        ),
        (
            UnionConstraint(Constraint("win32"), Constraint("linux")),
            UnionConstraint(Constraint("win32"), Constraint("darwin")),
            (
                UnionConstraint(
                    Constraint("win32"), Constraint("linux"), Constraint("darwin")
                ),
                UnionConstraint(
                    Constraint("win32"), Constraint("darwin"), Constraint("linux")
                ),
            ),
        ),
        (
            UnionConstraint(
                Constraint("win32"), Constraint("linux"), Constraint("darwin")
            ),
            UnionConstraint(
                Constraint("win32"), Constraint("cygwin"), Constraint("darwin")
            ),
            (
                UnionConstraint(
                    Constraint("win32"),
                    Constraint("linux"),
                    Constraint("darwin"),
                    Constraint("cygwin"),
                ),
                UnionConstraint(
                    Constraint("win32"),
                    Constraint("cygwin"),
                    Constraint("darwin"),
                    Constraint("linux"),
                ),
            ),
        ),
        (
            UnionConstraint(Constraint("win32"), Constraint("linux")),
            MultiConstraint(Constraint("win32", "!="), Constraint("darwin", "!=")),
            UnionConstraint(
                Constraint("win32"),
                Constraint("linux"),
                MultiConstraint(Constraint("win32", "!="), Constraint("darwin", "!=")),
            ),
        ),
        (
            UnionConstraint(Constraint("win32"), Constraint("linux")),
            MultiConstraint(Constraint("win32", "!="), Constraint("linux", "!=")),
            UnionConstraint(
                Constraint("win32"),
                Constraint("linux"),
                MultiConstraint(Constraint("win32", "!="), Constraint("linux", "!=")),
            ),
        ),
        (
            MultiConstraint(Constraint("win32", "!="), Constraint("linux", "!=")),
            MultiConstraint(Constraint("win32", "!="), Constraint("darwin", "!=")),
            MultiConstraint(Constraint("win32", "!=")),
        ),
    ],
)
def test_union(
    constraint1: BaseConstraint,
    constraint2: BaseConstraint,
    expected: BaseConstraint | tuple[BaseConstraint, BaseConstraint],
) -> None:
    if not isinstance(expected, tuple):
        expected = (expected, expected)
    assert constraint1.union(constraint2) == expected[0]
    assert constraint2.union(constraint1) == expected[1]


def test_difference() -> None:
    c = Constraint("win32")

    assert c.difference(Constraint("win32")).is_empty()
    assert c.difference(Constraint("linux")) == c


@pytest.mark.parametrize(
    "constraint",
    [
        EmptyConstraint(),
        AnyConstraint(),
        Constraint("win32"),
        UnionConstraint(Constraint("win32"), Constraint("linux")),
        MultiConstraint(Constraint("win32", "!="), Constraint("linux", "!=")),
    ],
)
def test_constraints_are_hashable(constraint: BaseConstraint) -> None:
    # We're just testing that constraints are hashable, there's nothing much to say
    # about the result.
    hash(constraint)
