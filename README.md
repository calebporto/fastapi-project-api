<h1>IBVG API</H1>
<p>Api em FastAPI para transações com o banco de dados</p>
<p><b>Tecnologias Utilizadas:</b> FastAPI, async SQLAlchemy, Pydantic, Requests, OpenAPI, Middleware, JSON</p>
<br>
<h3>Aplicação para gerenciamento completo de uma igreja</h3>

<h4>Sobre o Projeto:</h4>
<p>- Páginas abertas ao público em geral (Home/Quem Somos/Projetos Sociais/Contato);</p>
<p>- Páginas de acesso (Entrar, Cadastrar-se);
<p>- Painel de membros, com autorização de acesso via registro de sessão de usuário com cookies;
<p>- Painel administrativo, com diversas funções para manutenção de usuários, registro de entradas e saídas de valores, visualização
de relatórios financeiros por período, saídas e entradas ou ambos;
<p>- Scheduler (agendador de tarefas) para envio de e-mail, whatsapp e geração automática de relatórios por período; (Em desenvolvimento)
<p>- Registro de logs de erros; (Em desenvolvimento)
<p>- Senha exclusiva para designers, para fácil manutenção da parte gráfica das páginas públicas. (Em desenvolvimento)

<h4>Arquitetura:</h4>
<p>Cliente <------> Backend <-------> API <-------> Banco de Dados</p>
<p><b>Backend em Flask:</b> https://github.com/calebporto/flask-project-backend</p>
<br>

<h1>Sobre a API</h1>
<h3>Características:</h3>
<p>- Conexões seguras e performáticas com o banco de dados, usando async SQLAlchemy;</p>
<p>- Middleware para autorização de acesso, via api_key obtida do cabeçalho http;</p>
<p>- Uso de classes Pydantic, facilitando a leitura do código e simplificando o trabalho;</p>
<p>- Endpoints específicos para o scheduler.</p>
<h3>Finalidade:</h3>
<p>- Isolar as transações com o banco de dados do Backend, gerando mais algumas camadas de segurança;</p>
<p>- Facilitar a manutenção da aplicação;</p>
<p>- Dividir o projeto em blocos, conforme arquitetura de microsserviços.</p>
<h3>Observações:</h3>
<p>Caso queira baixar o código para rodar no seu computador, você deve saber que para acessar a API
pelo localhost, deve ser fornecido um cabeçalho {'api_key':<...>, 'id':<...>}, onde os valores fornecidos no cabeçalho devem coincidir com as variáveis de ambiente de mesmo nome.
Para isso, você deve criar um arquivo .env dentro da pasta models, com as variáveis API_KEY e AUTHORIZED_ID, com os valores que você achar melhor. Esses valores devem ser os mesmos do cabeçalho 
fornecido na requisição http.</p>
<p>Você deve instalar as dependencias com o comando 'pip install -r requirements.txt' no seu terminal, e para rodar o código, digite no terminal: 'uvicorn main:app --port=8000 --reload'</p>