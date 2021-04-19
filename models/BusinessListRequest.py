class BusinessListRequest:

    def get_page_size(self):
        return self._page_size

    def set_page_size(self, page_size):
        self._page_size = page_size

    def get_page(self):
        return self._page

    def set_page(self, page):
        self._page = page

    def get_from_date(self):
        return self._from_date

    def set_from_date(self, from_date):
        self._from_date = from_date

    def get_to_date(self):
        return self._to_date

    def set_to_date(self, to_date):
        self._to_date = to_date

