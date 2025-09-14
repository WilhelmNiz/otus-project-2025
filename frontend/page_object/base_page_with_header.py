from frontend.page_object.base_page import BasePage
from frontend.page_object.header_elements import HeaderElements


class BasePageWithHeader(BasePage):
    """Базовый класс для всех страниц с header"""

    def __init__(self):
        super().__init__()
        self.header = HeaderElements()