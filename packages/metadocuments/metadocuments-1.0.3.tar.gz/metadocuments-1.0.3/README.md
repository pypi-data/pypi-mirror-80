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

```
@MetaDocument
class SubObject:
    a = 2
    b = "c"

@Metadocument
class MyClass:
    a = 1
    b = SubObject()

>>> print(MyClass().to_json(indent=4))
{
    "a": 1,
    "b": {
        "a": 2,
        "b": "c"
    }
}
```  

### Example 2

```
@Metadocument
class MyClass:
    a = 1

class Child(MyClass):
    b = 2
    c = "c"

>>> print(Child().to_json(indent=4))
{
    "a": 1,
    "b": 2,
    "c": "c"
}
```  