# MIT License
#
# Copyright (c) 2020 Aki Mäkinen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

def Metadocument(cls):
    newclass = DocumentMetaclass(cls.__name__, cls.__bases__, dict(cls.__dict__))
    return newclass

class DocumentMetaclass(type):
    def __new__(cls, clsname, bases, clsdict):
        fields = []
        class_dict = dict(clsdict)
        new_class_dict = {**class_dict}
        for key, value in class_dict.items():
            if not str.startswith(key, "__") and not callable(value):
                new_class_dict[key] = value
                fields.append(key)

        new_class_dict["_fields"] = fields

        def to_dict(self):
            new_dict = {}
            for key in getattr(self, "_fields"):
                value = getattr(self, key)
                if type(value.__class__) is DocumentMetaclass:
                    new_dict[key] = value.to_dict()
                else:
                    new_dict[key] = value
            return new_dict

        def to_json(self, *args, **kwargs):
            dictionary = self.to_dict()
            import json
            return json.dumps(dictionary, *args, **kwargs)

        def to_yaml(self, *args, **kwargs):
            dictionary = self.to_dict()
            import yaml
            return yaml.dump(dictionary, *args, **kwargs)
        clsobj = super().__new__(cls, clsname, bases, new_class_dict)

        setattr(clsobj, to_dict.__name__, to_dict)
        setattr(clsobj, to_json.__name__, to_json)
        setattr(clsobj, to_yaml.__name__, to_yaml)

        return clsobj


@Metadocument
class FromKeywords(dict):
    def __init__(self, *args, **kwargs):
        fields = []
        for key, value in kwargs.items():
            fields.append(key)
            setattr(self, key, value)
        self._fields = fields
        dict.__init__(self, **kwargs)
