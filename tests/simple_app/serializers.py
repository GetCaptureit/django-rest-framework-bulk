# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from . import models


class SimpleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SimpleModel
