# -*- encoding:utf8 -*-
from core.models import CutBatchOP,BatchVersion,Page
from rest_framework import serializers

class CutBatchOPSerializer(serializers.ModelSerializer):
    class Meta:
        model = CutBatchOP
        fields = ['id','page', 'cut_data']
        class Meta:
            depth = 1

class PageSerializer(serializers.ModelSerializer):
    c_page = serializers.StringRelatedField(many=True)
    class Meta:
        model = Page
        fields = ['id', 'batch_version', 'image_name', 'c_page', 'get_page_url']

class PageNSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['id', 'batch_version', 'image_name', 'get_page_url']


class BatchVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchVersion
        fields = ['id', 'des', 'organiztion', 'submit_date', 'accepted']