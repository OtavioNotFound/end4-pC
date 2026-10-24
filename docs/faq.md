# Perguntas frequentes / FAQ

## Onde está o modo escuro?

Na área de aparência do dashboard e nos botões sol/lua da página Quick.
O atalho de modo claro/escuro da barra depende da opção “Dark/Light toggle”.
Os controles existentes chamam o gerador de cores. Este fork não adiciona
um tema nem muda o modo padrão.

## Por que o tema da shell e o do aplicativo diferem?

São camadas distintas: a shell usa a paleta do Quickshell; aplicativos GTK
usam configurações GTK; aplicativos Qt usam seus estilos/temas; alguns apps
têm preferência própria. O pipeline original de `switchwall.sh` pode modificar
GTK, Qt, terminal e outras integrações conforme as opções existentes. As opções
de wallpaper theming controlam essa integração; o fork não impõe um novo tema
global nem promete que todo aplicativo acompanhe a shell.

## Glassy UI está ligado, mas não vejo o efeito

Confira o wallpaper real, inclusive extensão e permissões, antes de alterar
transparência. Veja [Glassy UI](glassy-ui.md). O fallback de cor mantém os
controles disponíveis, mas não equivale ao efeito de vidro funcionando.

## Alterei Persona. Por que voltou ao trocar de preset?

Você alterou a configuração ativa. Salve/sobrescreva o preset desejado para
persistir uma variação. Campos ausentes são mesclados; o nome do preset não
representa um snapshot completo. [Detalhes](configuration.md).

## Posso usar Persona, Maomao v2 e persona-teste existentes?

Sim, o esquema e a blacklist permanecem. Um asset inexistente passa a impedir
aplicação, com diagnóstico. Corrigir esse caminho pode ser necessário uma vez
em cada preset salvo. Não há migração silenciosa de imagens.

## Preciso de root ou copiar ícones para o sistema?

Não para usar a shell ou os fallbacks internos. Instalar dependências do sistema
é uma ação separada que você decide com seu gerenciador de pacotes.

## Como vejo atalhos e encontro opções?

No launcher, digite `<` para consultar os atalhos existentes; pesquise nomes
como `wallpaper`, `transparency` e `blur` para encontrar as opções. O fork não
instala atalhos novos. `Escape` fecha o overlay de configurações.

## Posso reiniciar sem sair do Hyprland?

Sim: na pasta do checkout, `qs kill -p .` seguido de `qs -p . --daemonize`.
Confira `qs list` antes para identificar a instância correta.

## O doctor corrige ou envia dados?

Não. É somente leitura e offline. `--report` produz JSON sanitizado localmente.
Correções, restauração e publicação são ações separadas. Scripts antigos de
compartilhamento continuam existindo, mas não são executados pelo diagnóstico.

**English:** dark/light controls already exist; application theming depends
on the original integration settings. Presets and active state differ. No root
is required for local fallbacks. The doctor neither repairs nor transmits data.
