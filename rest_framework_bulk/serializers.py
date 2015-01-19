# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.serializers import ListSerializer


class BulkSerializerMixin(object):
    def to_internal_value(self, data):
        ret = super(BulkSerializerMixin, self).to_internal_value(data)
        if isinstance(self.root, BulkListSerializer) and self.context['view'].action in ('partial_bulk_update', 'bulk_update'):
            id_attr = self.root.update_lookup_field
            id_field = self.fields[id_attr]
            id_value = id_field.get_value(data)
            ret[id_attr] = id_value
        return ret


class BulkListSerializer(ListSerializer):
    update_lookup_field = 'id'

    def create(self, validated_data):
        model_class = self.child.Meta.model
        instances = [model_class(**item) for item in validated_data]
        return model_class.objects.bulk_create(instances)

    def update(self, instance, validated_data):
        def _get_updated():
            for obj in instance:
                obj_id = getattr(obj, lookup_field)
                update = update_dict.get(obj_id)
                if update:
                    for attr, value in update.items():
                        setattr(obj, attr, value)
                    obj.save(update_fields=update.keys())
                    yield obj

        lookup_field = self.update_lookup_field
        update_dict = dict((item.pop(lookup_field), item) for item in validated_data)
        return list(_get_updated())
