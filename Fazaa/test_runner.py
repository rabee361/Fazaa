import warnings
from django.test.runner import DiscoverRunner
from django.test.utils import override_settings

class ExampleTestRunner(DiscoverRunner):
    def run_tests(self, *args, **kwargs):
        # Show all warnings once, especially to show
        DeprecationWarning
        # messages which Python ignores by default
        warnings.simplefilter("default")
        return super().run_tests(*args, **kwargs)
        
    
TEST_SETTINGS = {
"PAGINATION_COUNT": 10,
"DEBUG": False
}