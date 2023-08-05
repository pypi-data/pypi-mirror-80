def Metadocument(cls):
    newclass = DocumentMetaclass(cls.__name__, cls.__bases__, dict(cls.__dict__))
    return newclass

class DocumentMetaclass(type):
    def __new__(cls, clsname, bases, clsdict):
        fields = []
        class_dicts = [clsdict] + [b.__dict__ for b in bases]
        new_class_dict = {}
        for c in class_dicts:
            for key, value in c.items():
                if not str.startswith(key, "__") and not callable(value):
                    new_class_dict[key] = value
                    fields.append(key)
        new_class_dict["__fields"] = fields
        # setattr(clsobj, "__fields", fields)

        def to_dict(self):
            new_dict = {}
            for key in getattr(self, "__fields"):
                value = getattr(self, key)
                if type(value.__class__) is DocumentMetaclass:
                    new_dict[key] = value.to_dict()
                else:
                    new_dict[key] = value
            return new_dict
        new_class_dict["to_dict"] = to_dict
        # setattr(clsobj, to_dict.__name__, to_dict)

        def to_json(self, *args, **kwargs):
            dictionary = self.to_dict()
            import json
            return json.dumps(dictionary, *args, **kwargs)
        # setattr(clsobj, to_json.__name__, to_json)
        new_class_dict["to_json"] = to_json

        def to_yaml(self, *args, **kwargs):
            dictionary = self.to_dict()
            import yaml
            return yaml.dump(dictionary, *args, **kwargs)
        # setattr(clsobj, to_yaml.__name__, to_yaml)
        new_class_dict["to_yaml"] = to_yaml

        clsobj = super(DocumentMetaclass, cls).__new__(cls, clsname, bases, new_class_dict)

        return clsobj

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
