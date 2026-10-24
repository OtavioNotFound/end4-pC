# Entrega de UX — Fase 2, P0

Base: `046a182`. Branch **local**: `feat/settings-usability-p0`.
Não houve push nesta fase. O fork público continua na versão anterior até
uma nova autorização de publicação. Configurações pessoais não foram usadas
nos testes nem alteradas.

## 1. Problemas encontrados

[UX_AUDIT.md](UX_AUDIT.md) registra 29 achados, com evidências, impacto,
prioridade e riscos. O [inventário](UX_SETTINGS_INVENTORY.md) cobre as 63 seções,
344 cards do catálogo original e os rótulos estáticos de todas as páginas.
O [plano](UX_IMPLEMENTATION_PLAN.md) separa P0, P1 e P2.

Principais confirmações: busca excluindo Glassy UI e opções condicionais,
pesquisa desativada no launcher em modo dashboard, ausência de atalho de
monitores, categorias vinculadas a traduções, unidade incorreta nos sliders,
feedback de sucesso antes de processos terminarem, sobrescrita sem confirmação
e substituição do wallpaper quando o marcador de primeira execução faltava.

Não foram classificados como ausentes recursos que já existem: prévias de
wallpaper/preset, seletor gráfico, canvas de monitores, aviso de HDR, backend
de aplicação/backup de presets e doctor. Essas implementações foram reutilizadas.

## 2. Melhorias implementadas

### Encontrar e navegar

- Busca compartilhada entre dashboard e launcher: acentos, todos os termos,
  descrições, nomes antigos e sinônimos PT/EN. A correspondência fuzzy do
  projeto é reutilizada como fallback; não foi criada outra implementação fuzzy.
- Hero cards pesquisáveis e deduplicados; opções condicionais aparecem na busca
  com motivo de indisponibilidade. Recursos de outro compositor continuam filtrados.
- IDs de categoria estáveis; Aparência, Barra e dock, Desktop e widgets, Geral,
  Serviços e compositor atual. Dock agrupado com barra; seletor com wallpaper.
- Acessos a claro/escuro/cores, monitores, configurações completas e diagnóstico.
  Wallpapers e presets conservam as abas próprias já existentes.
- Páginas completas são abertas por navegação temporária, com retorno ao
  dashboard, sem mudar `settings.style` no JSON. Busca por seção também funciona.
- Tab/Shift+Tab ficam para foco; Ctrl+Tab/Ctrl+Shift+Tab trocam páginas.

### Entender e modificar

- Metadados de apresentação compartilhados, sem novo schema de configuração.
  Dicas explicam efeito, alcance, dependência e momento de aplicação dos
  controles comuns. Descrições longas têm largura limitada e quebra de linha.
- Transparência, Glassy UI e blur são diferenciados; valores manuais permanecem
  salvos quando automação manda no resultado. Fórmulas originais não mudam.
- Sliders manuais ficam indisponíveis enquanto automático está ativo; o motivo
  aparece no card e no tooltip. O launcher não oferece edição inline nesses casos.
- Transparência `0.11` é mostrada como **11%**, inclusive em tooltips; blur usa px
  e intervalos usam ms/s/min conforme o controle. Marcadores de referência
  existentes do slider são mantidos; não foram inventados novos defaults.
- Rótulos de proteção de volume, busca tolerante a erros e conteúdo de anime
  ficaram compreensíveis; nomes técnicos continuam pesquisáveis.
- Avisos de wallpaper ausente, GPS indisponível e cliphist ausente descrevem a
  situação sem trocar silenciosamente a preferência do usuário.
- Combos não selecionam falsamente a primeira opção quando falta o valor ativo.
- Confirmações de botões e controles alterados usam a ativação nativa por clique,
  que também atende teclado. Nomes/descrições acessíveis foram acrescentados.

### Diagnosticar e preservar

- “Verificar configuração” no dashboard e em Sobre nos estilos tradicional/mínimo.
  A tela chama **doctor.py**; não duplica validação de assets/dependências.
- Saída privada local inclui os caminhos necessários para diagnóstico, renderizados
  como texto simples. `--report` continua sanitizado; os modos são mutuamente exclusivos.
- Presets mostram sucesso somente após conclusão. Falhas não viram check verde.
- Sobrescrever exige confirmação nos detalhes e no popup antigo; salvar um novo
  nome pela UI usa criação exclusiva, inclusive sob concorrência. A CLI antiga
  `--save` continua permitindo sobrescrita explícita com backup.
- O texto de “salvar como” é mantido em caso de falha, em ambos os painéis.
- Ausência do marcador de primeira execução não substitui wallpaper existente.
- A UI deixa de zerar globalmente o debounce de Config; flush transacional e
  persistência da fase 1 permanecem.

### Layout responsivo

A renderização isolada identificou overflow do seletor de estilo em 900×600 e
em 1100×680 com PT-BR. O mesmo componente passa a ocupar uma linha inteira
abaixo de 1200 unidades lógicas e fica em Geral. Os controles frequentes
ganham precedência. Cores, formas, curvas e componentes nativos foram mantidos.

## 3. Arquivos modificados

| Área | Arquivos principais |
|---|---|
| Pesquisa | `SettingsSearch.js`, `SettingsMetadata.js`, `SettingsSearchIndex.qml`, `SettingsQuickControls.qml`, `LauncherSearch.qml`, `SearchItem.qml` |
| Navegação | `GlobalStates.qml`, `Settings.qml`, `SettingsContent.qml`, `Dashboard.qml`, `DashboardContent.qml`, `DashboardSettingsPage.qml`, `DashboardGroupRail.qml`, catálogo |
| Clareza | `SettingsHelp.qml`, `SettingsControlHelp.qml`, cards de controles, `ConfigSwitch.qml`, `ConfigSlider.qml`, tooltips e páginas General/Interface/Services |
| Diagnóstico | `doctor.py`, `SettingsDiagnostics.qml`, `DashboardDiagnosticsPage.qml`, `NoticeBox.qml`, página About |
| Presets | `Presets.qml`, `presets.sh`, detalhe/página de presets, `PresetPopup.qml`, Profile |
| Segurança da primeira execução | `FirstRunExperience.qml` |
| Testes/traduções | `tests/settings/`, runner e `en_US.json`/`pt_BR.json` |

A lista integral aparece no apêndice ao final. Não há alteração nesta fase em
`shell.qml`, defaults de `Config.qml`, fórmulas de `Appearance.qml`, shaders,
`WindowGlass.qml` ou componentes visuais da barra/dock fora do painel.

## 4. Testes executados

Comando, a partir do checkout (Fish ou Bash):

```sh
python3 scripts/run_checks.py
```

**88 testes passaram, sem skips neste ambiente:** 32 de temas de ícones,
38 da fase 1 e 18 de configurações. Também passaram validação de 25 JSONs,
sintaxe Python/Bash, parsing de **81 QMLs** e `git diff --check`.

| Evidência | Cobertura e limite |
|---|---|
| JS real e páginas reais | Busca por vidro, termos técnicos, dependências, comentários/strings QML, acentos, todos os termos e categorias antigas |
| Metadados | Unidades reais e existência das novas descrições PT/EN; não são uma segunda fonte de defaults |
| Quickshell offscreen | Dashboard real, leitura externa do JSON, valores manuais preservados, rotas Hyprland/Niri sem alterar estilo |
| Presets | Confirmação de dois cliques no componente real; falha do processo no serviço real; sucesso só após retorno |
| CLI | Colisão ao criar, criação concorrente, sobrescrita legada e backup |
| Doctor | Integração com painel e serviço reais; falha do checker não é conclusão; saída local privada e relatório sanitizado |
| Primeira execução | Função real com APIs simuladas; aguarda Config.ready e preserva wallpaper existente |
| Layout | Botões dentro do card e tooltip com quebra de linha em PT-BR: 900×600/escala 1, 1100×680/1, 1366×768/1.25 e 900×600/2 |

O harness usa HOME/XDG temporários, componentes reais e fontes incluídas;
serviços de desktop ficam inertes. O teste de presets usa script falso e
`notify-send` falso. Não inicia shell.qml, autostart, sessões de bloqueio,
instaladores, alterações de monitores nem downloads de galeria.

Foram inspecionadas capturas em renderização de software. Isso permitiu
reproduzir overflow e orientar a correção; **não comprova equivalência visual
em Hyprland**, renderização GPU, fontes externas ou todos os temas pessoais.

## 5. Problemas ainda existentes

- Restauração de defaults por categoria e undo seguro não foram implementados:
  são P1. Reset não pode incluir monitores, bloqueio ou comandos arbitrários.
- Não há diff exato nem indicador de alterações não salvas contra o preset ativo.
  Prévia/resumo existentes continuam; o novo feedback não pretende ser um diff.
- Backend de monitores ainda aplica imediatamente sem confirmação temporizada.
- Há duplicação preexistente de coleta de presets online em Profile; unificação
  requer teste dos dois formatos/fontes. Não foi adicionada outra implementação.
- Papéis de fontes/tema de apps e alguns processos externos ainda têm estado
  otimista até a próxima consulta. Resultado externo completo permanece P1.
- Novas dicas cobrem controles comuns e dependências confirmadas; não todas as
  344 opções. Índice captura rótulos estáticos de tipos conhecidos; listas
  dinâmicas são acessadas pelas páginas completas.
- Report do doctor é dirigido aos campos críticos, não valida todo schema ou
  saúde de GeoClue/D-Bus. Falta de dependência não autoriza instalação automática.
- Se o JSON impedir a própria shell de iniciar, o diagnóstico gráfico não fica
  disponível. A recuperação CLI da fase 1 continua necessária nesse caso.
- Rollback de presets continua limitado ao JSON, sem transação global de temas
  externos/processos de vídeo. Não editar a mesma configuração por outros meios
  durante a aplicação.
- A experiência inicial continua sendo o welcome existente; o wizard opcional
  completo foi apenas avaliado e planejado.

## 6. Validação manual necessária

Em sessão de teste isolada, não contra configurações pessoais sem backup:

1. Tab/Shift+Tab, Ctrl+Tab, Space/Enter e Escape nos três estilos; foco após voltar
   de páginas completas e diagnóstico; leitores de tela, sem depender só de hover.
2. PT/EN com fontes reais, escalas de monitores e janela pequena; checar elipses,
   tooltips, navegação e buscas com palavras usadas por iniciantes.
3. Glassy UI × transparência × auto/manual, efeitos e animações da barra/dock,
   troca real de wallpaper/preset e reinício da shell.
4. Abrir páginas de monitores sem alterar modo; mudanças de modo/escala/HDR
   somente em ambiente preparado para recuperação, pois o backend ainda é imediato.
5. Temas GTK/Qt/ícones e aplicações externas: sucesso/falha e necessidade de reabrir.
6. Ausência real de cliphist/GPS/vídeo e comportamento das alternativas descritas.
7. Download e instalação reais de presets em cache isolado; comparar dados
   salvos antes/depois, sem publicar nada.

## 7. Próximas melhorias recomendadas

1. Validar esta entrega em Hyprland antes de certificar aparência ou publicar.
2. P1: transação gráfica de monitores com teste/confirmar/reverter.
3. P1: diff/preview e undo de presets reaproveitando backend/blacklist/snapshots.
4. P1: defaults autoritativos do adapter, reset por opção/categoria e undo limitado.
5. P1: confirmar resultados de wallpaper/temas externos e unificar galeria legada.
6. P2: evoluir welcome existente, opcional e sem sobrescrever preferências.

**English:** P0 improves settings discovery, explanations, native navigation,
dependency feedback and truthful preset completion. Tests are isolated;
compositor validation, P1 recovery features and P2 onboarding remain pending.
This phase was not pushed to GitHub.

## Apêndice — lista integral de arquivos desta fase

- `GlobalStates.qml`
- `README.md`
- `docs/UX_AUDIT.md`
- `docs/UX_DELIVERY_REPORT.md`
- `docs/UX_IMPLEMENTATION_PLAN.md`
- `docs/UX_SETTINGS_INVENTORY.md`
- `docs/development.md`
- `docs/presets.md`
- `docs/troubleshooting.md`
- `modules/common/widgets/ConfigSlider.qml`
- `modules/common/widgets/ConfigSwitch.qml`
- `modules/common/widgets/NoticeBox.qml`
- `modules/common/widgets/PresetPopup.qml`
- `modules/common/widgets/StyledToolTip.qml`
- `modules/common/widgets/StyledToolTipContent.qml`
- `modules/ii/overview/SearchItem.qml`
- `modules/ii/settings/Dashboard.qml`
- `modules/ii/settings/DashboardActionCard.qml`
- `modules/ii/settings/DashboardBarPositionCard.qml`
- `modules/ii/settings/DashboardComboCard.qml`
- `modules/ii/settings/DashboardContent.qml`
- `modules/ii/settings/DashboardDiagnosticsPage.qml`
- `modules/ii/settings/DashboardDurationCard.qml`
- `modules/ii/settings/DashboardGroupRail.qml`
- `modules/ii/settings/DashboardPaletteCard.qml`
- `modules/ii/settings/DashboardPresetDetail.qml`
- `modules/ii/settings/DashboardPresetsPage.qml`
- `modules/ii/settings/DashboardSchemeCard.qml`
- `modules/ii/settings/DashboardSelectCard.qml`
- `modules/ii/settings/DashboardSettingsCatalog.qml`
- `modules/ii/settings/DashboardSettingsPage.qml`
- `modules/ii/settings/DashboardSliderCard.qml`
- `modules/ii/settings/DashboardSpinCard.qml`
- `modules/ii/settings/DashboardStyleCard.qml`
- `modules/ii/settings/DashboardTextCard.qml`
- `modules/ii/settings/DashboardToggleCard.qml`
- `modules/ii/settings/DashboardWidgetsCard.qml`
- `modules/ii/settings/Settings.qml`
- `modules/ii/settings/SettingsContent.qml`
- `modules/ii/settings/SettingsControlHelp.qml`
- `modules/ii/settings/pages/About.qml`
- `modules/ii/settings/pages/GeneralConfig.qml`
- `modules/ii/settings/pages/InterfaceConfig.qml`
- `modules/ii/settings/pages/Profile.qml`
- `modules/ii/settings/pages/ServicesConfig.qml`
- `scripts/doctor.py`
- `scripts/presets.sh`
- `scripts/run_checks.py`
- `services/FirstRunExperience.qml`
- `services/HyprlandOptions.qml`
- `services/LauncherSearch.qml`
- `services/Presets.qml`
- `services/SettingsDiagnostics.qml`
- `services/SettingsHelp.qml`
- `services/SettingsMetadata.js`
- `services/SettingsQuickControls.qml`
- `services/SettingsSearch.js`
- `services/SettingsSearchIndex.qml`
- `tests/settings/runtime.py`
- `tests/settings/test_backend.py`
- `tests/settings/test_runtime.py`
- `tests/settings/test_search.py`
- `translations/en_US.json`
- `translations/pt_BR.json`
