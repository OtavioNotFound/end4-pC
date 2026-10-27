# Desenvolvimento / Development

## Organização

- `shell.qml`: entrada, serviços e carregamento da família de painéis.
- `modules/common/Config.qml`: adapter tipado do JSON ativo; debounce de 50 ms.
- `modules/common/Appearance.qml`: paleta, fontes, tamanhos e transparência.
- `modules/ii/`: componentes visuais originais.
- `services/Presets*.qml`: interface de ações locais e galeria.
- `scripts/presets.sh`: CLI compatível e blacklist central existente.
- `scripts/preset_resources.py`: campos de assets conhecidos, diagnóstico,
  reparo explícito e persistência atômica.
- `scripts/preset_apply.py`: lock entre aplicações, snapshot, commit e verificação.
- `scripts/preset_bundle.py`: importação/exportação com staging e manifesto aditivo.
- `services/WallpaperResources.qml`: validação compartilhada para wallpaper/vidro.
- `scripts/doctor.py`: diagnóstico somente leitura e relatório por allowlist.

Leia [a auditoria](audit.md) antes de alterar esses fluxos. Não reescreva o layout,
shaders, animações ou fórmulas de transparência para corrigir recursos inválidos.
Mantenha GPL v3 e créditos. Não use presets privados como fixtures.

## Executar verificações

Na pasta do checkout, Fish ou Bash:

```sh
python3 scripts/run_checks.py
```

Requer Python 3, Bash, jq e ImageMagick. Testes de QML em modo offscreen usam
`qs` se disponível; testes de funções JavaScript usam Node quando disponível.
Sem essas ferramentas, os respectivos testes são marcados como skipped; isso
deve ser informado na entrega. O parser QML usa `qmlformat` do Qt 6 se presente,
sem `--inplace`, portanto não reformata o código. Também verifica JSON,
sintaxe Python/Bash e whitespace de mudanças no Git.

Comandos individuais:

```sh
python3 -m unittest discover -s tests/icon_theme_manager -v
python3 -m unittest discover -s tests/presets -v
python3 -m unittest discover -s tests/settings -v
```

Os testes usam diretórios temporários. A shell mínima de teste copia os
componentes reais de configuração/aparência e substitui `Directories`; não
carrega `shell.qml`, autostart, limpeza de caches, rede ou serviços do desktop.
Os testes de `switchwall.sh` substituem comandos do sistema por stubs e usam
HOME/XDG temporários. Testes de aplicação substituem a integração de cores,
além de testar separadamente a propagação de falhas do script original.

Não foi criada CI remota: não havia workflow existente. O runner pode ser usado
em CI futura, com a matriz gráfica separada de verificações sem compositor.

## Convenções e limites

Adicione teste que reproduza o problema antes da correção. Use arrays de
argumentos em processos, arquivo temporário no diretório de destino para
`os.replace`, backup privado e erro explícito. Nunca resolva um basename
ambíguo por ordem de diretório. Não registre configuração bruta em relatórios.

O lock de presets não é compartilhado por todos os scripts históricos. Não
prometa transação de temas/processos externos. `Config.beginPresetUpdate()`
descarrega escrita pendente e bloqueia timers; `endPresetUpdate()` relê disco
antes de liberar escrita. Teste alterações rápidas para evitar sobrescrita.

`qmllint` isolado não resolve automaticamente todos os imports `qs.*` gerados
pelo Quickshell; não trate todos os warnings de import como defeitos novos.
O parser de formatter com as opções upstream provoca falha da ferramenta local
em alguns arquivos; `--ignore-settings` é usado na validação sem alterar a
configuração do projeto. O arquivo legado `LauncherSearchResult.qml` também
falha no formatter antes das mudanças; não está no escopo desta correção.

## Verificação visual e contribuição

Siga [a matriz pendente](validation.md). Compare a base `cbe1aad` e a branch do
fork com os mesmos presets/monitores/fontes, cada versão em configuração
isolada. Não rode as duas contra o mesmo arquivo ativo. Capturas precisam
incluir barra, dock, dashboard, widgets, sidebars, lockscreen e transições.

O fork público é [OtavioNotFound/end4-pC](https://github.com/OtavioNotFound/end4-pC),
publicado após autorização explícita do usuário. Sua branch padrão é
`fix/preset-resource-reliability`. No checkout de desenvolvimento, `fork` aponta
para esse repositório e `origin` permanece apontando para o projeto de referência;
confira `git remote -v` antes de publicar. Não foi aberto PR no upstream. Consulte
`git log --oneline` para revisar os commits e `git diff cbe1aad..HEAD` para o diff.
Para descartar a implantação, pare a instância, restaure o snapshot e execute
a versão anterior; não é necessário apagar esta branch nem usar reset destrutivo.

**English:** use `python3 scripts/run_checks.py`. Fixtures and runtime stubs
are isolated from personal configuration. Headless checks do not replace the
graphical acceptance matrix. Publication to the linked fork was explicitly authorized.

## Personalização: barra, dock e widgets

Consulte [o mapa de capacidades](personalization/CAPABILITIES.md),
[o relatório incremental](personalization/DELIVERY_1.md) e
[o guia PT/EN](personalization/USER_GUIDE.md). O editor de barra usa regras em
BarLayout.js e estado/undo em BarLayout.qml; a interface não mantém uma segunda
cópia persistente do layout. SettingsInlineControls reaproveita os accessors do
catálogo atual. SettingsScreenSelection compartilha a semântica de lista vazia
(todos os monitores) entre barra, dock e desktop. O esquema continua autoritativo.

Os testes de recursos e mídia carregam os componentes consumidores reais em cenas
isoladas, sem player/rede ativos. O teste de primeira execução carrega o serviço
real com marcador existente. Testes com outros serviços simulados não comprovam
a inicialização da shell completa nem o comportamento com o compositor real.
