# Plano de crescimento — personalização explícita

Status: planejamento, sem implementação das entregas abaixo.
Prioridade definida pelo usuário: barra, dock e widgets; aparência/wallpaper depois.
Este plano complementa UX_IMPLEMENTATION_PLAN.md e substitui sua ordem de evolução
para a próxima etapa. A implementação P0 anterior não equivale às entregas deste plano.

## 1. Resultado esperado e limites

Um iniciante deve montar sua barra, escolher como a dock funciona e configurar seus
widgets sem editar JSON, conhecer IDs internos ou descobrir menus por tentativa.
Mais possibilidades úteis e visíveis, além de pesquisa e reorganização.
A shell mantém cores, componentes, curvas, animações e valores padrão originais.
Mudanças visuais acontecem somente quando escolhidas pelo usuário.

Sem novo editor livre de widgets, plugins arbitrários, duplicação dos serviços de
configuração, migração destrutiva, instalação automática ou push sem autorização.
Não expor parâmetros sem efeito comprovado no componente consumidor.

## 2. Evidências verificadas no checkout

| Área | Base existente | Consequência para o plano |
|---|---|---|
| Barra | Config.qml: bar.layouts, autoHide, cornerStyle, screenList e configurações por item | Expor e completar o fluxo existente, preservando IDs e listas |
| Catálogo da barra | DashboardBarWidgets.qml contém 24 itens | Não prometer 24 widgets novos; dar acesso às opções dos existentes |
| Editor da barra | DashboardBarLayoutCard.qml já move itens entre três regiões e restringe duplicatas | Reutilizar editor e regras; adicionar alternativa por teclado e painel do item |
| Restrições | canExist/canPlace restringem Dynamic Island e divisor | Mostrar motivo; não remover ou converter layouts antigos silenciosamente |
| Estilo por item | bar/BarGroup.qml consome bar.widgetStyles | Tornar o estilo acessível no contexto do item, preservando overrides |
| Dock | Config.qml: dock; InterfaceConfig.qml já tem muitos controles | Criar destino próprio e um fluxo completo, sem chamar controles antigos de novidade |
| Monitores da dock | dock/Dock.qml cria instâncias para Quickshell.screens | Escolha de monitor exige função nova; não existe apenas um controle escondido |
| Widgets desktop | DesktopWidgets.qml lista 15; DashboardWidgetsCard.qml liga/desliga e favorita | Separar ações Ativar, Configurar e Mostrar no menu |
| Texto personalizado | WidgetsLoader.qml carrega customText e BackgroundConfig.qml o configura, mas DesktopWidgets.catalog não o lista | Integrar o item já existente; validar consistência entre catálogo, carregador e esquema |
| Posição dos widgets | Config.qml guarda x/y/z e placementStrategy; widgetCanvas tem infraestrutura própria | Reutilizar manipulação existente e oferecer reposicionar/recuperar pela interface |
| Monitores desktop | WidgetsLoader.qml usa background.screenList e trata relógio no bloqueio especialmente | Explicar alcance compartilhado; não prometer configuração por widget/monitor sem backend |
| Tamanho da barra | Bar.qml/BarGroup.qml usam Appearance.sizes | Auditar cadeia de tamanhos antes de introduzir controle; não reduzir tudo com scale |

Arquivos referidos são relativos à raiz deste repositório. A presença de uma chave
não comprova que seu efeito funciona em todas as orientações; essa validação é parte
de cada entrega. Os controles atuais são base de reaproveitamento, não bugs presumidos.

## 3. Navegação proposta

Destinos diretos e visíveis: **Barra**, **Dock**, **Widgets**. Continuam dentro do
painel nativo, com pesquisa compartilhada e links das páginas antigas.
Não oferecer dois editores independentes para a mesma configuração.

- Barra: posição e monitores; itens e ordem; comportamento; estilo.
- Dock: posição e monitores; aplicativos; comportamento; tamanho e aparência.
- Widgets: catálogo; configuração do selecionado; organização no desktop.

Controles frequentes aparecem diretamente. Avançado fica limitado a expressões,
IDs e ajustes raros; opções usuais não devem depender de expandir vários grupos.
O catálogo de widgets desktop é distinto dos itens da barra, com nomes explícitos.

## 4. Contrato de cada controle

Cada controle informa nome compreensível, resultado, valor atual e unidade; oferece
restaurar padrão quando houver padrão autoritativo seguro. Dependências indisponíveis
mostram motivo e solução prática. Mudanças imediatas dizem “Aplicado na hora”; mudanças
com recriação/reinício identificam o alcance real. Tooltips complementam, não escondem
informações essenciais. Traduções PT-BR e inglês fazem parte de cada entrega.

Estados “ativado”, “sem dados”, “dependência ausente” e “erro” são distintos. Um widget
habilitado sem música não deve parecer desligado. Não prometer saúde de um serviço
somente porque seu executável existe.

## 5. Entregas incrementais

### E0 — Base executável e mapa de capacidades (bloqueante)

Resolver a falha de carregamento FirstRunExperience/Connections relatada pelo usuário,
validar o serviço real e registrar limites do harness com serviços simulados.
Produzir matriz chave → consumidor → controle existente → efeito → dependência → teste
para barra, dock e widgets, incluindo controles atuais antes de propor novos.

Arquivos: services/FirstRunExperience.qml, tests/settings/, Config.qml,
Appearance.qml, SettingsMetadata.js e os componentes consumidores.
Aceite: carregamento do serviço real em ambiente isolado; nenhum resultado de teste
isolado apresentado como prova de inicialização completa no Hyprland.

### E1 — Barra: montar e configurar (primeira entrega funcional)

- Abrir Barra diretamente; posição/orientação e monitores detectados visíveis.
- Reutilizar as três regiões do editor: esquerda/centro/direita ou topo/centro/base.
- Cada item oferece Adicionar, Configurar, Remover e Mover; arrastar é opcional.
- Botões mover antes/depois e trocar região funcionam por teclado.
- Selecionar item abre suas opções específicas no mesmo contexto.
- Catálogo mostra descrição, posição atual e motivo de indisponibilidade.
- Expor comportamento de ocultação, área de revelação e uso de Super com unidades.
- Disponibilizar estilo por item onde BarGroup já suporta, sem alterar estilo global.
- Prévia estrutural discreta; não criar segunda barra com serviços ativos para prévia.

Começar por relógio, workspaces, recursos, mídia, bandeja e atalhos. Os demais itens
permanecem disponíveis; os controles de cada um entram conforme a matriz comprovar.
Não permitir divisor/Island incompatível sem explicar; layouts legados desconhecidos
são preservados e sinalizados. A edição não apaga itens que o catálogo não reconhece.

Arquivos: DashboardBarLayoutCard.qml, DashboardBarWidgets.qml, BarConfig.qml,
DashboardSettingsPage.qml, SettingsPages.qml, BarGroup.qml, SettingsMetadata.js.
Aceite: adicionar item, configurar, mudar região/ordem, remover e restaurar layout sem
JSON; nenhum desaparecimento silencioso ao mudar orientação; persistência após reload.

### E2 — Dock: controle completo e aplicativos

- Página própria com controles existentes de posição, fundo, bordas, raio, ícones,
espaçamento, ampliação, prévias, botões e mídia.
- Explicar “manter visível ao iniciar”, revelação ao passar o mouse e comportamento
em workspace vazio/fullscreen, com base na lógica real.
- Lista de aplicativos fixados com nome/ícone: adicionar pelo catálogo de apps,
remover e reordenar. Preservar IDs .desktop sem exigir digitação.
- Mostrar entradas indisponíveis sem removê-las; manter regras regex no avançado.
- **Função nova:** seleção de monitores da dock. Esquema aditivo; ausência da chave
mantém todos os monitores. Monitor desconectado permanece salvo e sinalizado.
- Tamanho mostra o efeito real; validar relação entre height, iconSize e ampliação.

Arquivos: InterfaceConfig.qml, dock/Dock.qml, DockActiveApps.qml, Config.qml,
componente DockStyle localizado no inventário E0, registro de páginas e pesquisa.
Aceite: administrar aplicativos e comportamento pela UI, orientação lateral e inferior
sem corte de ícones; desconectar/reconectar monitor sem perder preferência.

### E3 — Widgets: catálogo configurável e explícito

- Catálogo existente ganha ações separadas Ativar e Configurar; favoritos significam
“Mostrar no menu do desktop”, com rótulo explícito.
- Integrar Texto personalizado já suportado, sem inventar outro widget.
- Detalhe do widget contém prévia leve, opções suportadas, dependências e estado.
- Primeira fatia: relógio (estilos e data), clima (cidade/unidades/localização), recursos
(métricas), mídia (estado sem player) e texto personalizado (conteúdo/fonte/cor).
- Próximas fatias: calendário/fusos; imagens/stickers com seletor e erro de caminho;
visualizador com estilos/sensibilidade; acesso às opções já existentes dos demais.
- Tamanho somente onde o widget oferece variantes/tamanho real. Não prometer escala
universal que distorce texto e áreas de interação.
- Acesso explícito a bloquear/desbloquear posições e “Trazer para a área visível”.
Reutilizar canvas; recuperação afeta geometria, nunca conteúdo de notas/tarefas/imagens.
- Mostrar monitores do desktop como configuração compartilhada, sem simular seleção
independente por widget. Seleção individual é expansão posterior.

Arquivos: DesktopWidgets.qml, DashboardWidgetsCard.qml, BackgroundConfig.qml,
background/WidgetsLoader.qml, background/widgets/, widgets/widgetCanvas/.
Aceite: habilitar, entender e configurar os widgets da primeira fatia sem JSON; preservar
conteúdo ao mover/desativar/restaurar estilo; catálogo e loader consistentes.

### E4 — Experimentação segura (base acompanha E1; conclusão após E3)

- Restaurar padrão por opção, layout e seção; confirmação mostra exatamente o alcance.
- Desfazer a última alteração segura da seção, com snapshot limitado às chaves tocadas.
- Operações compostas usam transação/backup existentes; sem segunda camada de persistência.
- Detectar alteração externa antes de desfazer: não sobrescrever silenciosamente.
- Padrões vêm do esquema original; não manter cópia divergente em metadados.
- Dados pessoais e listas criadas pelo usuário não entram em reset genérico.
- Mudanças que podem esconder controles recebem confirmação com reversão temporizada
quando for tecnicamente segura; acesso às configurações não depende só da barra/dock.

Arquivos: Config.qml (API existente a reutilizar), SettingsQuickControls.qml,
novo adaptador pequeno de recuperação se necessário; infraestrutura de backups existente.
Aceite: reset e undo só afetam o escopo anunciado, preservam chaves desconhecidas e
resistem a falha de gravação e edição externa. Sem promessa de desfazer efeitos externos.

### E5 — Acabamento: aparência, wallpapers e presets

Depois dos fluxos prioritários: transparência/Glassy explícitos; seleção e prévia de
wallpaper; resumo de alterações do preset; salvar composição como novo preset.
Reutilizar validação, backup, diagnóstico e operações assíncronas já existentes.
Assistente inicial, perfis por monitor, múltiplas instâncias do mesmo widget e novos
tipos de widgets ficam fora desta rodada. Não bloquear E1–E3 por essas expansões.

## 6. Implementação e compatibilidade

Separar metadados de apresentação das chaves persistidas. Reusar catálogo, serviços e
componentes nativos; extrair controles compartilhados das páginas antigas conforme
necessário. Novos nomes visíveis não renomeiam IDs de widget nem chaves de presets.
Novas propriedades têm fallback ao comportamento anterior; nenhum reset na abertura.
Habilitar recuperação básica antes de expor mudanças compostas. Commits pequenos por
fluxo, documentação e teste; sem reformatar QML fora do escopo.

## 7. Verificação e critérios de qualidade

Automatizados: round-trip de presets antigos/chaves desconhecidas; regras de layout;
ordem e duplicatas permitidas; opções por item; IDs de apps; fallback de monitor;
undo/reset com edição concorrente; reload externo; PT/EN; teclado e foco em cenas QML.
Testar consumidores reais por fatia, além de parser e serviços simulados. Acrescentar
smoke de importação dos serviços reais para evitar repetir a regressão Connections.

Sessão Hyprland real, registrada separadamente: iniciar shell completa; top/bottom e
vertical; todas as posições da dock; fullscreen; reserva de espaço; autohide; atalhos;
aplicativos fixados/em execução; DPI 1/1,25/2; 900×600 e resoluções maiores; dois monitores,
hotplug e recuperação de widget fora da tela; GPU/blur/animações e ausência de regressão
nos padrões originais. Não iniciar a shell real sobre a configuração pessoal como teste.

Aceite prático com usuário iniciante: montar barra com relógio/recursos/mídia, mudar
ordem, configurar workspaces, fixar app na dock, configurar clima e relógio desktop,
recuperar posição e desfazer sem terminal/JSON. Registrar passos, dúvidas e resultado;
o sucesso não é inferido somente de testes unitários.

## 8. Riscos e decisões já tomadas

- Barra cheia: validar overflow/responsividade antes de oferecer mais itens.
- Orientações e estilos não têm capacidades idênticas; explicar limitações em contexto.
- Dock e widgets podem compartilhar aparência; identificar alcance antes de editar.
- Geometria global dos widgets e monitores com escalas distintas exigem validação real.
- Prévia não pode disparar rede, áudio, autostart ou escrita na configuração ativa.
- Dados sensíveis de widgets não aparecem em relatórios públicos/screenshots automáticos.
- Dependências opcionais não são instaladas nem widgets ativados automaticamente.
- Mudanças pessoais e correções locais anteriores são preservadas; não entram neste plano
como funcionalidades concluídas. Publicação remota exige autorização específica.

Ordem final: E0 → E1 com recuperação básica → E2 → E3 em fatias → concluir E4 → E5.
Cada entrega precisa ter controles funcionais e teste do efeito; busca e descrições
isoladas não satisfazem o critério de personalização.
