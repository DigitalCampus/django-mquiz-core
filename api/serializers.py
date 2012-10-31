from django.core.serializers import json
from django.utils import simplejson
from tastypie.serializers import Serializer

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
    
        if 'objects' in data:
            for o in data['objects']:
                if 'q' in o:
                    self.format_quiz(o)
            data['quizzes'] = data['objects']
            del data['objects']
        if 'q' in data:
            self.format_quiz(data)
        
        return simplejson.dumps(data, cls=json.DjangoJSONEncoder,
                sort_keys=True, ensure_ascii=False, indent=self.json_indent)
        
    def format_quiz(self, data):
        # rename fields
        data['qref'] = data['id']
        del data['id']
        data['quiztitle'] = data['title']
        del data['title']
        data['quizdescription'] = data['description']
        del data['description']
        data['lastupdate'] = data['lastupdated_date']
        del data['lastupdated_date']
        
        # remove intermediate quizquestion data
        for question in data['q']:
            del question['id']
            del question['order']
            for qkey, qvalue in question['question'].items():
                question[qkey] = qvalue
            del question['question']
            # add maxscore for question
            
        # add maxscore for quiz
        data['maxscore'] = 0
         
        return data  