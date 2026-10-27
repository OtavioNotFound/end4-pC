# Primeira entrega — barra, dock e widgets

Branch local: feat/settings-usability-p0. Base da rodada: 8007031.
Esta entrega inicia o plano PERSONALIZATION_GROWTH_PLAN.md; não conclui o roteiro inteiro.

## Problemas confirmados e mudanças

1. **Inicialização:** FirstRunExperience usava Connections sem import QtQuick no commit
base. O log real fornecido pelo usuário confirmou a falha. A importação foi corrigida;
a qualificação QQ.Connections já presente no checkout foi preservada. O teste novo
carrega esse serviço real, com marcador de usuário existente e configuração temporária.
2. **Barra:** o editor do dashboard iniciava arraste no clique e dependia de botão direito
para remoção; a página tradicional tinha outro editor/catálogo. Agora as páginas reutilizam
DashboardBarLayoutCard: seleção, botões adicionar/mover/ordenar/remover, foco e ativação
por teclado e configurações suportadas do item no mesmo contexto. As regras e a edição
ficam em BarLayout.js/BarLayout.qml; IDs legados desconhecidos são preservados.
3. **Limitações escondidas:** Dynamic Island exige barra horizontal/centro exclusivo e
separador depende de grupos transparentes. Itens indisponíveis continuam no catálogo,
com explicação textual; a edição incompatível é rejeitada sem mudar as listas.
4. **Ajustes da barra:** quatro opções já consumidas pelo componente agora são explícitas:
área de revelação em px, reservar espaço ao revelar, revelar com Super e atraso em ms.
Os valores existentes não são alterados para ativar dependências.
5. **Dock:** ganhou destino próprio com os controles existentes, pesquisa de aplicativos,
fixar/desafixar e reordenação. Reusa TaskbarApps e o resolvedor de ícones existente.
IDs indisponíveis permanecem na lista. Ampliação lateral é identificada como indisponível,
sem apagar a preferência. A seleção de monitores é funcionalidade nova; ausência da
chave ou lista vazia mantém o comportamento de todos os monitores.
6. **Widgets:** o catálogo omitía customText, embora o loader e a página antiga já o
suportassem. Agora os 16 itens estão no catálogo. Configurar, ativar no desktop e mostrar
no menu são ações distintas. A primeira fatia oferece controles de relógio, clima,
recursos, texto e disposições de mídia, reaproveitando o catálogo/accessors existentes.
7. **Recursos:** opções novas permitem mostrar/ocultar CPU e memória e escolher o terceiro
cartão: automático, bateria, disco ou oculto. O padrão mantém os três cartões originais.
Há aviso se todas as medições forem ocultadas. Ausência de bateria não é apresentada
como bateria em zero: a escolha explícita de bateria mostra — sem dados.
8. **Estado após manipulação no desktop:** atribuições locais no botão de orientação de
recursos e no redimensionamento de mídia quebravam suas ligações ao JSON. Essas ligações
são restauradas após a interação, permitindo mudanças posteriores pela configuração.
9. **Recuperação limitada e segura:** desfazer a última edição de layout; recuperar e
desfazer a posição de um widget sem tocar no conteúdo. Alterações externas conflitantes
inviabilizam o desfazer. Operações novas respeitam o bloqueio durante aplicação de preset.
10. **Navegação e explicações:** atalhos diretos no dashboard e páginas Dock/Widgets na
navegação nativa, sem mudar settings.style. Descrições, unidades e traduções PT-BR/EN.
O seletor de monitores compartilhado mantém nomes desconectados e evita a seleção vazia
acidental, que no esquema significa todos os monitores.

O mapa de evidências e os consumidores estão em CAPABILITIES.md. O guia de uso é USER_GUIDE.md.

## Arquivos envolvidos

- Esquema: modules/common/Config.qml (apenas propriedades aditivas; defaults antigos mantidos).
- Serviços: BarLayout.js/.qml, DesktopWidgets.qml, TaskbarApps.qml, FirstRunExperience.qml,
SettingsHelp.qml, SettingsQuickControls.qml, SettingsMetadata.js e SettingsPages.qml.
- Configurações: DashboardBarLayoutCard.qml, DashboardBarWidgets.qml,
DashboardSettingsCatalog.qml, DashboardSettingsPage.qml, DashboardWidgetsCard.qml,
SettingsInlineControls.qml, SettingsScreenSelection.qml e pages/BarConfig.qml,
pages/DockConfig.qml, pages/WidgetsConfig.qml.
- Consumidores: dock/Dock.qml, background/widgets/resources/ResourcesWidget.qml e
background/widgets/media/MediaWidget.qml.
- Qualidade: tests/settings/runtime.py, test_runtime.py, test_search.py,
scripts/run_checks.py, translations/en_US.json, translations/pt_BR.json.
- Documentação: README.md, getting-started.md, development.md, plano e docs/personalization/.

## Testes e evidências

Comando: `python3 scripts/run_checks.py`.
Resultado final desta rodada: **100 testes passaram**, sem skips neste ambiente
(32 de ícones, 38 de presets, 30 de configurações); 25 JSONs válidos; sintaxe Python e
Bash validada; **91 QMLs** passaram no parser, sem reformatação automática.

Cobertura nova: serviço real de primeira execução; regras de layout; rejeição de
incompatibilidades; preservação de IDs desconhecidos; botões nativos com rótulos e clique;
spin/switch reais; desfazer com escopo e conflito; aplicativos fixados no serviço real;
seletor de monitores e fallback de presets antigos; página de widgets e preservação de
texto; recuperação de posição; combo mostrando valor atual e seleção nativa; componente
de recursos real com dimensões padrão 420×120; componente de mídia real depois de
redimensionamento. Textos de novas capacidades e metadados constam em PT-BR/EN.

Cenas offscreen usam Config, componentes e serviços específicos reais, com outras
integrações simuladas e HOME/XDG temporários. Tipos carregados apenas por URL são
verificados com imports explícitos no harness. Ausência de componente é falha do teste,
mesmo quando o timer geral ainda poderia emitir PASS.

Inspeção visual por capturas de cenas QML isoladas: editor da barra em 900×1000,
Dock e Widgets em 900×700. Foram corrigidos botões sem rótulo (buttonText no componente
nativo) e valor inicialmente vazio no combo. Limites dos botões da barra foram testados
em 600, 810 e 1100 px; a matriz de escalas/resoluções dos testes anteriores permanece.
Isso **não comprova equivalência visual da shell completa em Hyprland/GPU**.

## Riscos, compatibilidade e limites

Não foram iniciadas shells sobre as configurações pessoais, alterados autostart/atalhos,
instalados pacotes nem executado push. O backup local preexistente
services/FirstRunExperience.qml.bak foi preservado e não integra a implementação.

Os padrões gráficos originais de barra/dock foram preservados; suas opções existentes
passaram a ser acessíveis em outros contextos. A diferença padrão do widget de recursos
limita-se à tradução de rótulos; dimensões e os três cartões permanecem nos defaults.
As novas escolhas só mudam a composição mediante ação do usuário.

A seleção de monitores da dock é global; widgets ainda compartilham coordenadas e
background.screenList. O relógio no bloqueio conserva sua regra especial no loader.
As opções de tempo e clima compartilhadas têm esse alcance explicado. A recuperação
seleciona posicionamento manual; não muda o conteúdo do widget.

Não há garantia de desfazer efeitos externos de temas, gravações ou processos. Também
não foi implementado um undo genérico, restauração por categoria, restauração arbitrária
de opção, ou confirmação temporizada de mudanças de monitor/compositor.

## Pendências e próxima entrega

- Testar a shell completa em sessão Hyprland real, com configurações isoladas: iniciar,
barra nas quatro bordas, foco/teclado, fullscreen, área sensível, Super e reserva de espaço.
- Testar dock inferior/lateral, estilos float/hug, ampliação, prévias, apps reais,
monitores com escalas diferentes e desconectar/reconectar telas.
- Comparar composição original com presets existentes, em GPU, incluindo animações,
blur/Glassy, lockscreen, sidebar e diferentes escalas. Nenhuma certificação visual é inferida.
- Ampliar controles por item da barra, sobretudo acesso contextual aos overrides de estilo,
e oferecer reset seguro a partir do esquema autoritativo. O editor de estilo já existente
na própria barra não foi removido nem duplicado nesta entrega.
- Completar detalhes dos demais widgets, seletores de arquivos/prévias e diagnósticos de
dependências por widget. A página informa quando não possui controles específicos.
- Completar E4 (defaults/reversão abrangente) antes de mudanças mais arriscadas; E5
(wallpapers, aparência e resumo de presets) continua posterior às prioridades atuais.

English: this is the first incremental delivery, not completion of the growth roadmap.
It adds explicit bar actions and inline controls, a Dock page with app/monitor management,
and a Widgets page with separate visibility/menu settings and initial widget editors.
Resource metric choices are new; default geometry is preserved. Scoped undo and position
recovery reject conflicting changes. 100 automated tests and 91 QML parses pass; real
Hyprland, GPU and multi-monitor acceptance checks remain outstanding. No remote push.
