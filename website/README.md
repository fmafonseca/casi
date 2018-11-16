**Ferramentas para criar** https://fmafonseca.github.io/casi/

## Criando o website

Instalar os pacotes necessários (apenas a primeira vez):

```
$ pip install ghp-import
```

Clonar o repositório localmente e acessar a pasta website:

```
$ git clone https://github.com/fmafonseca/casi.git
$ cd website
```

Criar a estrutura do "site" (as páginas html que compreendem os notebooks):

```
$ python convert_notebooks_to_html.py
```

Publicar as páginas no github

```
$ ghp-import output
$ git push origin gh-pages
```