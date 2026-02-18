"""
Network utility plugins
"""
import socket
import requests
import urllib.parse
from typing import Dict, List, Any
from ..core import Plugin, register_plugin


@register_plugin(category="network")
class PortScannerPlugin(Plugin):
    """Scan network ports on a host"""
    
    def execute(self, host: str, ports: List[int] = None, timeout: float = 1.0) -> Dict[int, bool]:
        """
        Scan ports on a host
        
        Args:
            host: Hostname or IP address
            ports: List of ports to scan (default: common ports)
            timeout: Connection timeout in seconds
        
        Returns:
            Dictionary mapping port numbers to their status (open/closed)
        """
        if ports is None:
            # Common ports
            ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 8080, 8443]
        
        results = {}
        
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            
            try:
                result = sock.connect_ex((host, port))
                results[port] = (result == 0)
            except socket.error:
                results[port] = False
            finally:
                sock.close()
        
        return results


@register_plugin(category="network")
class URLValidatorPlugin(Plugin):
    """Validate and parse URLs"""
    
    def execute(self, url: str, check_reachable: bool = False) -> Dict[str, Any]:
        """
        Validate and parse a URL
        
        Args:
            url: URL to validate
            check_reachable: Check if URL is reachable via HTTP
        
        Returns:
            Dictionary with URL components and validation status
        """
        try:
            parsed = urllib.parse.urlparse(url)
            result = {
                "valid": bool(parsed.scheme and parsed.netloc),
                "scheme": parsed.scheme,
                "netloc": parsed.netloc,
                "path": parsed.path,
                "params": parsed.params,
                "query": parsed.query,
                "fragment": parsed.fragment
            }
            
            if check_reachable and result["valid"]:
                try:
                    response = requests.head(url, timeout=5, allow_redirects=True)
                    result["reachable"] = response.status_code < 400
                    result["status_code"] = response.status_code
                except:
                    result["reachable"] = False
            
            return result
        except Exception as e:
            return {"valid": False, "error": str(e)}


@register_plugin(category="network")
class HTTPRequestPlugin(Plugin):
    """Make HTTP requests with various methods"""
    
    def execute(self, url: str, method: str = "GET", headers: Dict = None, 
                data: Any = None, timeout: int = 30) -> Dict[str, Any]:
        """
        Make an HTTP request
        
        Args:
            url: URL to request
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            headers: Request headers
            data: Request body data
            timeout: Request timeout in seconds
        
        Returns:
            Dictionary with response details
        """
        try:
            response = requests.request(
                method=method.upper(),
                url=url,
                headers=headers,
                json=data if isinstance(data, dict) else None,
                data=data if not isinstance(data, dict) else None,
                timeout=timeout
            )
            
            return {
                "success": True,
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content": response.text[:1000],  # Limit content length
                "content_length": len(response.content),
                "encoding": response.encoding
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


@register_plugin(category="network")
class DownloadManagerPlugin(Plugin):
    """Download files from URLs with progress tracking"""
    
    def execute(self, url: str, destination: str = None, chunk_size: int = 8192) -> Dict[str, Any]:
        """
        Download a file from a URL
        
        Args:
            url: URL to download from
            destination: Local file path to save to
            chunk_size: Download chunk size in bytes
        
        Returns:
            Dictionary with download details
        """
        try:
            if destination is None:
                # Extract filename from URL
                destination = url.split('/')[-1] or 'downloaded_file'
            
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(destination, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
            
            return {
                "success": True,
                "destination": destination,
                "size": downloaded,
                "url": url
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


@register_plugin(category="network")
class DNSLookupPlugin(Plugin):
    """Perform DNS lookups and reverse lookups"""
    
    def execute(self, target: str, lookup_type: str = "forward") -> Dict[str, Any]:
        """
        Perform DNS lookup
        
        Args:
            target: Hostname or IP address
            lookup_type: Type of lookup (forward or reverse)
        
        Returns:
            Dictionary with lookup results
        """
        try:
            if lookup_type == "forward":
                # Hostname to IP
                ip_address = socket.gethostbyname(target)
                return {
                    "success": True,
                    "hostname": target,
                    "ip_address": ip_address
                }
            elif lookup_type == "reverse":
                # IP to hostname
                hostname = socket.gethostbyaddr(target)[0]
                return {
                    "success": True,
                    "ip_address": target,
                    "hostname": hostname
                }
            else:
                return {
                    "success": False,
                    "error": f"Unknown lookup type: {lookup_type}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
