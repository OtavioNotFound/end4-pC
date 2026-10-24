# Auditoria e plano técnico — 24/10/2026

Base local: `cbe1aad`, branch inicial `main`, checkout limpo. Remoto configurado:
`https://github.com/pctrade/end4-pC`. Licença GPL v3, créditos mantidos.
A especificação de referência está em `../END4_PC_FORK_SPEC.md`, fora do checkout.
Na Fase A, não foi criado fork remoto nem executada publicação.
Após autorização explícita do usuário, o fork público foi criado em
[OtavioNotFound/end4-pC](https://github.com/OtavioNotFound/end4-pC), com a branch
`fix/preset-resource-reliability` como padrão. O upstream permanece inalterado.

## Escopo e arquitetura

Inventário da árvore, README, licença, histórico recente e revisão dos caminhos
críticos de presets, configuração, recursos, renderização, ícones e serviços.
Isso não equivale a revisar individualmente todas as linhas dos 860 arquivos
versionados nem a uma certificação de segurança de toda a shell.

`shell.qml` inicializa serviços singleton e `IllogicalImpulseFamily` carrega os
painéis após `Config.ready`. `Config.qml` usa `FileView` + `JsonAdapter`, com
gravações/releituras adiadas em 50 ms. `Directories.qml` deriva diretórios XDG;
o script de presets original, ao contrário, fixava `$HOME/.config` e `.cache`.

Fluxo original:

```text
DashboardPresetDetail → Presets.qml → presets.sh
                                     ├─ jq: filtrar + mesclar config.json
                                     └─ switchwall.sh: wallpaper, vídeo, cores e temas externos
config.json → Config.options → Background / Appearance / WindowGlass
```

`WindowGlass` recorta uma cópia do wallpaper segundo a posição da superfície,
e `FrostedGlass` aplica o shader existente. O vidro depende de imagem válida;
não há evidência de toggle invertido. Não alterar sua fórmula de transparência.
`Background` possui transições e reprodução de vídeo; `CenteredWallpaper`
recorta outra imagem. `Appearance` usa `ColorQuantizer` para transparência.

## Ciclo de presets auditado

| Operação | Implementação original | Risco encontrado |
|---|---|---|
| Salvar/sobrescrever | `presets.sh --save`, blacklist jq | Redirecionamento antes de validar; snapshot ausente |
| Aplicar | `Presets.qml` → `--apply` destacado | Sem validação de assets, UI sem resultado, sem rollback |
| Duplicar | Salvar estado ativo com outro nome | Não é cópia direta de um preset salvo; documentar |
| Renomear | mover JSON | Nome sem restrição de caminho; assets referidos continuam pelo caminho antigo |
| Excluir | remover JSON e diretório de cache pelo nome | Caminhos construídos com nome não validado |
| Importar ZIP | extrair, escolher primeiro JSON, copiar por basename | JSON ambíguo, colisões, arquivo parcialmente escrito |
| Exportar | filtrar/sanitizar, copiar imagens, `meta.json` | Colisões por basename; sem manifesto de integridade |
| Instalar da galeria | `preset_install.py` | Procura primeira imagem com mesmo nome em Pictures; escolha arbitrária |
| Baixar da galeria | `PresetsOnline.qml`, curl/jq | Rewrite direto no JSON final; validação apenas posterior |
| Migrar/reverter | Não há operação formal | Compatibilidade depende de mesclagem e blacklist; falta recuperação documentada |

Compartilhamento (`preset_share*.sh`) autentica e publica no GitHub. Não foi
executado. `shell.qml`, `Directories` e scripts de cores têm efeitos reais de
autostart, limpeza de caches e temas: não iniciar a shell completa para testar.

## Evidências antes das alterações

Simulações com HOME temporário e `switchwall.sh` substituído por stub:

1. PNG ausente + JPEG existente + switchwall retornando 19: `--apply` retorna 19,
   mas **config já foi alterada**. Não existe correção/validação prévia.
2. `config_json_replace` com stdin vazio: retorna 0 e produz **zero bytes**.
   `jq empty` aceita stream sem documentos, portanto não prova JSON de configuração válido.
3. Inspeção: `Weather.data.description` é lido no dashboard, mas não existe no
   objeto inicial. Causa concreta possível do aviso `undefined → QString`;
   outros bindings ainda precisam de observação na sessão real.
4. Há `assets/icons/cachyos-symbolic.svg`, `arch-symbolic.svg` e
   `desktop-symbolic.svg`: fallback local é possível sem modificar `/usr/share`.
5. `wallpaper_order.json` já possui fallback vazio: ausência na primeira execução
   é normal. `colors.json` também pode ainda não ter sido gerado, mas o loader
   original tenta parsear conteúdo inválido sem proteção.
6. `Cliphist.refresh()` inicia processo sem verificar dependência. Weather já
   desativa GPS inválido e usa cidade manual; a disponibilidade de GeoClue na
   máquina do usuário não foi reproduzida nesta auditoria.

Baseline: 32 testes existentes de gerenciamento de temas de ícones passaram.
Quickshell disponível localmente: 0.3.2. Python, jq, ImageMagick, Fish e
ferramentas Qt 6 estão presentes. Isso não estabelece versão mínima suportada
de Hyprland/Quickshell; não há matriz de versões upstream neste checkout.

## Sequência proposta e critérios

1. **Persistência P0** — `scripts/lib/config.sh`: exigir um único objeto JSON;
   testes de stream vazio, inválido, array, scalar e múltiplos documentos.
2. **Recursos e aplicação P0** — novos `preset_resources.py`, `preset_apply.py`,
   `presets.sh`, `Config.qml`, `Presets.qml`: validar campos de assets conhecidos,
   diagnosticar sem substituição implícita, backup antes da escrita, commit
   atômico e rollback do JSON quando o processo/verificação falhar. Pausar
   escrita QML; serializar aplicações. Testar Persona/Maomao e lockscreen separado.
3. **Portabilidade P0** — `preset_bundle.py`, `preset_install.py`: staging,
   manifesto aditivo SHA-256, suporte a ZIP antigo, basename ambíguo bloqueado,
   colisões preservadas, nomes restritos e importação sem sobrescrever cache.
4. **Resiliência P1** — `WallpaperResources.qml`, `WindowGlass`, `Appearance`,
   `Background`, `CenteredWallpaper`, `SystemAppearance`, loaders e serviços:
   verificar wallpaper uma vez, fallback de cor, aviso por caminho e SVG interno.
   `switchwall.sh`: propagar falha de matugen/geração para permitir rollback.
5. **Diagnóstico/UX P1** — `doctor.py`, `preset_recover.py`, dicas nos controles
   existentes; leitura offline, relatório sanitizado por allowlist, sem
   instalação automática nem nova tela. Não implementar ideias opcionais da
   especificação sem proposta/aprovação.
6. **Documentação P2** — guias PT-BR e notas EN, comandos seguros para Fish,
   testes isolados e roteiro de validação visual original.

## Riscos e limites de aceite

- Atomicidade do arquivo não é atomicidade de toda a sessão. `switchwall.sh`
  também altera GTK/Qt, processos de vídeo e outros arquivos; não prometer
  rollback completo desses efeitos. Scripts externos não compartilham o lock
  de presets. Evitar editar em outra ferramenta durante aplicação/recuperação.
- JSONs antigos continuam aceitos; recursos inexistentes passam a bloquear
  aplicação. Essa mudança de erro é intencional e exige instrução de correção.
- Fontes são nomes de famílias, não arquivos: blacklist preservada, substituições
  inspecionadas pelo doctor. Diagnóstico de schema é inicialmente direcionado,
  não validação exaustiva de todas as propriedades aninhadas.
- Imagem corrompida exige decoder. ImageMagick valida presets; reprodução de
  vídeos e codecs precisa de compositor. Arquivos remotos não são baixados.
- Assets de widgets conhecidos/collage são validados; strings arbitrárias e
  comandos nunca são reinterpretados como caminhos.
- Validar sem compositor cobre persistência/bindings, **não comprova equivalência
  visual**. Matriz gráfica: vidro on/off × transparência on/off × auto/manual,
  alternância Persona/Maomao, reinício, monitores e lockscreen.
- A galeria ainda precisa de teste real de download com cache isolado; testes
  offline não autorizam publicação nem certificam disponibilidade da rede.

Resultados e pendências após implementação: [validation.md](validation.md).
