# Auto Acesso

Este projeto Python utiliza a biblioteca Selenium para automatizar o acesso a websites usando uma lista de proxies especificada em um arquivo CSV. A interface gráfica é construída usando Tkinter, permitindo ao usuário interagir facilmente com o programa. O principal objetivo é testar a eficácia de diferentes proxies para acessar um elemento específico em uma página web e clicar nele.

## Funcionalidades

- **Carregamento de Proxies via CSV**: Carrega uma lista de proxies de um arquivo CSV, onde cada proxy é testado sequencialmente.
- **Acesso Automatizado a Websites**: Utiliza o Selenium para abrir um navegador e tentar acessar um site utilizando os proxies carregados.
- **Interatividade Gráfica**: Permite ao usuário iniciar e pausar o teste através de uma interface gráfica.
- **Logs de Atividades**: Exibe logs de todas as atividades realizadas, incluindo sucessos e erros, em uma área de texto scrollável.
- **Relatório de Sessão**: Gera um arquivo CSV ao final da sessão com todos os logs de atividades.

## Tecnologias Utilizadas

- Python
- Selenium WebDriver
- Tkinter
- CSV

## Como Usar

### Configuração Inicial

1. **Instalação de Dependências**:
   - Certifique-se de que Python está instalado na sua máquina.
   - Instale o Selenium e as dependências do Tkinter com o seguinte comando:
     ```bash
     pip install selenium tkinter
     ```
   - Garanta que o driver correto para o navegador (por exemplo, ChromeDriver) está disponível e configurado corretamente.

2. **Preparação do Arquivo CSV**:
   - Prepare um arquivo CSV nomeado `proxies.csv` com colunas para 'IP Address', 'Port', e 'Https'. Certifique-se de que cada proxy é listado corretamente.

### Executando a Aplicação

1. **Iniciar a Interface**:
   - Execute o script Python para abrir a interface gráfica:
     ```bash
     python nome_do_arquivo.py
     ```
   - Insira a URL e o ID do elemento da página que deseja testar nos campos correspondentes da interface.

2. **Iniciar o Teste**:
   - Clique no botão "Iniciar Teste" para começar a testar os proxies. O programa tentará acessar o site e clicar no elemento especificado usando cada proxy listado no arquivo CSV.

3. **Visualizar Logs e Pausar o Teste**:
   - Os logs de acesso serão exibidos na área de texto scrollável. Você pode pausar o teste a qualquer momento clicando no botão "Pausar".
   - Ao pausar, um arquivo CSV chamado `report.csv` será gerado com todos os logs da sessão.

## Contribuições

Contribuições são bem-vindas para melhorar a aplicação ou adicionar novas funcionalidades. Sinta-se à vontade para clonar o repositório, propor mudanças ou abrir issues para discussão.
