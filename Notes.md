# FastAPI Learning Notes

## 1. Path vs. Query Parameters

- **Path Parameters**: Part of the actual URL path (e.g., `/greet/Sivanath`). Used for identifying specific resources.
- **Query Parameters**: Key-value pairs added after a `?` in the URL (e.g., `/greet?name=Sivanath`). Used for filtering, optional settings, or sorting.

---

## 2. Function Defaults (`=`) vs. Type Hints (`Optional`)

- **Default Value (`= "User"`)**: Handles **runtime behavior**. If a user does not pass a parameter, Python defaults to this value.
- **Type Hint (`Optional[str]`)**: Handles **type safety and documentation**. It is shorthand for `str | None`, telling type checkers and FastAPI that passing `None` (or JSON `null`) is allowed.
  - _Note: `Optional` does **not** make a parameter optional to omit in plain Python; you still need the `=` default value for that._

### Handling `None` Gracefully

When a parameter is `Optional` and a caller explicitly passes `None`, an f-string like `f"Hello, {name}"` will output `"Hello, None"`.
To handle this gracefully:

```python
display_name = name if name is not None else "Guest"
```
