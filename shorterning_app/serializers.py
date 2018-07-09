from rest_framework import serializers
from models import *
class url_mapSerializer(serializers.ModelSerializer):
	class Meta:
		model=url_map
		fields='__all__'#optional, name of fields to return as a list
