"""Servidor local que simula wellaraujo.com.br.

A raiz serve este site pessoal e cada /<repo>/ serve a pasta do projeto
correspondente, como o GitHub Pages fará quando o domínio for ligado ao
repositório welwelaraujo.github.io.

Uso: python visualizar.py   (abre http://localhost:8000)
"""
import functools
import http.server
import os
import webbrowser

AQUI = os.path.dirname(os.path.abspath(__file__))
# Caminho na URL -> pasta publicada de cada projeto.
PROJETOS = {
    '/projetos_santoandre': os.path.join(AQUI, '..', 'projetos_santoandre', 'docs'),
}
PORTA = 8000


class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        for prefixo, pasta in PROJETOS.items():
            if path.startswith(prefixo + '/'):
                # Troca a raiz só durante a tradução e reaproveita a normalização da classe-mãe.
                raiz, self.directory = self.directory, os.path.abspath(pasta)
                try:
                    return super().translate_path(path[len(prefixo):])
                finally:
                    self.directory = raiz
        return super().translate_path(path)

    def do_GET(self):
        # /<repo> sem barra final quebraria os links relativos.
        caminho = self.path.split('?')[0]
        if caminho in PROJETOS:
            self.send_response(301)
            self.send_header('Location', caminho + '/')
            self.end_headers()
            return
        super().do_GET()


if __name__ == '__main__':
    servidor = http.server.ThreadingHTTPServer(
        ('127.0.0.1', PORTA), functools.partial(Handler, directory=AQUI))
    url = f'http://localhost:{PORTA}/'
    print(f'Site local em {url}  (Ctrl+C para parar)')
    webbrowser.open(url)
    servidor.serve_forever()
