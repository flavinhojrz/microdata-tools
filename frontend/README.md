# MicroData Tools

MicroData Tools é uma ferramenta web para limpar, converter e analisar planilhas
CSV e Excel sem exigir conhecimento técnico. A proposta é transformar arquivos
bagunçados em dados mais claros, portáveis e prontos para decisão.

O projeto nasce de um problema comum em pequenos negócios, operações comerciais e
rotinas administrativas: muitas informações importantes ficam presas em planilhas
exportadas de sistemas diferentes, com nomes de colunas inconsistentes, linhas
vazias, duplicatas, formatos brasileiros de número e data, e pouca visibilidade
sobre a qualidade dos dados.

## O Que A Ferramenta Faz

- Gera uma prévia inicial de arquivos CSV, XLSX e XLS.
- Remove linhas vazias, colunas vazias e registros duplicados.
- Padroniza nomes de colunas para um formato simples e previsível.
- Converte dados para JSON, Markdown e comandos SQL INSERT.
- Analisa a planilha para mostrar linhas, colunas, ausências, duplicatas,
  estatísticas numéricas, categorias frequentes e datas detectadas.
- Normaliza, quando solicitado, números e datas em formatos comuns no Brasil.
- Exporta resultados sem salvar arquivos no navegador ou criar banco de dados.

## Para Quem Foi Pensada

A interface foi desenhada para pessoas que trabalham com dados no dia a dia, mas
não necessariamente programam. O foco está em fluxos curtos, linguagem direta e
respostas visuais que ajudem o usuário a entender o que mudou no arquivo.

Casos de uso típicos:

- Conferir relatórios de vendas antes de enviar para outra pessoa.
- Limpar exports de maquininhas, ERPs, CRMs ou planilhas manuais.
- Transformar uma tabela em JSON, Markdown ou SQL para uso técnico posterior.
- Avaliar rapidamente a qualidade de uma base antes de importá-la em outro lugar.

## Experiência E Design

O design segue uma lógica de ferramenta operacional: poucos enfeites, controles
visíveis e resultado direto. A tela principal começa no fluxo útil, não em uma
página de marketing. O usuário envia um arquivo, vê uma prévia e escolhe a ação:
limpar, converter ou analisar.

Princípios usados na interface:

- clareza antes de densidade;
- ações explícitas, sem automações silenciosas;
- estados de erro e carregamento simples;
- tabelas e cartões compactos para facilitar comparação;
- linguagem em português, com termos próximos da rotina de planilhas;
- visual neutro para não competir com os dados.

## Segurança E Privacidade

O frontend envia o arquivo diretamente para a API configurada no ambiente de
produção. Por isso, a URL da API precisa ser um host confiável e usar HTTPS. A
aplicação não usa cookies de sessão nas chamadas de upload e não depende de
armazenamento local para processar os arquivos.

O backend processa os arquivos em memória, aplica limites de upload e retorna as
pré-visualizações ou downloads gerados. A ferramenta não foi desenhada para
armazenar arquivos, criar contas ou manter histórico de uploads.

Pontos de atenção para publicação:

- publicar frontend e backend apenas em HTTPS;
- configurar CORS somente para as origens públicas esperadas;
- manter limites de upload compatíveis com a infraestrutura;
- monitorar erros de parsing e tempo de resposta;
- evitar logs com conteúdo dos arquivos enviados;
- revisar política de privacidade antes de uso público.

## Motivação

Muitas ferramentas de dados começam complexas demais para problemas pequenos.
MicroData Tools segue o caminho oposto: resolver bem as primeiras tarefas que
quase todo mundo precisa fazer antes de analisar ou importar uma planilha.

A intenção é reduzir atrito. Em vez de pedir que o usuário aprenda fórmulas,
scripts ou processos longos, a ferramenta mostra uma prévia, executa limpezas
seguras e devolve um resultado fácil de conferir.

## Estado Atual

O produto já cobre o primeiro ciclo de uso:

- upload de CSV e Excel;
- prévia;
- limpeza básica;
- download do arquivo limpo;
- conversão para formatos técnicos;
- análise de qualidade e estatísticas;
- normalização brasileira opcional;
- headers de segurança no frontend;
- CORS configurável no backend;
- validações automatizadas no backend e frontend.

## Melhorias Planejadas

Melhorias de produto:

- seleção manual de colunas para limpeza;
- explicação visual das alterações linha a linha;
- suporte a múltiplas abas em arquivos Excel;
- perfis de limpeza reutilizáveis;
- detecção assistida de moeda, data, CPF/CNPJ e identificadores;
- comparação entre arquivo original e arquivo limpo;
- mensagens mais específicas para erros de planilha.

Melhorias de análise:

- score de qualidade dos dados;
- histogramas e distribuições simples;
- alertas sobre colunas com muitos valores ausentes;
- detecção de outliers;
- sugestões automáticas de próximas ações.

Melhorias de segurança e deploy:

- rate limit por IP ou usuário;
- métricas de tamanho, tempo e erro por endpoint;
- Content-Security-Policy com nonce para remover scripts inline;
- logs estruturados sem dados sensíveis;
- proteção opcional por autenticação ou chave de acesso;
- documentação pública de privacidade e retenção.

## Visão

MicroData Tools deve ser uma ponte entre planilhas comuns e dados confiáveis.
Pequena o suficiente para ser simples, prática o suficiente para virar hábito, e
transparente o suficiente para que o usuário sempre entenda o que aconteceu com
o arquivo.
