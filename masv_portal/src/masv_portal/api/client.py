#!/usr/bin/env python3

# python/masv_portal/src/masv_portal/api/client.py

"""
Sending, receiving, and diagnosing requests to the MASV API.
"""

import json
from typing import Optional, Dict
import httpx

from masv_portal.config import get_api_key, debug

MASV_API_URL = "https://api.massive.app"

async def check_response(response: httpx.Response, verbose: bool = False) -> dict:
    """
    Handle a response.
    
    Args:
        response: Response from httpx request
        verbose: Show diagnostic info
        
    Returns:
        Parsed JSON of the response's body from the MASV server
        
    Raises:
        Exception: If the response indicates an error
    """
    body_text = response.text
    body = json.loads(body_text) if body_text else {}
    
    if verbose:
        debug(f"response status: {response.status_code}")
        debug(f"response body: {body_text}")
        
    if not response.is_success:
        raise Exception(body.get('message', 'Unknown error'))
        
    return body

async def request_async(
    path: str,
    *,
    method: str = 'GET',
    headers: Optional[Dict[str, str]] = None,
    body: Optional[str] = None,
    verbose: bool = False
) -> dict:
    """
    Send an async request and wait for a response.
    
    Sends a request to the MASV cloud and waits for its response.
    Optionally outputs diagnostic info for the request URL and the 
    status and body of the response.
    
    Args:
        path: The path for the endpoint for the MASV API. Must start with "/"
        method: HTTP method to use
        headers: Optional additional headers
        body: Optional request body
        verbose: Show diagnostic info
        
    Returns:
        Parsed JSON of the response's body from the MASV server
    """
    url = f"{MASV_API_URL}{path}"
    headers = headers or {}
    headers['X-API-Key'] = get_api_key()
    
    if verbose:
        debug(f"URL: {url}")
    
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=method,
            url=url,
            headers=headers,
            content=body
        )
        return await check_response(response, verbose)

def request(
    path: str,
    *,
    method: str = 'GET',
    headers: Optional[Dict[str, str]] = None,
    body: Optional[str] = None,
    verbose: bool = False
) -> dict:
    """
    Synchronous version of request_async.
    
    This is a convenience wrapper that runs the async request in a new event loop.
    """
    import asyncio
    
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(
        request_async(
            path,
            method=method,
            headers=headers,
            body=body,
            verbose=verbose
        )
    )