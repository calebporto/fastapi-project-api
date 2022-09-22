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
<p>- Scheduler (agendador de tarefas) para envio de e-mail, whatsapp e geração automática de relatórios por período;
<p>- Registro de logs de erros;
<p>- Senha exclusiva para designers, para fácil manutenção da parte gráfica das páginas públicas.

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
