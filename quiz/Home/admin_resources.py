# Home/admin_resources.py
from import_export import resources
from .models import JavaQuestion, CppQuestion, PythonQuestion

class JavaQuestionResource(resources.ModelResource):
    class Meta:
        model = JavaQuestion

class CppQuestionResource(resources.ModelResource):
    class Meta:
        model = CppQuestion

class PythonQuestionResource(resources.ModelResource):
    class Meta:
        model = PythonQuestion
