import httpx


async def fetch_url(url: str):
    """
    Fetches content from a given URL asynchronously using httpx.

    Args:
        url: The URL to fetch.

    Returns:
        The text content of the response, or None if an error occurred.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, follow_redirects=True)

            # Raise an exception for bad status codes (4xx or 5xx)
            response.raise_for_status()

            return response.text

    except httpx.RequestError as e:
        print(f"An error occurred while requesting {url}: {e}")
        return None
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred for {url}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
