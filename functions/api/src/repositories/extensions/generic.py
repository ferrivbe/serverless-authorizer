import base64
import hashlib
import hmac


class GenericExtensions:
    """
    Handles all repository generic extensions.
    """

    def get_secret_hash(client_param: str, client_id: str, client_secret: str) -> str:
        """
        Calculates the secret hash for the given email and client secret.

        :param client_param: The client_param of the user.
        :type client_param: str
        :return: The secret hash.
        :rtype: str
        """
        message = client_param + client_id
        digest_result = hmac.new(
            str(client_secret).encode("utf-8"),
            msg=str(message).encode("utf-8"),
            digestmod=hashlib.sha256,
        ).digest()
        decode_result = base64.b64encode(digest_result).decode()

        return decode_result
