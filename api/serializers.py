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
    json_indent = 4

    def to_json(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
    
        if 'objects' in data:
            for o in data['objects']:
                if 'q' in o:
                    self.format_quiz(o)
            data['quizzes'] = data['objects']
            del data['objects']
        if 'questions' in data:
            self.format_quiz(data)
        
        return simplejson.dumps(data, cls=json.DjangoJSONEncoder,
                sort_keys=True, ensure_ascii=False, indent=self.json_indent)
        
    def format_quiz(self, data):
        
        qmaxscore = 0.0
        # remove intermediate quizquestion data
        for question in data['questions']:
            if 'props' in question['question']:
                question['question']['p'] = {}
                for p in question['question']['props']:
                    try:
                        question['question']['p'][p['name']] = float(p['value'])
                    except:
                        question['question']['p'][p['name']] = p['value']
                question['question']['props'] = question['question']['p']
                del question['question']['p']
                try:
                    float(question['question']['props']['maxscore'])
                    qmaxscore = qmaxscore + float(question['question']['props']['maxscore'])
                except:
                    qmaxscore = qmaxscore
                
          
        # calc maxscore for quiz
        
        data['p'] = {}
        data['p']['maxscore'] = qmaxscore
        for p in data['props']:
            data['p'][p['name']] = p['value']
        data['props'] = data['p']
        del data['p']  
        
         
        return data  
    