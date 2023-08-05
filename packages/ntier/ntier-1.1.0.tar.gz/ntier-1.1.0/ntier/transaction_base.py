"""Contains the TransactionBase class."""
from typing import Optional, Tuple

from ntier.constants import PAGE_DEFAULT, PER_PAGE_DEFAULT, PER_PAGE_MAX
from ntier.transaction_result import TransactionResult


class TransactionBase:
    """Base class for transactions."""

    def __init__(self):
        self.paging: Optional[Tuple[int, int]] = None

    def set_paging(self, page: int, per_page: int) -> "TransactionBase":
        """Sets paging values for the transaction."""
        if page < 1:
            page = 1
        if per_page < 1:
            per_page = PER_PAGE_DEFAULT
        if per_page > PER_PAGE_MAX:
            per_page = PER_PAGE_MAX

        self.paging = (page, per_page)
        return self

    def parse_paging(
        self, raw_page: Optional[str], raw_per_page: Optional[str]
    ) -> "TransactionBase":
        """Tries to parse paging from string values.

        Paging parameters often come in on the request as strings and need to be parsed as
        integers.
        """
        page: Optional[int] = None
        per_page: Optional[int] = None

        if raw_page:
            try:
                page = int(raw_page)
            except ValueError:
                page = PAGE_DEFAULT
        else:
            page = PAGE_DEFAULT
        if raw_per_page:
            try:
                per_page = int(raw_per_page)
            except ValueError:
                per_page = PER_PAGE_DEFAULT
        else:
            per_page = PER_PAGE_DEFAULT

        self.set_paging(page, per_page)
        return self

    @property
    def offset(self):
        """Returns the offset based on the paging."""
        if self.paging is None:
            (page, per_page) = (PAGE_DEFAULT, PER_PAGE_DEFAULT)
        else:
            (page, per_page) = self.paging
        return (page - 1) * per_page

    @property
    def limit(self):
        """Returns the limit based on the paging."""
        if self.paging is None:
            return PER_PAGE_DEFAULT
        (_, per_page) = self.paging
        return per_page

    def set_output_paging(
        self, result: TransactionResult, total_records: int
    ) -> TransactionResult:
        """Assign paging to a TransactionResult."""
        if self.paging is None:
            (page, per_page) = (PAGE_DEFAULT, PER_PAGE_DEFAULT)
        else:
            (page, per_page) = self.paging
        result.set_paging(page, per_page, total_records)
        return result
