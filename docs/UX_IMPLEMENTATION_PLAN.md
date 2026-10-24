# Plano incremental de UX — Fase 2

Base: `046a182`; auditoria: [UX_AUDIT.md](UX_AUDIT.md).
Esta fase implementa **P0**. P1/P2 são entregas futuras, não funcionalidades
implicitamente concluídas. Sem push autorizado nesta fase.

## P0.1 — Índice e metadados compartilhados

Arquivos: `SettingsSearchIndex.qml`, utilitário JS puro, metadados de ajuda,
`DashboardSettingsPage.qml`, `LauncherSearch.qml` e testes.

- Normalizar acentos/espaços/pontuação; exigir todos os tokens.
- Indexar rótulos/descrições/sinônimos, incluindo originais técnicos.
- Corrigir scanner de rótulos sem contar chaves em strings/comentários.
- Incluir hero cards, sem duplicar controles por chave.
- Mostrar resultados condicionais com explicação; filtrar incompatibilidade
  de compositor, sem habilitar recurso automaticamente.
- Mesmo índice do launcher em todos os estilos, roteando às páginas existentes.

Aceite: vidro/glass, transparência, dock, monitor/resolução, fontes e clima
são encontráveis em português/inglês. Texto parcial não produz página que
ignore outros tokens. Fixtures reais medem cobertura do índice.

## P0.2 — Navegação e funções frequentes

Arquivos: dashboard/catalog/rail, `Settings.qml`, `SettingsContent.qml`,
`GlobalStates.qml` e um card de ação baseado em DashboardCard/RippleButton.

- IDs de categoria independentes da tradução; aliases antigos aceitos.
- Agrupar barra e dock, wallpaper e seletor; nome claro de aparência.
- Atalhos nativos para wallpaper, presets, claro/escuro, monitores e configurações
  completas. Abrir componentes existentes, com retorno ao dashboard.
- Não trocar `Config.options.settings.style` ao abrir um atalho avançado.
- Tab navega foco; Ctrl+Tab mantém troca de páginas. Preservar Escape e busca.

Aceite: monitor e opções não representadas por cards ficam a um clique do
atalho; todas as páginas antigas continuam disponíveis; mudança de idioma
não invalida a categoria selecionada. Layout, formas e animações dos cards
continuam os componentes nativos.

## P0.3 — Clareza, dependências e unidades

Arquivos: metadados compartilhados, cards toggle/slider/spin/select/combo/text,
`DashboardSettingsCatalog.qml`, páginas tradicionais quando necessário,
`translations/en_US.json` e `pt_BR.json`.

- Ajuda contextual com descrição, efeito e dependência; usar StyledToolTip e
  texto de apoio existente, sem expandir todos os cards indiscriminadamente.
- Diferenciar wallpaper/vidro/blur/transparência e explicar valores salvos.
- Desabilitar sliders manuais enquanto o modo automático manda no resultado,
  preservando seus valores. Não mudar fórmula nem limpar opções dependentes.
- Exibir transparência fracionária como valor ×100, não posição no range;
  respeitar unidades declaradas pelo controle; adicionar unidades nos spins
  críticos. Usar defaults numéricos já existentes como referência, sem um
  novo sistema de reset nesta entrega.
- Termos claros de apresentação com sinônimos técnicos mantidos na busca.
- Avisos de runtime/dependência com alternativa prática; sem instalar pacotes.

Aceite: 0.11 vira 11%, blur é px, polling é min/ms/s conforme o campo. Um
controle inativo explica como habilitá-lo; navegar/buscar não altera JSON.

## P0.4 — Diagnóstico e feedback verdadeiro

Arquivos: serviço fino que chama `doctor.py`, card/painel nativo de diagnóstico,
`Presets.qml`, `DashboardPresetDetail.qml`, `presets.sh` e testes.

- Executar o doctor existente e mostrar resultado pela UI, em estados
  verificando/concluído/erro. Não duplicar regras do Python.
- Sucesso de exportar/instalar/sobrescrever só após resultado do processo.
- Confirmar overwrite com padrão de dois cliques já usado para Delete.
- Salvar como novo via UI não sobrescreve colisão, inclusive se o modelo de
  arquivos estiver atrasado; preservar comportamento da CLI antiga explícita.
- Evitar sobrescrita de wallpaper em first-run de usuário com config existente.

Aceite: erro não vira check verde; arquivos/presets pessoais não são apagados;
diagnóstico é somente leitura; ausência de marcador não muda wallpaper existente.

## Validação por entrega

- Testes JS das funções reais, fixtures de páginas e resultados de pesquisa.
- Quickshell offscreen com HOME/XDG temporários, Directories stub e componentes
  reais para bindings, leitura externa e navegação que não modifica preferência.
- Testes de subprocessos com comandos falsos/temporários, incluindo falha de
  preset, colisão ao salvar e diagnóstico sanitizado.
- Runner da fase 1: presets antigos, import/export, persistência, rollback,
  cores, JSON/Python/Bash e parsing QML dos arquivos alterados.
- Renderização em sessão Hyprland: 900×600, 1100×680, 1366×768, escala 1/1.25/2;
  teclado, textos PT/EN, tooltip sem corte, busca, monitores e efeitos externos.
  Registrar como **pendente** se não executada; unitários não comprovam visual.

## P1 — Próximas entregas

1. Preview/diff exato de presets usando blacklist/validador atuais; estado
   alterado em relação ao último preset; undo com fronteira explícita de JSON.
2. Restaurar uma opção/categoria a partir do adapter/defaults real, com snapshot,
   confirmação e undo seguro. Nunca incluir monitores/segurança nesse reset genérico.
3. Monitores: aplicar para teste, confirmar ou reverter por timeout e persistir
   somente após confirmação; exibir falha do backend.
4. Wallpaper: resultado confirmado de aplicação, validação assíncrona no seletor
   e indicação de uso em presets; manter preview existente.
5. Resultado de temas/ícones externos refletido após retorno dos processos.

## P2 — Primeira experiência e conveniência

Evoluir welcome.qml/FirstRunExperience existentes, não criar um segundo wizard.
Opt-in, pular etapas, retomar depois, preservar configurações e pedir consentimento
antes de aplicar wallpaper/preset. Integrar páginas/diagnóstico existentes.
Viável tecnicamente; não prioritário sobre o painel atual.

## Estado desta entrega

P0.1–P0.4 implementados no escopo descrito, com resultados e limites em
[UX_DELIVERY_REPORT.md](UX_DELIVERY_REPORT.md). O aceite de compositor/visual
continua separado e pendente. P1/P2 não estão incluídos no status de conclusão.
