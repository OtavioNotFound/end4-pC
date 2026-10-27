# Personalizar barra, dock e widgets / Personalize bar, dock and widgets

Estas melhorias estão no checkout local da branch feat/settings-usability-p0.
Não são um instalador de Hyprland e ainda precisam da validação gráfica indicada no relatório.

## Abrir

Use o atalho de configurações já existente no seu ambiente. No dashboard, use
**Monte sua barra**, **Configure sua dock** ou **Configurar widgets do desktop**.
Nos estilos tradicional e mínimo, use **Barra**, **Dock** e **Widgets** na navegação.
Os atalhos do dashboard abrem as páginas nativas e não mudam o estilo salvo do painel.

Para testar este checkout, siga [o guia de primeiros passos](../getting-started.md): diagnóstico, backup e parada
somente da instância anterior antes de executar `qs -p .` na pasta do repositório.
Não execute duas shells sobre a mesma configuração.

## Barra

1. Abra **Barra**. Escolha em quais monitores ela aparece.
2. No editor, selecione um item do catálogo ou da barra. Não é necessário arrastar.
3. Use **Adicionar em**, **Mover para**, **Mover para antes/depois** ou **Remover da barra**.
4. As configurações disponíveis daquele item aparecem no próprio editor. Use a rolagem
interna para ver todas. **Abrir todas as opções** acessa a seção original quando existir.
5. **Desfazer alteração de disposição** restaura só a última mudança de layout, inclusive
limpar todos os itens. Não desfaz ajustes de aparência ou workspaces. Se outra edição
alterar a disposição depois, o desfazer fica indisponível para não sobrescrevê-la.

A Ilha Dinâmica precisa de barra horizontal e centro exclusivo. Separadores precisam
do estilo de grupo transparente. Essas limitações aparecem em texto. Itens antigos
que o catálogo não conhece continuam salvos até você removê-los explicitamente.

Em **Visibilidade da barra**, escolha a área sensível do mouse, a revelação com Super e
o atraso. Ative a ocultação automática para usar esses controles. Abrir espaço nas
janelas significa reservar espaço enquanto a barra estiver revelada, não enquanto oculta.
Mudar para barra vertical não converte nem apaga sua composição automaticamente.

## Dock

Abra **Dock** para configurar visibilidade, comportamento, tamanho, estilo e monitores.
A ampliação de ícones só funciona na borda inferior; mover para outra borda mantém
seu valor salvo. Fixar na inicialização tem efeito no próximo início da shell.

Em **Aplicativos fixados**, use ↑/↓ para ordenar ou **Desafixar** para remover da dock.
Isso não desinstala aplicativos. Busque pelo nome para fixar um aplicativo instalado.
Entradas indisponíveis são mostradas e preservadas. A lista de busca mostra até 30
resultados; digite para filtrar. Regras avançadas existentes continuam nas opções anteriores.

A seleção vazia de monitores significa **todos, incluindo novos monitores**. Nomes de
monitores desconectados continuam salvos. Não é permitido desmarcar o último monitor
pelo seletor; escolha outro ou volte para todos.

## Widgets

Escolha o widget no catálogo. **Mostrar no desktop** controla sua ativação.
**Mostrar no menu do desktop** controla a presença no menu, sem ligar/desligar o widget.
No dashboard, clique no cartão para configurar; o switch do cartão controla a ativação.
A estrela representa a presença no menu, com dica explicativa.

- Relógio: estilo e controles relevantes ao estilo escolhido.
- Clima: cidade, GPS e unidades compartilhados com o clima da barra.
- Recursos: orientação, CPU, memória e terceira medição. Automático usa bateria quando
há bateria, ou disco caso contrário. Ocultar todas as medições deixa o widget sem cartões.
- Mídia: escolha a disposição. Sem um reprodutor compatível, ele continua ativado,
mas não tem dados de mídia; esse estado é informado.
- Texto personalizado: conteúdo, fonte, tamanho e cores, reutilizando o widget existente.

O catálogo inclui os 16 widgets carregados pelo desktop. Isso não significa que todos
já ganharam um editor completo: os detalhes de outros widgets ainda serão ampliados.
Onde não há controles específicos novos, a página informa esse limite.

**Posicionar próximo ao canto superior esquerdo** recupera um widget e seleciona
posicionamento manual. Preserva conteúdo, imagens, notas e tarefas. **Desfazer
posicionamento do widget** recupera as coordenadas anteriores se elas não mudaram
em outro lugar. As coordenadas e os monitores do desktop são compartilhados;
não há configuração independente por widget/monitor nesta entrega.

**Bloquear posições dos widgets** evita movimentações acidentais. Não apaga nada.

## English

Open the existing settings shortcut. The dashboard offers **Build your bar**,
**Configure your dock**, and **Configure desktop widgets**; classic/minimal settings
have Bar, Dock, and Widgets pages. Select a bar item to add, move, remove, or edit it.
Dragging is optional. Layout undo affects only the last layout operation and refuses
conflicting external changes. Existing unknown item IDs remain intact.

The Dock page manages pinned apps, native appearance/behavior settings, and monitors.
Unpinning does not uninstall. Empty monitor selection means all monitors, including new
ones. Dock magnification works only on the bottom edge; startup pinning applies next start.

Widget configuration is separate from desktop visibility and menu membership. Clock,
weather, resources, media layouts and custom text have direct controls. Resource metric
choices preserve the original default layout. Inactive media means no data, not disabled.
Position recovery and its scoped undo preserve content; widget positions/desktop monitor
selection remain shared. Other widget editors, generic reset and generic undo are future work.
