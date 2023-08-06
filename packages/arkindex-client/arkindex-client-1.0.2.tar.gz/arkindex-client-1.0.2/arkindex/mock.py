# -*- coding: utf-8 -*-
import collections
import logging

import apistar

logger = logging.getLogger(__name__)

MockRequest = collections.namedtuple("MockRequest", "operation, body, args, kwargs")
MockResponse = collections.namedtuple(
    "MockResponse", "operation, response, args, kwargs"
)


class MockApiClient(object):
    """A mockup of the Arkindex API Client to build unit tests"""

    def __init__(self):
        self.history = []
        self.responses = []

    def add_response(self, operation_id: str, response: dict, *args, **kwargs):
        """Store a new mock response for an endpoint"""
        response = MockResponse(operation_id, response, args, kwargs)
        self.responses.append(response)
        return response

    def next_response(
        self,
        operation_id,
        *args,
        **kwargs,
    ):
        """Find the next available response for a request, and remove it from the stack"""
        for response in self.responses:
            if (
                response.operation == operation_id
                and response.args == args
                and response.kwargs == kwargs
            ):
                self.responses.remove(response)
                yield response.response

    def paginate(self, operation_id: str, body=None, *args, **kwargs):
        """Simply send back the next matching response"""
        return self.request(operation_id, body, *args, **kwargs)

    def request(self, operation_id: str, body=None, *args, **kwargs):
        """Send back a mocked response, or an exception"""

        # Save request in history
        self.history.append(MockRequest(operation_id, body, args, kwargs))

        # Find the next valid response
        response = next(self.next_response(operation_id, *args, **kwargs), None)
        if response is not None:
            logger.info(f"Sending mock response for {operation_id}")
            return response

        # Throw exception when no response is found
        logger.error(
            f"No mock response found for {operation_id} with body={body} args={args} kwargs={kwargs}"
        )
        raise apistar.exceptions.ErrorResponse(
            title="No mock response found",
            status_code=400,
            content="No mock response found",
        )
