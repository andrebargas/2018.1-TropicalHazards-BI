import pandas
import pymongo
import json
import os

from django.core.files.storage import default_storage

from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import permission_classes
from rest_framework import permissions


@permission_classes((permissions.AllowAny,))
class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    # authentication_classes = (JSONWebTokenAuthentication, )

    def post(self, request, format=None):
        file_obj = request.data['file']
        file_path = '/code/tmp/' + file_obj.name
        with default_storage.open(file_path, 'wb+') as dest:
            for chunk in file_obj.chunks():
                dest.write(chunk)

        dataframe = pandas.read_csv(file_path)
        json_data = json.loads(dataframe.to_json(orient="records"))

        mongo_client = pymongo.MongoClient('mongo', 27017)
        mongo_db = mongo_client['main_db']
        collection = mongo_db['collection_teste']

        collection.insert(json_data)

        # Remove temporary file
        os.remove(file_path)
        return Response(status=201)