from urllib.parse import urlparse

class DomConfig:
    def __init__(self, allowed_ip='127.0.0.1', allowed_hosts=None, allowed_schemes=None):
        if allowed_hosts is None:
            allowed_hosts = {'localhost', '127.0.0.1'}
        if allowed_schemes is None:
            allowed_schemes = {'http', 'https'}
        
        self.allowed_ip = allowed_ip
        self.allowed_hosts = allowed_hosts
        self.allowed_schemes = allowed_schemes

    def localhost_identifier(self, request):
        return request.remote_addr == self.allowed_ip

    def url_segura(self, url2):
        try:
            resultado = urlparse(url2)
            return resultado.scheme in self.allowed_schemes and resultado.hostname in self.allowed_hosts
        except (ValueError, AttributeError):
            return False