from flask_restful import Resource

class Foo(Resource):
    def get(self, id="World"):
        return f"Hello {id}!"
    def post(self):
        pass
