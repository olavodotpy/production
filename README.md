### Introdução


Todo projeto que você pretende colocar em deploy para subir em domínio público, não apenas no seu ambiente de desenvolvimento, precisa de toda uma infraestrutura ou seja diferentes serviços e processos que podem escalar lateralmente em vários containers obrigatoriamente com o seu código fonte que está, provavelmente, no seu repositório Git.


O Famoso "Só funciona na minha máquina" só ocorre quando não se sabe que, para subir uma aplicação web, não depende da sua linguagem ou do seu framework, muitos pensariam que é só comprar um domínio e apontar para o endereço e acabou, sou um desenvolvedor web. Infelizmente não é tão simples assim. 


Depois desse disclaimer irei abordar toda a minha experiência e alguns passos importantes para configurar todo o ambiente de desenvolvimento e produção, realizando o deploy de um projeto de teste usando o framework Django. Estou usando o Railway como hospedagem e deployment e também Docker para container, irei abordar cada uma dessas tecnologias e o processo que todos devem fazer para criar uma boa infraestrutura.


### Ambientes virtuais e containers


Antes mesmo de criar a primeira pasta do projeto, ou a primeira linha do seu framework, você já pode errar brutalmente se antes você não criou o seu venv ou virtual environment no Python. Esse processo é necessário para separar as dependências de outros projetos. Além disso, até gerenciar a versão do python do sistema operacional por exemplo para evitar conflito. Para criar um environment via terminal do gerenciamento de pacotes pip execute o comando:


```pip
python -m venv <nome_do_ambiente>
```


O Docker foi uma opção que usei para fazer conteinerização do meu projeto, o Railway usa ele como padrão sem precisar de um dockerfile. Um container é um ambiente que simula um sistema operacional usado para empacotar as dependências e apps, executando o código. Tornando o leve comparado a VM(Máquinas Virtuais) sendo extremamente necessário para que o seu projeto e infraestrutura seja executada em qualquer ambiente e Sistema Operacional. No Railway tem um painel dentro de cada contêiner contendo as variáveis de ambientes, que são variáveis acessadas globalmente e contendo conteúdos privados, como senhas, tokens e chaves que ninguém pode ter acesso. Toda variável de ambiente é colocada em um arquivo .env e quando subir com um ```git commit``` 
lembre-se de listar no gitignore.


### Gerenciamento de dependências


Agora que criamos o ambiente virtual, iremos instalar o framework e montar o projeto junto com app, com cada funcionalidade independente. Como um app chamado blog que vai pegar informações do banco de dados e formar os templates, um outro app chamado users para gerenciamento de contas, configuarar a urls.py para endpoint, e a url.py do diretório do projeto que contém o settings.py para centralizar e reconhecer as urls dos apps. Outras bibliotecas que usei foram requests, DRF(Django REST Framework) para manipular API, gunicorn para servidor WSGI e pymemcache para cache. Todas essas bibliotecas vão ter que estar em um arquivo de manifesto como requirements.txt para que o Docker instale as dependências. Não ignore isso, é extremamente necessário pois faz com que todos os containers em produção e desenvolvedores tenham as dependências e versões certas. Use este comando via pip para atualizar o requirements:


```pip
pip freeze > requirements.txt
```


### Subindo arquivos estáticos no Railway


Agora que realizamos todo esse processo, vamos ver o nosso código funcionando. Coloque ```DEBUG = True``` pra subir na máquina local e execute com o comando:


```bash
python manage.py runserver
```


O Django tem um servidor local como o IP ```http://127.0.0.1:8000(localhost)``` que executa localmente na sua máquina, porém para fazer deploy não usaremos esse endereço.
O próximo passo é escolher o serviço de hospedagem como Railway, AWS, Heroku, Google cloud, etc... Existem várias que escalam da mesma forma, porém escolhi Railway por causa do plano gratuito.
O Railway irá subir o projeto através do repositório do Github toda a vez que o desenvolvedor fizer um ```git push``` para o  branch do repositório, provavelmente para o staging. Todo o repositório de projetos reais e que podem escalar, deve ter branch separados por exemplo o staging por exemplo para desenvolvedores testarem cada nova funcionalidade e correção de bugs e o main onde é a versão mais próxima do cliente e perfeita possível.


Os arquivos estáticos como os assets: imagens, CSS e JavaScript. colocaremos no diretório como ```myapp/static/myapp/assets/``` note que o nome do app é usado no subdiretório para facilitar o Django de localizar os arquivos certo nos templates. Vamos também mexer no settings.py para configurar o ```staticfiles``` que é o diretório que entregaremos ao Railway para servir os arquivos estáticos em produção. No settings.py vamos colocar o enderço da raiz do projeto no ```STATIC_ROOT``` para localizar a montagem quando rodamos o comando:


```bash
python manage.py collectstatic
```


colocaremos o caminho dos assets no ```STATICFILES_DIRS``` para localizar esses arquivos de maneira mais direta. Últimos passos para o primeiro deploy agora vai ser tornar esses arquivos estáticos mais rápidos e menos pesados para subir no Railway, usaremos o Whitenoise, no settings adicionaremos:


```python
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
```


Assim como o requirements.txt que carrega as dependências para o Docker, usaremos o procfile para executarmos indiretamente os primeiros comandos assim que o container for iniciado. Um exemplo seria assim:


```procfile
web: source /opt/example/bin/activate
web: python manage.py collectstatic
```


Começaremos cada linha com ```web:``` para indicar que iniciaremos um serviço web no Railway, Primeiro iniciaremos o ambiente virtual, depois o ```collectstatic``` para gravar os arquivos estáticos.
Feito tudo isso agora é só fazer um ```git commit``` e ```git push```  para subir no Railway o endereço do domínio aparecerá, e quando acessarmos, irá aparecer a página formatada porém, sem servidor.




### Finalizando, subindo o Servidor, Cache e Escalabilidades


Quando fiz uma integração com REST API que é um processo que precisa de alta requisição HTTP, tive os piores tipos de bugs, acho que foi tentando implementar isso que me dei o trabalho de fazer essa documentação e memorizei os status code como 5xx para erro interno, 0 para problemas de direitos, 4xx para no not found e bad request, 2xx para sucesso, 3xx para múltiplos processos. 


O ```manage.py runserver``` é embutido no Django e é utilizado em comandos simples para configurações no Railway ou para testes locais, mas não serve para ambientes de produção que requer múltiplos requisições ao mesmo tempo de muitos usuários, pois esse servidor embutido é single-threaded. Uma solução para esse problema é utilizar o servidor de aplicação WSGI(Web Server Gateway Interface) gunicorn que serve como um intermediário entre o balanceador de carga e a aplicação Django, garantindo uma boa segurança contra ataques DDoS por exemplo. Usando esse servidor conseguimos ter uma boa performance para múltiplas requisições pois suporta múltiplos workers permitindo que a aplicação processe mais requisições.


Meu plano gratuito do Railway tem o limite de 2 CPUs e 0.512GB disponíveis então é necessário ter bastante controle e evitar operações que custam memória e CPUs como as múltiplas requisições, já que cada worker equivalem a 1 CPU. Worker é um processo que possui memória própria e recursos funcionando independentemente da aplicação. A seguir p gunicorn mostra o tipo de modelo e um PID de processo de um worker:


```gunicorn
[2024-12-12 19:23:36 +0000] [1] [INFO] Using worker: sync
[2024-12-12 19:23:36 +0000] [5] [INFO] Booting worker with pid: 5
```


Meu view recebe de uma API da coingecko um JSON com muitas propriedades, e meu REST API recebe com método GET somente o título e um parágrafo de texto que está nesse JSON para o contexto, formando as variáveis do template. porém para cada atualização que o usuário faz da minha página about, uma requisição é feita para o endpoint api/consult/about E ainda pior, além do alto uso tanto de memória quanto do CPU para cada requisição, essa API coingecko possui um limite de 5 a 15 chamadas por minuto, quando se ultrapassa esse limite minha página retorna erro do tipo 5xx, exceção de dicionário, inválid Keys.


Na primeira vez que implementei a minha REST eu não sabia do limite de worker muito menos do CPU e memória, e então, deu ruim, os sintomas foram, pagina muito lento para carregar e dando status code do tipo 5xx (Internal Error [CRITICAL] WORKER TIMEOUT).


Cheguei a pesquisar no google sobre WORKER TIMEOUT e usuários do stack overflow falavam sobre acrescentar tempo de timeout e graceful-timeout no configfile do gunicorn, então, fiz essas modificações, a minha página só funciona 1 vez e quando atualizava novamente voltava ao erro. Então pesquisei mais sobre o gunicorn e então descobri sobre os limites, workers e processos por requisições. Subi o meu gunicorn para produção com 2 worker. Porém por algum motivo o número de workers não subia, então defini no painel do Railway em "Custom Start Command" o seguinte comando:


```bash
gunicorn django_production.wsgi:application --bind 0.0.0.0:8080 --timeout 120 --workers 2
```


Quando se aumenta recursos como CPU e memória isso se chama Escalabilidade Vertical, aumentando o número de worker para ter mais poder de processamento. Com isso resolvemos o problema do erro interno, só restando um, o problema de limite de requisição da API.


Pymemcache é um sistema de cache, uma forma de evitar requisições e número de operações do código. O melhor exemplo que eu poderia dar é:


Eu tenho um sistema que precisa pegar uma lista de produtos do meu ecommerce, para cada 1 mil usuários eu tenho em média 5 requi/s, e em cada requisição, acontece o seguinte: O meu código pega os itens do banco de dados, a partir de um loop while, e coloca todo o conteúdo dentro do meu contexto de variáveis para ser usado na montagem do template. Agora com o uso do Cache, na primeira requisição o meu sistema verifica se tem dados existentes dentro banco do cache, se não tiver eu faço o fluxo normal pegando a lista de itens só que agora no final da requisição eu guardo tudo dentro do cache, na próxima requisição eu vou estar com o contexto armazenado no cache evitando todo o fluxo do loop while e complexidade O(N) de itens para percorrer, só precisando agora de 1 processo de busca, poupando uso de CPU e memória.


Para implementar um sistema de cache eu precisei criar um container Docker só que pelo painel visual do Railway ficou super fácil e eu não precisei escrever 1 linha de código, e é assim que deveria ser, não é necessário um desenvolvedor escrever código diretamente dentro da linha da produção, tem que ser tudo automático para evitar conflitos. Quando se aumenta o número de containers e servidores isso se chama escalabilidade horizontal. 