from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class BasePaginator(PageNumberPagination):
    page_size_query_param = "page_size"

    def __init__(self, page_size_setting, max_page_size_setting):
        self.page_size = getattr(settings, page_size_setting)
        self.max_page_size = getattr(settings, max_page_size_setting)


class LessonsPaginator(BasePaginator):
    def __init__(self):
        super().__init__(
            "PAGINATOR_LESSON_PAGE_SIZE", "PAGINATOR_LESSON_MAX_PAGE_SIZE"
        )


class CoursesPaginator(BasePaginator):
    def __init__(self):
        super().__init__(
            "PAGINATOR_COURSE_PAGE_SIZE", "PAGINATOR_COURSE_MAX_PAGE_SIZE"
        )
