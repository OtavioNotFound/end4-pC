# Auditoria de usabilidade — Fase 2

Base: `046a182`. Branch de trabalho local: `feat/settings-usability-p0`.
Escopo: dashboard, páginas tradicionais, pesquisa/launcher, controles e serviços
associados. Nenhuma configuração pessoal ou sessão gráfica foi usada como fixture.
Esta é uma auditoria de código; impacto visual/comportamento no compositor deve
ser validado separadamente. O inventário completo está em
[UX_SETTINGS_INVENTORY.md](UX_SETTINGS_INVENTORY.md).

## Arquitetura existente e capacidades que devem ser preservadas

- Há três estilos: `default`, `minimal`, `dashboard`. `Settings.qml` monta o
  painel tradicional e `Dashboard.qml` abre a janela do dashboard.
- O dashboard tem seis grupos e 63 seções, com 344 cards no catálogo e 13
  atalhos hero. `SettingsQuickControls` e o catálogo fornecem acesso ao estado;
  não se deve criar outro adapter JSON para a interface.
- Páginas tradicionais têm opções adicionais de monitores, fontes, geração de
  cores, políticas AI/networking e autostart. Sua navegação e API `goTo()` já
  existem. O dashboard não deve substituir/remover essas páginas.
- Wallpapers já têm grid de miniaturas, navegação, prévia, seletor de arquivos,
  alvos desktop/lockscreen e sincronização. Não falta um seletor gráfico.
- Presets já têm prévia e resumo (barra, paleta, dock, relógio). Aplicação já
  valida assets, cria backup e restaura JSON após falha. Não duplicar o motor.
- Monitores já têm canvas, modos, escala, orientação, posições e verificação
  de capacidade HDR. HDR indisponível já é explicado: não é lacuna nova.
- A fase 1 já inclui `doctor.py`, relatório sanitizado, recuperação CLI,
  fallback de imagens/ícones, verificação de cliphist e algumas dicas de vidro.

## Problemas confirmados

As referências abaixo usam nomes de função/propriedade para continuar úteis
após mudanças de linhas. Prioridades seguem o plano de implementação.

| ID / prioridade | Evidência no código-base | Impacto | Solução proposta / arquivos |
|---|---|---|---|
| U01 P0 | `DashboardSettingsPage.matches()` exclui hero toggles sem `searchable`; Glassy UI só está no hero, não nas seções | A busca não encontra vidro, embora o card exista | Incluir atalhos e deduplicar por chave; página de dashboard e testes de busca |
| U02 P0 | Mesma função chama `isVisibleEntry`, que elimina `requires` ausente e condições como `dockmagnify` | Usuário não descobre por que a opção sumiu | Durante busca, manter resultados dependentes com razão e entrada desabilitada; preservar filtros de compositor |
| U03 P0 | Busca do dashboard usa título/seção/kw/chave; `SettingsSearchIndex.search` só rótulos/seções e não normaliza acentos | Descrições e sinônimos não participam; resultados divergem | Metadados compartilhados, normalização e regras de tokens comuns |
| U04 P0 | `SettingsSearchIndex.parsePage` conta `{}` dentro de strings/comentários e não inclui `ConfigRow` label lateral nem descrições | Indexação pode atribuir contexto errado; cobertura de nomes é incompleta | Scanner léxico limitado a propriedades estáticas, com fixtures de QML real e comentários/templates |
| U05 P0 | `scoreText` aceita página se qualquer token bater; não exige todos os tokens na busca de páginas | Resultados de páginas podem ignorar parte da pergunta | Aplicar a mesma regra de todos os tokens a páginas/opções |
| U06 P0 | `LauncherSearch`: `style === "dashboard" ? [] : SettingsSearchIndex.search(...)` | Busca de configurações desaparece no launcher no estilo dashboard | Reutilizar índice e roteamento existentes em todos os estilos |
| U07 P0 | Catálogo dashboard não tem Displays/Fonts/Color generation/Autostart; acesso tradicional passa por trocar `settings.style` | Funções avançadas e monitores são difíceis de alcançar | Atalhos nativos para páginas existentes, com retorno, sem mudar preferência persistida |
| U08 P0 | Dock/Dock style estão em Interface, barra em Bar, seletor de wallpaper em Interface e wallpaper em Desktop | Conteúdos relacionados ficam espalhados | Agrupar barra+dock, wallpaper+seletor; identificar aparência, mantendo chaves antigas |
| U09 P0 | `GlobalStates.dashboardGroup` contém rótulos traduzidos; comparação em `groupDefs`/seções é textual | Mudar idioma pode perder a categoria atual | IDs estáveis em memória e aliases para os rótulos anteriores; nenhum formato de preset muda |
| U10 P0 | Transparência manual no dashboard não usa `enabled` equivalente à página Interface; `Appearance.contentTransparency` usa piso de vidro e auto 0.9 | Controle parece ter efeito mesmo quando o cálculo usa outro valor | Explicar valor salvo versus efetivo; impedir edição manual enquanto automático, sem alterar valores/fórmulas |
| U11 P0 | `DashboardSliderCard` calcula `%` como `(current-from)/(to-from)`; transparência de fundo tem range 0..0.6 | Valor salvo 0.11 aparece como 18%, não 11% de transparência | Usar valor real em controles fracionários; preservar controles de outras unidades |
| U12 P0 | `DashboardSettingsPage`: `showPercent: percent !== false`, ignorando `control.usePercentTooltip`; raio de blur 1..64 não tem percent false | Pixels podem aparecer como porcentagem | Unidade/metadados explícitos, fallback para definição do controle e testes |
| U13 P0 | Rótulos `Earbang protection`, `Levenshtein search`, `Weeb`, `Polling interval (m)` sem explicações no dashboard | Termos técnicos/ambíguos para iniciantes | Renomear apresentação sem trocar chave; descrições, sinônimos, unidades e efeito |
| U14 P0 | Cards padrão têm valor/título, mas quase nenhum motivo de indisponibilidade; GPS usa opção persistida e `Weather.gpsActive` pode ser false | Switch selecionado não explica falha do serviço | Metadados de estado/capacidade, diagnóstico reutilizado e aviso contextual, sem inverter preferência |
| U15 P0 | `DashboardPresetDetail` marca `overwritten/exported/installed=true` logo após disparar sinal | Mostra sucesso antes de concluir e inclusive quando falha | Resultado assíncrono do serviço como fonte única do feedback |
| U16 P0 | Mesmo detalhe confirma Delete/Unshare em dois cliques, mas Overwrite não confirma; `Presets.save` chama `--save`, que sobrescreve colisão | Usuário pode perder preset salvo sem confirmação | Confirmar overwrite existente; novo nome na UI usa criação exclusiva sem mudar CLI legada |
| U17 P0 | `Settings.qml` e `DashboardContent` usam Tab para trocar páginas; cards têm cobertura desigual de foco | Navegação sequencial pelos controles conflita com atalhos de página | Reservar Ctrl+Tab para páginas, deixar Tab/Shift+Tab para foco; nomes acessíveis e feedback de foco |
| U18 P0 | Não há consumidor UI de `doctor.py`; erros da fase 1 aparecem em notificação/log/CLI | Falhas exigem terminal para diagnóstico completo | Ação nativa e painel de resultado com componentes existentes; executar o doctor, não reimplementar checks |
| U19 P0 | `FirstRunExperience.handleFirstRun()` sempre chama switchwall se o marcador first_run.txt faltar | Ausência do marcador pode substituir wallpaper de usuário existente | Aguardar Config.ready e preservar wallpaper configurado antes de abrir welcome existente |
| U20 P1 | Modelo de monitores aplica/salva imediatamente, sem countdown/reversão; `applyProc/saveProc` não expõem resultado UI | Mudança de modo pode deixar tela ilegível; falha de persistência pouco visível | Entrega própria: teste/reverter modo com confirmação temporizada e snapshot; não implementar reset genérico de monitores |
| U21 P1 | `Presets` não mantém identidade/hash do preset ativo nem diff; resumo do detalhe não é diff exato | Não informa alterações não salvas nem lista exata de campos alterados | Reutilizar blacklist/validação para preview/diff e undo de JSON; definir fronteira para efeitos externos |
| U22 P1 | `DashboardSelectCard` só mostra reset se o controle tiver `reset`; não há reset geral baseado no adapter | Recuperação de opção/categoria não é uniforme | Defaults vindos de Config; confirmação por categoria e undo limitado a opções locais seguras |
| U23 P1 | Wallpaper apply usa processo destacado e mantém `confirmedPath` antes de concluir | Seleção visual pode antecipar aplicação efetiva | Processar retorno e validar nova seleção com o mesmo serviço de recursos; preservar previews |
| U24 P2 | Já existem welcome.qml e marcador, mas não fluxo progressivo opcional de diagnóstico/preset/wallpaper | Wizard adicional duplicaria a primeira experiência | Evoluir welcome existente depois de estabilizar painel; pular etapas e consentimento explícito |

## Dependências, efeitos e situações de terminal

| Recurso | Evidência / estado atual | Ação |
|---|---|---|
| Glassy UI | `WallpaperResources` expõe source e erro; tooltip da fase 1 existe | Exibir aviso contextual e torná-lo pesquisável; não inverter toggle |
| Transparência automática | Fonte válida + `Appearance` usa fórmula para fundo e constante para conteúdo | Explicar exatamente essa semântica; não afirmar que todo valor é derivado do tema |
| Cores claro/escuro | QuickConfig possui sol/lua; pipeline switchwall/matugen pode alterar apps | Atalho direto à página existente; efeito identificado como geração de cores, não mero boolean |
| Histórico clipboard | Cliphist verifica disponibilidade; UI não usa esse estado nos controles relacionados | Explicar dependência e acesso ao diagnóstico |
| GPS | Weather já desativa runtime GPS inválido e usa cidade, mas preferência enableGPS continua true | Mostrar runtime indisponível e alternativa de cidade manual |
| Vídeo | ffmpeg/mpvpaper; doctor já verifica instalação | Reutilizar relatório e orientação, sem instalar pacotes |
| Monitores | hyprctl + scripts Lua + compositor; HDR já tem aviso | Reutilizar página e não prometer segurança de testes sem compositor |
| Animações Hyprland | Página tradicional mostra linha require obrigatória; dashboard só oferece seletor | Ligar ajuda/atalho à página existente para pré-requisito |
| Ícones/temas externos | SystemAppearance processos assíncronos; mudanças de app podem exigir reabrir app | Descrever alcance e não marcar tema aplicado só por preferência |
| Presets | Validação/backup já existentes; reparo e restauração ainda CLI | P0: diagnóstico e erro legível; P1: preview/undo gráfico transacional |

Não foi comprovada necessidade de reiniciar a shell para switches comuns de
layout/transparência. São bindings dinâmicos: não adicionar selo de reinício
indiscriminadamente. Dependência recém-instalada pode exigir nova detecção
(cliphist), e apps externos podem exigir reabertura. Atalhos de compositor,
modo de monitor e efeitos externos precisam de teste na sessão real.

## Riscos e compatibilidade

- Chaves persistidas, defaults, enums, blacklist de presets e fórmulas visuais
  permanecem. Renomear rótulos não autoriza renomear identificadores.
- Reorganização afeta apenas painel e aliases de navegação; funções avançadas
  continuam acessíveis por suas páginas existentes.
- Metadados de ajuda não podem se tornar um segundo schema/default store.
- Não considerar preferência persistida igual a sucesso de processo externo.
- Dados do doctor ficam locais; relatório exportável continua sanitizado.
- Sem redesign de barra/dock/widgets, sem novo editor de widgets e sem libs pesadas.
- Baseline automatizada: runner da fase 1; resultados novos e validação manual
  serão registrados em `UX_DELIVERY_REPORT.md`, sem alegar aceite visual.
