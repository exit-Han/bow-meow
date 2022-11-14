from flask import request, render_template
from flask_restx import Resource, Api, Namespace, fields


Test = Namespace('Test')

test_model = Test.model('test_model', {
    'test': fields.String(description='example', required=True)
})

@Test.route('/new')
class TestCreate(Resource):
    @Test.expect(test_model)
    def post(self): 
        result = request.json.get('test')
        return result