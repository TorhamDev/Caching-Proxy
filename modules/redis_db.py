import typing

import redis


class RedisDB:
    """
    A class to manage an  connection to Redis for caching.
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        expiry_time_seconds: int = 300,
    ):
        """
        Initializes the AsyncRedisCache with connection details and default expiry.

        Args:
            host: The Redis server hostname or IP address.
            port: The Redis server port.
            db: The Redis database number to use.
            expiry_time_seconds: Default expiration time for cached items in seconds.
        """
        self._host = host
        self._port = port
        self._db = db
        self._expiry_time_seconds = expiry_time_seconds
        self._redis_client: typing.Optional[redis.Redis] = (
            None  # Store the client instance
        )

        # connect to the redis after init
        self._connect()

    def _connect(self):
        """
        Establishes the  connection to the Redis server.
        Call this method before performing any operations.
        """
        if self._redis_client is None:
            print(f"Connecting to Redis at {self._host}:{self._port}/{self._db}...")
            try:
                # Create the  Redis client instance
                self._redis_client = redis.Redis(
                    host=self._host,
                    port=self._port,
                    db=self._db,
                    decode_responses=True,  # Automatically decode responses to strings
                )
                # Ping the server to verify the connection
                self._redis_client.ping()
                print("Successfully connected to Redis.")
            except redis.exceptions.ConnectionError as e:
                print(f"Error connecting to Redis: {e}")
                self._redis_client = None  # Ensure client is None if connection fails
                raise  # Re-raise the exception to indicate failure

    def close(self):
        """
        Closes the connection to the Redis server.
        Call this method when your application is shutting down.
        """
        if self._redis_client:
            print("Closing Redis connection...")
            self._redis_client.close()
            self._redis_client = None
            print("Redis connection closed.")

    def get(self, key: str) -> typing.Optional[str]:
        """
        Retrieves a value from the cache by its key.

        Args:
            key: The key to retrieve.

        Returns:
            The cached value as a string, or None if the key does not exist.
        """
        if not self._redis_client:
            print("Redis client not connected. Cannot get key.")
            return None
        try:
            value = self._redis_client.get(key)
            # Redis GET returns None if the key does not exist
            return value
        except Exception as e:
            print(f"Error getting key '{key}' from Redis: {e}")
            return None

    def set(self, key: str, value: str, ex: typing.Optional[int] = None):
        """await
        Args:
            key: The key to set.
            value: The value to store (will be converted to string).
            ex: Optional expiration time in seconds. If None, uses the default.
        """
        if not self._redis_client:
            print("Redis client not connected. Cannot set key.")
            return
        try:
            # Use the provided expiration or the default
            self._redis_client.set(
                key, value, ex=ex if ex is not None else self._expiry_time_seconds
            )
        except Exception as e:
            print(f"Error setting key '{key}' in Redis: {e}")

    def delete(self, key: str):
        """
        Deletes a key from the cache.

        Args:
            key: The key to delete.
        """
        if not self._redis_client:
            print("Redis client not connected. Cannot delete key.")
            return
        try:
            self._redis_client.delete(key)
        except Exception as e:
            print(f"Error deleting key '{key}' from Redis: {e}")
