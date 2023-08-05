"""Methods to connect N-Tier to aiohttp"""
from http import HTTPStatus
from typing import Any, Callable, Mapping, Optional

import ujson
from aiohttp.web import Request, Response, json_response
from ntier import (APITransactionBase, TransactionBase, TransactionCode,
                   TransactionInput, TransactionResult)
from webdi import Container

from .deserialize import RequestData

PAGE_DEFAULT = 1
PER_PAGE_DEFAULT = 25
PAGE_KEY = "page"
PER_PAGE_KEY = "per_page"
TOTAL_RECORDS_KEY = "total_records"
TOTAL_PAGES_KEY = "total_pages"
PAGING_KEY = "paging"
DATA_KEY = "data"
ERRORS_KEY = "errors"
TRANSACTION_CODE_MAP = {
    TransactionCode.success: HTTPStatus.OK,
    TransactionCode.found: HTTPStatus.OK,
    TransactionCode.created: HTTPStatus.CREATED,
    TransactionCode.updated: HTTPStatus.OK,
    TransactionCode.not_changed: HTTPStatus.OK,
    TransactionCode.deleted: HTTPStatus.OK,
    TransactionCode.failed: HTTPStatus.BAD_REQUEST,
    TransactionCode.not_found: HTTPStatus.NOT_FOUND,
    TransactionCode.not_authenticated: HTTPStatus.UNAUTHORIZED,
    TransactionCode.not_authorized: HTTPStatus.FORBIDDEN,
    TransactionCode.not_valid: HTTPStatus.UNPROCESSABLE_ENTITY,
}
Data = Mapping[str, Any]
Serializer = Callable[[Any], Any]
Deserializer = Callable[[RequestData], TransactionInput]


def set_paging(transaction: TransactionBase, data: RequestData) -> None:
    """Sets paging on a transaction class based on query string args."""
    page_str: Optional[str] = data.query.get(PAGE_KEY)
    per_page_str: Optional[str] = data.query.get(PER_PAGE_KEY)
    page: Optional[int] = None
    per_page: Optional[int] = None

    if page_str:
        try:
            page = int(page_str)
        except ValueError:
            page = PAGE_DEFAULT
    if per_page_str:
        try:
            per_page = int(per_page_str)
        except ValueError:
            per_page = PER_PAGE_DEFAULT

    if not (page or per_page):
        return

    if not page or page < 0:
        page = PAGE_DEFAULT
    if not per_page or per_page < 0:
        per_page = PER_PAGE_DEFAULT

    transaction.set_paging(page, per_page)


def map_transaction_code(code: TransactionCode) -> HTTPStatus:
    """Map a TransactionCode to an HTTPStatus code."""
    status_code = TRANSACTION_CODE_MAP.get(code)
    if status_code is None:
        raise Exception(f"Unrecognized transaction code: {code}")
    return status_code


async def build_transaction_data(request: Request) -> RequestData:
    """Build a dict from a Request object."""
    if request.can_read_body:
        body = await request.json()
    else:
        body = None
    return RequestData(request.query, request.match_info, body)


async def execute_transaction(
    transaction_name: str,
    deserialize: Deserializer,
    serialize: Serializer,
    container: Container,
    request: Request,
) -> Response:
    """Call a transaction with data from a request and build a JSON response."""
    request_data = await build_transaction_data(request)
    transaction_input = deserialize(request_data)
    transaction: APITransactionBase = container.get(transaction_name)
    set_paging(transaction, request_data)
    result = await transaction(transaction_input)
    http_status = map_transaction_code(result.status_code)

    if http_status < HTTPStatus.BAD_REQUEST:
        result_data = {DATA_KEY: serialize(result.payload)}
        if result.has_paging:
            result_data[PAGING_KEY] = {
                PAGE_KEY: result.paging.page,
                PER_PAGE_KEY: result.paging.per_page,
                TOTAL_RECORDS_KEY: result.paging.total_records,
                TOTAL_PAGES_KEY: result.paging.total_pages,
            }
        return json_response(result_data, status=http_status, dumps=ujson.dumps)

    result_data = {ERRORS_KEY: result.payload}
    return json_response(result_data, status=http_status, dumps=ujson.dumps)
