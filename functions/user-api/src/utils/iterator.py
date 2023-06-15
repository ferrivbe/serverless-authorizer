class AsyncIteratorWrapper:
    """
    This class provides an asynchronous iterator wrapper around a regular iterator.

    :param obj: The object to be wrapped as an asynchronous iterator.
    :type obj: object
    """

    def __init__(self, obj):
        """
        Initializes the AsyncIteratorWrapper instance.

        :param obj: The object to be wrapped as an asynchronous iterator.
        :type obj: object
        """
        self._it = iter(obj)

    def __aiter__(self):
        """
        Returns the asynchronous iterator object.

        :return: The asynchronous iterator object.
        :rtype: AsyncIteratorWrapper
        """
        return self

    async def __anext__(self):
        """
        Retrieves the next value from the iterator.

        :return: The next value from the iterator.
        :rtype: object

        :raises StopAsyncIteration: Raised when there are no more items in the iterator.
        """
        try:
            value = next(self._it)
        except StopIteration:
            raise StopAsyncIteration
        return value
