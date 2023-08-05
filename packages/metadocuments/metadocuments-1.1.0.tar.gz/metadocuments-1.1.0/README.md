# MetaDocuments

## Installation

`pip install metadocuments`

## Usage

Decorate the document with `@Metadocument` to specify that it (and all its children) should be treated
as a metadocument. This adds functions `to_dict`, `to_json`  and `to_yaml` to the class instance which
then can be called to create a corresponding structure. Classes can contain methods, but those are ignored
unless they are decorated with `@property`. Inheritance and multiple inheritance do work, the `@Metadocument`
decorator is only required for the parent class.

### Example

```python
@MetaDocument
class SubObject:
    a = 2
    b = "c"

@Metadocument
class MyClass:
    a = 1
    b = SubObject()

print(MyClass().to_json(indent=4))
# {
#     "a": 1,
#     "b": {
#         "a": 2,
#         "b": "c"
#     }
# }
```  

### Example 2

```python
@Metadocument
class MyClass:
    a = 1

class Child(MyClass):
    b = 2
    c = "c"

print(Child().to_json(indent=4))
# {
#     "a": 1,
#     "b": 2,
#     "c": "c"
# }
```  

### Example 3

Using `FromKeywords` helper class. This can be helpful when there are structures that one does not want
to define as class. All the keywords are mapped 1:1 to a attribute / key.

```python
if __name__ == "__main__":
    @Metadocument
    class Foobar():
        a = 1
        b = 2
        c = FromKeywords(
            d="a",
            e="b",
            f=FromKeywords(
                g=1,
                asd=FromKeywords(
                    a = "b"
                )
            )
        )
    print(Foobar().to_json(indent=4))
```

## Limitations

Because of Python syntax abuse, there is no support for numeric keys unfortunately. If those are necessity, then
old-school dicts are best option (for now).

`FromKeywords` does inherit `dict` so it is possible to use it inside a dictionary which then can be serialized to JSON.

```python
if __name__ == "__main__":
    @Metadocument
    class Foobar:
        a = 1
        b = 2
        c = FromKeywords(
            d="a",
            e="b",
            f=FromKeywords(
                g=1,
                asd=FromKeywords(
                    a = "b"
                )
            )
        )

    some_dict = {
        "foo": "bar",
        1: "asd",
        "afgg": FromKeywords(
            a=1, b=2
        ),
        "ccc": Foobar().to_dict()
    }
    print(Foobar().to_json(indent=4))
    print(json.dumps(some_dict))
```
