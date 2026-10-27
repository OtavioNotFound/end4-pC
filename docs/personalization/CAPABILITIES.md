# Mapa de capacidades — primeira entrega de personalização

Este mapa registra caminhos e consumidores verificados para esta entrega. O inventário
geral anterior está em ../UX_SETTINGS_INVENTORY.md. Não é uma certificação de todos os
parâmetros históricos do projeto: opções não rastreadas até um consumidor não foram
expostas como funcionalidades novas.

| Chave/função | Consumidor real | Controle/fluxo nesta entrega | Efeito e dependência | Verificação |
|---|---|---|---|---|
| bar.layouts.leftLayout/middleLayout/rightLayout | bar/BarContent.qml | DashboardBarLayoutCard compartilhado com BarConfig | Reativo; restrições Island/divisor | Regras JS, cena QML e botões reais |
| bar.vertical/bottom | bar/Bar.qml e BarContent.qml | Controles existentes de posição | Pode recriar geometria; sem conversão silenciosa do layout | Posições finais em Hyprland pendentes |
| bar.screenList | bar/Bar.qml e verticalBar/VerticalBar.qml | SettingsScreenSelection em BarConfig | Lista vazia mantém todos; desconectados permanecem salvos | Seletor QML; hotplug real pendente |
| bar.autoHide.enable | bar/Bar.qml | Controle existente de ocultação automática | Condiciona as quatro opções abaixo | Cena de estados; comportamento real pendente |
| bar.autoHide.hoverRegionWidth | bar/Bar.qml: margens da região de hover | Novo acesso explícito; 1–32 px | Área sensível do ponteiro | Consumidor e registro; teste manual de bordas pendente |
| bar.autoHide.pushWindows | bar/Bar.qml: normalExclusiveZone | Novo acesso explícito | Reserva espaço ao revelar, nunca ao estar oculta | Consumidor confirmado; tiling real pendente |
| bar.autoHide.showWhenPressingSuper.enable/delay | bar/Bar.qml: timer de Super | Novo acesso explícito; 0–1500 ms | Depende de autohide e opção de Super | Condições na UI; tecla real pendente |
| bar.workspaces.* | bar/Workspaces.qml e WorkspacesAlt.qml | Controles existentes agora junto do item | Estilo limita quais opções têm efeito | Alteração real do spin e persistência; desenho real pendente |
| bar.resources.* | bar/Resources.qml | Controles existentes junto do item | Métricas fornecidas por ResourceUsage | Clique real do switch; medições reais pendentes |
| bar.media.* | bar/Media.qml | Controles existentes junto do item | Precisa de player MPRIS para haver conteúdo | Sem ativar player nos testes |
| time.format/showDate | bar/ClockWidget.qml e services/DateTime.qml | Também acessíveis ao selecionar relógio da barra | Compartilhados com outros relógios; aviso explícito | Registro compartilhado; integração gráfica pendente |
| bar.widgetStyles | bar/BarGroup.qml | Mantido no editor de estilo existente da barra | Overrides por modo e widget | Novo acesso contextual no painel ainda pendente |
| dock.screenList | dock/Dock.qml: filtro de Quickshell.screens | Função nova na página Dock | Ausência/[] preserva todos os monitores | Fallback e nomes desconectados; dois monitores reais pendentes |
| dock.pinnedApps | services/TaskbarApps.qml e dock/Dock.qml | Lista com nomes, ícones, fixar/desafixar/reordenar | Reusa togglePin; movePinned preserva IDs desconhecidos | Serviço real em cena isolada |
| dock.position/style | dock/Dock.qml e common/DockStyle.qml | Controles existentes reunidos em Dock | inferior/esquerda/direita; float/hug | Página carrega; geometria real pendente |
| dock.magnify/magnification | common/DockStyle.qml | Controles existentes com explicação da limitação | Ampliação só funciona na borda inferior | UI não apaga valor salvo; efeito real pendente |
| dock.iconSize/iconSpacing/radius/showPreviews/... | dock/Dock.qml, common/DockStyle.qml e botões da dock | Mesmos accessors do catálogo existente | Não são opções recém-implementadas | Página real; limites visuais pendentes |
| background.widgets.*.enable | background/WidgetsLoader.qml | Switch próprio, separado de configurar | Estado salvo permanece mesmo sem dados externos | Serviço real e página QML |
| background.widgets.menuHidden | services/DesktopWidgets.qml e common/widgets/WidgetsSubmenu.qml | Mostrar no menu separado de mostrar no desktop | Não liga/desliga o widget | Serviço real; menu real pendente |
| background.widgets.customText.* | background/widgets/customtext/CustomTextWidget.qml | Integrado ao catálogo: agora 16 itens | Reusa widget e controles existentes | Página e preservação de conteúdo |
| background.widgets.clock.* | background/widgets/clock/* | Opções relevantes ao estilo escolhido | Estilos inativos mantêm valores salvos | Página real; cada estilo visual pendente |
| bar.weather.* | services/Weather.qml, widget weather e WeatherBar | Cidade/GPS/unidades no detalhe do widget | Compartilhado com a barra, explicado na UI | Serviços externos simulados; rede/GPS reais pendentes |
| background.widgets.resources.showCpu/showMemory/thirdMetric | background/widgets/resources/ResourcesWidget.qml | Funções novas: CPU, memória, automático/bateria/disco/oculto | Defaults true/true/auto mantêm os três cartões; bateria ausente mostra — | Componente real: dimensões padrão e alterações |
| background.widgets.resources.vertical | ResourcesWidget.qml | Controle existente agora explícito | Reativo inclusive depois de usar o botão do widget | Componente real e nova atribuição de binding |
| background.widgets.media.sizeMode | MediaWidget.qml | Disposições já suportadas selecionáveis na UI | 1x1, 1x2, 1x3, 2x2, 2x3; sem player é estado sem dados | Componente real após sinal de redimensionamento |
| background.widgets.media.showControls/showTitles/showLyrics | Declarados no esquema, sem consumo equivalente nesses nomes no MediaWidget examinado | Não expostos como novas capacidades | O botão de letras usa estado local próprio | Evitada promessa sem efeito comprovado |
| background.widgets.*.x/y/placementStrategy | AbstractBackgroundWidget.qml | Recuperar posição e desfazer geometria | Coordenadas compartilhadas; muda para manual e preserva conteúdo | Serviço real; conflito externo bloqueia undo |
| background.widgetsLocked | AbstractWidget.qml e widgets derivados | Bloqueio explícito na página Widgets | Não altera conteúdo nem ativação | Serviço/registro; arraste real pendente |
| background.screenList | background/WidgetsLoader.qml | Seletor compartilhado na página Widgets | Afeta o conjunto de widgets do desktop, não cada widget individual | UI isolada; bloqueio/monitores reais pendentes |

Os limites de sliders/spins novos são limites de interface, não uma migração dos
valores já gravados. Presets não são reescritos ao abrir as páginas. Mudanças passam
pelo Config existente; operações de preset bloqueiam os controles novos.

English: this is the evidence map for the first delivery, not an assertion that every
legacy configuration field is functional. Existing capabilities, newly exposed controls,
and newly implemented behavior are distinguished above. Real compositor checks remain separate.
