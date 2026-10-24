# Validação e pendências — 24/10/2026

Base: `cbe1aad`. Branch local: `fix/preset-resource-reliability`.
Runner: `python3 scripts/run_checks.py`.

## Executado

**70 testes passaram:** 32 existentes de temas de ícones e 38 novos de
presets/diagnóstico/runtime. Nenhum desses testes foi marcado como skipped
neste ambiente. Quickshell local 0.3.2, Qt 6, Python 3, jq, ImageMagick e Node.

Também passaram: 25 arquivos JSON do projeto, sintaxe dos scripts Python e
Bash, parsing dos 15 arquivos QML envolvidos e `git diff --check`.
O parsing usa `qmlformat --ignore-settings`, sem modificar/reformatar arquivos.
Isso não é lint semântico completo nem prova de renderização no compositor.

| Cenário | Evidência |
|---|---|
| PNG ausente, JPEG presente | Sugerido, aplicação bloqueada; reparo explícito cria backup |
| Dois candidatos de extensão | Reparo recusado; arquivo original inalterado |
| Lockscreen ausente | Erro separado; bloqueia antes do commit |
| Caminhos com espaços/URL local/tilde | Resolução e carregamento de source testados |
| Imagem corrompida | Decoder rejeita antes de aplicar |
| Caminho de outro usuário | Não procurado em Pictures; pacote legado relocaliza asset próprio |
| Persona/Maomao sintéticos | Seis alternâncias, configuração e glass preservados |
| Falha do switchwall | JSON restaurado byte a byte; saída em log privado |
| Processo retorna sucesso mas altera wallpaper/glass | Verificação rejeita e restaura JSON |
| Duas aplicações simultâneas | Lock serializa a execução inteira |
| Glass × transparência × automático/manual | Oito combinações no Quickshell offscreen real |
| Escrita QML ainda pendente | Flush confirmado antes do processo externo |
| Releitura/reinício | Segundo processo confirma toggle persistido |
| Próximo wallpaper em validação | Source anterior mantido até verificar o próximo |
| Pacote portátil/legado | Ida e volta, manifesto, hash e ZIP antigo |
| Basenames iguais, imagens diferentes | Arquivos distintos preservados |
| Avatar portátil | Diretório de avatar acompanha a imagem importada |
| Reimportação/preparo de upload repetidos | Importação não sobrescreve; preparo anterior recebe backup |
| ZIP malformado/traversal/JSON ambíguo/hash alterado | Importação recusada |
| Instalação sobre nome pessoal existente | Conteúdo pessoal preservado |
| XDG personalizado e blacklist | CLI save/export/import validada em ambiente temporário |
| Fallback de ícones | Função JS real testada com SVGs existentes e stub de tema |
| Paleta inválida | Função JS real mantém cores anteriores, sem atualização parcial |
| matugen/gerador Python falha | Script real com comandos stub; propaga erro e preserva SCSS |
| Relatório para issue | Teste garante ausência de caminhos, tokens, SSIDs e conteúdo de log |
| Recuperação de JSON corrompido/default explícito | Restaura e guarda bytes anteriores em backup |

As funções JS são extraídas dos próprios QMLs nos testes, com APIs do host
substituídas. Isso verifica a lógica, não o motor de temas real do desktop.
As imagens são fixtures geradas localmente; nenhum preset privado foi usado.

## Equivalência visual: ainda não certificada

Não foram alterados shaders, assets visuais, screenshots, medidas, fontes,
curvas de animação ou fórmulas originais de transparência. A resolução de
recursos e o fallback em caso de falha mudaram; há dica contextual em hover e
contorno de foco apenas ao navegar com teclado nos toggles existentes.

Essa revisão de código **não prova equivalência visual pixel a pixel**. O
ambiente de teste mínimo não carrega barra/dock/dashboard completos, compositor,
PAM, autostart, serviços pessoais nem integrações reais de temas.

### Matriz gráfica pendente

Executar em sessão de teste com HOME/configurações isoladas:

1. Base e fork: mesmo wallpaper válido, fontes, resolução, escala, preset e modo.
2. Comparar barra, dock, dashboard, widgets, sidebars e lockscreen; repetir com
   presets Persona/Maomao reais disponibilizados para teste pelo usuário.
3. Glass ligado/desligado × transparência ligada/desligada × automático/manual.
4. Alternar presets repetidamente; confirmar animações e toggle após reinício.
5. Remover/recuperar wallpaper e lockscreen separadamente; verificar fallback,
   aviso único, ausência de loops e recuperação em até 10 s do recurso inválido.
6. Testar vídeo/thumbnail, codecs, GPS opcional, ausência de cliphist, múltiplos
   monitores, escalas e temas sem ícones de distro.
7. Exercitar download/instalação de galeria em cache de teste, sem publicar nada.

## Limites e trabalho restante

- Não há rollback global de GTK/Qt, matugen, integrações externas ou processos
  de vídeo. JSON tem recuperação; esses efeitos precisam de isolamento adicional.
- O lock serializa aplicações deste fork; não impede gravações de scripts
  legados/editores externos. Evitar edição concorrente fora da shell.
- O doctor não valida todo o schema aninhado nem certifica compatibilidade de
  versões. GeoClue/portais são inspeção de instalação, não teste de serviço.
- Famílias de fontes da UI continuam excluídas dos presets pela blacklist.
- O serviço compartilhado cobre fontes de wallpaper/thumbnail/vidro/centralizado.
  Outros widgets e prévias mantêm seus fluxos; não há watcher completo para
  imagens válidas removidas depois da checagem.
- O modo offline não comprova disponibilidade de rede, hash de manifesto em
  downloads da galeria nem comportamento completo do GPU/shader.
- Caches únicos retidos ainda não têm coleta automática. Serviços legados
  ainda têm caminhos fixos fora da nova CLI de presets.
- Os guias partem de um ambiente illogical-impulse instalado; não há instalador
  completo e validado do ambiente base para uma máquina CachyOS limpa.
- A fase de auditoria e este ciclo de correções não representam aceite gráfico
  completo da definição de pronto da especificação.

Não houve push, PR, fork remoto, instalação de pacotes, reinício da sessão
pessoal nem execução de comandos de configuração contra os arquivos do usuário.

**English:** all listed automated checks passed locally. Visual equivalence,
real gallery downloads, compositor behavior, full version compatibility and
global theme rollback remain unverified. No remote publication or personal
configuration changes were performed.
