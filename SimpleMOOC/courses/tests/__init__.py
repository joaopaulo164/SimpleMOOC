# Os arquivos de teste filhos devem ser importados no arquivo __init__.py (neste arquivo) da pasta tests para serem carregados

from .test_views import HomeViewTest, ContactCourseTestCase
from .test_models import CourseManagerTestCase