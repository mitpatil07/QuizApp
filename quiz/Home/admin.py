from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import JavaQuestion, CppQuestion, PythonQuestion

# Optional: Define separate resources if you want to customize fields
@admin.register(JavaQuestion)
class JavaQuestionAdmin(ImportExportModelAdmin):
    pass

@admin.register(CppQuestion)
class CppQuestionAdmin(ImportExportModelAdmin):
    pass

@admin.register(PythonQuestion)
class PythonQuestionAdmin(ImportExportModelAdmin):
    pass
