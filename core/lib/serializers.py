from rest_framework.serializers import ModelSerializer


def make_serializer_class(model_, *fields_):
    if not fields_:
        fields_ = "__all__"
    else:
        fields_ = ["id", *fields_]

    class _Serializer(ModelSerializer):
        class Meta:
            model = model_
            fields = fields_

    _Serializer.__name__ = f"{model_.__name__}Serializer"
    return _Serializer


def make_info_serializer(model_, source, *fields_):
    class _Serializer(ModelSerializer):
        class Meta:
            model = model_
            fields = ["id", *fields_]

    _Serializer.__name__ = f"{model_.__name__}InfoSerializer"
    return _Serializer(read_only=True, source=source)
