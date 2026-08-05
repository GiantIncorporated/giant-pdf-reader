# How to Determine What Scenarios to Test

A practical checklist for deciding what test cases actually matter, rather than
guessing or testing arbitrarily. The core skill of testing is choosing the
right *scenarios* — syntax is secondary.

## 1. Start with the Contract, Not the Implementation

Ask: **"What is this function/method promising to do?"** Test that promise,
not the internal steps used to fulfill it.

> Example: `Rectangle.area()`'s contract is "returns length × width." It
> doesn't matter how the code computes that internally — only that the output
> matches the contract for representative inputs.

## 2. Happy Path First

Cover the obvious, expected-use case before hunting for edge cases. This
confirms the basic logic works and documents *intent* — a reader should
understand what the code is for just from this test.

> Example: `Circle(5).area()` should return roughly `78.5`.

## 3. Boundary and Edge Values

For any numeric input, ask **"what happens at the extremes?"**

- **Zero** — `Circle(0)`, `Rectangle(0, 5)`. Does it break, or return a
  sensible zero?
- **Negative numbers** — a negative radius or width is physically
  nonsensical. Does the code guard against it, or silently return a negative
  result? If there's no guard, that's a gap worth documenting with a test
  even if you don't fix it right away.
- **Very large/small numbers** — floating-point precision issues tend to
  hide here.
- **Equal values** — e.g. a square (`Rectangle(5, 5)`) is a special case of
  the general rectangle case, worth checking it doesn't hit an unexpected
  code path.

## 4. Type and Equality Semantics

Whenever a class defines `__eq__`, `__lt__`, `__hash__`, etc., ask **"what
happens when compared to something it wasn't designed for?"**

> Example: a naive `__eq__` implementation might throw an `AttributeError`
> instead of returning `False` if it assumes `other` has the same
> attributes. Test comparisons against unrelated types, `None`, and sibling
> classes.

## 5. State Mutation vs. Purity

Does calling the method twice give the same answer? Does calling one method
change the result of another? This matters less for read-only/immutable
classes, but becomes a primary test category for anything with setters or
mutable state.

## 6. Polymorphism / Interface Conformance

If multiple classes share a base class, ask **"does every subclass honor the
base class's promises?"** Loop over instances of each subclass and check they
all implement the shared interface sensibly. This protects against future
subclasses that forget to override a required method.

## 7. "What Would a Bug Actually Look Like Here?"

The most practical filter of all. For each method, imagine someone
fat-fingers the code — swaps `+` for `*`, drops an exponent, forgets a
multiplier. Would the existing tests catch it?

- Prefer **parametrized tests** with a few different input values over a
  single hardcoded case — one hardcoded case can accidentally still pass
  even with a subtly wrong formula.

## 8. Domain-Specific Precision/Comparison Quirks

Know when equality checks themselves need adjusting for the data type
involved.

> Example: floating-point results (like anything involving `math.pi`) need
> `pytest.approx()` instead of `==`, while exact integer arithmetic doesn't.

---

## Quick Reference

A rough shorthand for scenario coverage:

**Valid → Invalid → Boundary → Edge-case-of-the-type-system**

If at least one test exists in each bucket, you've covered the categories
that catch the vast majority of real bugs. Anything beyond that is
diminishing returns unless the code is safety-critical.