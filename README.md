# Conector EnturOS CRM para o Claude

Este pacote conecta o Claude Desktop diretamente ao seu CRM (EnturOS), para você
poder pedir coisas como "liste meus contatos", "crie uma negociação para o cliente X"
ou "mostre o resumo de vendas do mês" direto no chat.

## Baixar

**[⬇️ Clique aqui para baixar o arquivo `enturos-crm-mcp.mcpb`](https://raw.githubusercontent.com/RenanhvBorges/enturOS_mcp/main/enturos-crm-mcp.mcpb)**

É o único arquivo que você precisa. Depois de baixado, siga o passo a passo abaixo.

## O que você precisa antes de começar

1. Ter o **Claude Desktop** instalado no computador (baixe em claude.ai/download, se ainda não tiver).
2. Estar **conectado à internet** (necessário na primeira instalação).
3. Sua **chave de API do EnturOS CRM**. Para gerar uma:
   - Entre no painel do EnturOS CRM.
   - Vá em **Configurações > API**.
   - Clique em gerar uma nova chave (formato `enturos_live_...`).
   - **Copie a chave na hora** — ela só aparece uma vez.

## Como instalar (leva 1 minuto)

1. Baixe o arquivo **`enturos-crm-mcp.mcpb`** (é o único arquivo que você precisa).
2. Dê **duplo clique** nele. Isso abre o Claude Desktop com uma tela de instalação.
   - Se o Windows ou o Mac perguntar "tem certeza que quer abrir esse arquivo?", pode confirmar.
   - O Claude Desktop pode avisar que a extensão "não é assinada" — isso é normal para
     conectores privados como este; pode seguir em frente e instalar.
3. Na tela de instalação, cole a **chave de API** que você copiou no painel do EnturOS
   no campo indicado.
4. Clique em **Instalar**.
5. Pronto. Feche e abra o Claude Desktop novamente para garantir que carregou.

Na primeira vez que você usar (fizer uma pergunta que precise do CRM), o Claude pode
demorar alguns segundos a mais — ele está baixando algumas peças internas automaticamente.
Da segunda vez em diante é instantâneo.

## Como testar se funcionou

No Claude Desktop, pergunte algo como:

> Liste meus últimos 5 contatos do CRM

Se aparecer uma lista de contatos (ou uma mensagem dizendo que não há contatos ainda),
está tudo certo. Se aparecer uma mensagem de erro mencionando "ENTUROS_API_KEY", a chave
não foi salva corretamente — desinstale a extensão nas configurações do Claude Desktop e
repita a instalação, conferindo se colou a chave certa.

## O que dá para fazer com ele

- **Contatos**: buscar, ver detalhes, criar, editar, aplicar tags, achar/mesclar duplicados.
- **Negociações**: listar, criar, mover de etapa, marcar como ganha/perdida, adicionar produtos.
- **Contas (B2B)**, **Propostas comerciais** (com roteiro, voos e hotéis), **Funis e etapas**.
- **Tarefas**, **Notas**, **Tags**, **Catálogo de produtos**.
- **Analytics**: resumo de KPIs, funil de conversão, motivos de perda.
- **RFV** (score de recência/frequência/valor dos contatos) e **Segmentos de audiência**.
- **Campos personalizados** e **Webhooks**.

Ações que apagam ou alteram dados de forma importante (excluir um contato, marcar uma
negociação como perdida, etc.) sempre pedem sua confirmação antes de o Claude executar.

## Problemas comuns

- **"Credencial inválida" / erro 401**: a chave de API expirou ou foi revogada no painel.
  Gere uma nova chave e reinstale o pacote (desinstalar e instalar de novo com a chave nova).
- **"Permissão negada" / erro 403**: a chave não tem permissão (escopo) para aquela ação
  específica. Peça ao administrador do CRM para ajustar os escopos da chave no painel.
- **Nada acontece ao clicar no arquivo `.mcpb`**: confirme que o Claude Desktop está
  instalado e atualizado (Ajuda > Verificar atualizações).
- **Erro de rede citando DNS (ex: "nodename nor servname provided")**: o endereço da
  API do CRM não foi encontrado na internet — normalmente indica que o endereço mudou do
  lado do EnturOS. Vá em Configurações > Extensões > EnturOS CRM no Claude Desktop e
  confira o campo avançado "Endereço da API (avançado)": ele deve ser
  `https://crm.enturos.com/api/v1`, a menos que o suporte do EnturOS informe outro.
- **Falha na instalação citando "invalid peer certificate" / "UnknownIssuer" (comum em
  Windows corporativo com antivírus)**: acontece quando um antivírus ou proxy da empresa
  inspeciona o tráfego HTTPS. A partir da versão 0.3.0 deste pacote isso já vem corrigido
  automaticamente — baixe a versão mais recente do `enturos-crm-mcp.mcpb` e instale de
  novo. Se persistir, pode ser necessário que o time de TI libere o acesso a
  `pypi.org` e `files.pythonhosted.org` no antivírus/firewall.

## Segurança

A chave de API é armazenada de forma protegida pelo próprio Claude Desktop (nunca em
texto simples) e é usada apenas para falar com o EnturOS CRM em seu nome. Não compartilhe
sua chave de API com ninguém — se ela vazar, revogue-a no painel do EnturOS e gere outra.
