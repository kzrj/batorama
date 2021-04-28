# -*- coding: utf-8 -*-
from rest_framework import serializers


class AnnotateFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(AnnotateFieldsModelSerializer, self).__init__(*args, **kwargs)
        if len(args) > 0 and len(args[0]) > 0:
            for field_name in args[0][0].__dict__.keys():
                if field_name[0] == '_' or field_name in self.fields.keys() \
                   or field_name == 'modified_at' :
                    continue
                self.fields[field_name] = serializers.ReadOnlyField()