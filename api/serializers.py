from django.core.serializers import json
from django.utils import simplejson
from tastypie.serializers import Serializer
import time

class PrettyJSONSerializer(Serializer):
    json_indent = 2

    def to_json(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
        return simplejson.dumps(data, cls=json.DjangoJSONEncoder,
                sort_keys=True, ensure_ascii=False, indent=self.json_indent)
        
        
class QuizJSONSerializer(Serializer):
    json_indent = 2

    def to_json(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
        for question in data['q']:
            del question['id']
            del question['order']
            for qkey, qvalue in question['question'].items():
                question[qkey] = qvalue
            del question['question']
        return simplejson.dumps(data, cls=json.DjangoJSONEncoder,
                sort_keys=True, ensure_ascii=False, indent=self.json_indent)