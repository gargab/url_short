from django.shortcuts import render
from models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from serializers import *
from rest_framework.decorators import detail_route,list_route
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from rest_framework.viewsets import ModelViewSet
from utils import *

from datetime import datetime as dt


class urlMapView(ModelViewSet):

	queryset=url_map.objects.all()
	serializer_class=url_mapSerializer

	@detail_route(methods=['get'])
	def get_stats(self,request,pk=None):
		if url_map.objects.filter(short_url=str(pk)).exists():
			returned = url_map.objects.filter(short_url=str(pk)).latest('date_time_stamp')
			return Response({"visits":returned.visits})
		else:
			return Response(status=status.HTTP_404_NOT_FOUND)


	@detail_route(methods=['get'])
	def short_url(self,request,pk=None):
		allowed_user=request.GET.get('user',0)
		print allowed_user
		print pk
		if url_map.objects.filter(short_url=str(pk)).exists():
			returned = url_map.objects.filter(short_url=str(pk)).latest('date_time_stamp')
			current_datetime = dt.utcnow()
			diff = (current_datetime - returned.date_time_stamp.replace(tzinfo=None)).total_seconds()
			print diff
			if diff <= returned.expiry:
				if len(returned.allowed_users)>0:
					if str(allowed_user) in returned.allowed_users:
						returned.visits +=1
						returned.save()
						return HttpResponseRedirect(returned.url)
					else:
						return HttpResponseForbidden()
				else:
					returned.visits +=1
					returned.save()
					return HttpResponseRedirect(returned.url)
			else:

				return Response(status=status.HTTP_404_NOT_FOUND)

		return Response(status=status.HTTP_404_NOT_FOUND)

	@list_route(methods=['post'])
	def create_url(self,request):
		post_data=request.data
		url = post_data['url']
		id_ret = 0
		try:
			id_ret = url_map.objects.order_by('-id')[0].id
			print id_ret
		except Exception as  e:
			print e
			id_ret = 0
		id_ret+=1

		try:
			short_url = post_data['short_url']
		except:
			short_url = baseconvert(id_ret,BASE10,BASE62)
			post_data['short_url'] = short_url

		if post_data["allowed_users"]:
			users = post_data["allowed_users"].split(",")
			post_data['allowed_users']=users

		serialized_data=url_mapSerializer(data=post_data)
		base_url="http://localhost:8000/"
		if serialized_data.is_valid():
			serialized_data.save()
			return Response({'short_url':base_url + post_data['short_url']+"/short_url/"},status=status.HTTP_201_CREATED)
		else:
			print serialized_data.errors
			return Response(status=status.HTTP_400_BAD_REQUEST)
