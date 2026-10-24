# Configuração / Configuration

## Arquivo ativo e presets

| Conteúdo | Caminho padrão |
|---|---|
| Estado ativo, lido/escrito por `Config.qml` | `~/.config/illogical-impulse/config.json` |
| Presets salvos | `~/.config/illogical-impulse/presets/*.json` |
| Presets baixados | `~/.cache/quickshell/presets/*.json` |
| Presets importados | `~/.cache/quickshell/presets_imported/*.json` |
| Backups | Subpasta `backups/` junto ao JSON alterado |
| Cores geradas | `~/.local/state/quickshell/user/generated/colors.json` |
| Ordem personalizada de wallpapers | `~/.config/illogical-impulse/wallpaper_order.json` |

O código QML usa diretórios XDG. Os scripts de presets deste fork respeitam
`XDG_CONFIG_HOME` e `XDG_CACHE_HOME`; o doctor também usa `XDG_STATE_HOME`.
Alguns scripts e serviços legados do projeto ainda fixam `$HOME/.config` ou
`.cache`. Não foi concluída migração global de XDG para toda a shell.

Mudar um switch altera o **estado ativo**, normalmente gravado após 50 ms.
Isso não atualiza automaticamente o preset salvo. “Save/Overwrite” captura
o estado ativo, respeitando a blacklist original. Para criar uma variação,
aplique o preset, altere as opções desejadas e salve com outro nome.

Aplicar é uma **mesclagem**: campos ausentes no preset preservam o estado
local. Serviços, credenciais, fontes da interface, apps fixados e outras
preferências da blacklist não são substituídos. Um preset não é um snapshot
completo de toda a sessão. Não existe indicador novo de “alterado”.

## Exemplo mínimo

Trecho ilustrativo; não substitua todo o seu JSON por ele:

```json
{
  "background": {
    "wallpaperPath": "/caminho/real/wallpaper.jpeg",
    "widgets": {"glass": {"enable": true}}
  },
  "appearance": {
    "transparency": {"enable": true, "automatic": true}
  }
}
```

Use a extensão e o caminho reais. Não desligue transparência automática
para tentar reparar um arquivo ausente. Veja [Glassy UI](glassy-ui.md).

Os campos de imagem conhecidos aceitam caminho absoluto, `~/`, URL local
`file://` ou, em um preset, caminho relativo à pasta do JSON. A aplicação
normaliza os caminhos conhecidos; texto livre e comandos não são reescritos.
URLs remotas não são baixadas automaticamente. Famílias de fontes são nomes,
não caminhos; o doctor avisa se `fc-match` encontra uma substituição.

Mudanças de switches de aparência são imediatas. O motor de cores pode
trabalhar em segundo plano; fontes/temas de aplicativos externos dependem do
próprio aplicativo. Mudanças no código QML normalmente são recarregadas pelo
Quickshell, mas reinicie apenas a shell se necessário.

**English:** active settings and saved presets are distinct. Applying merges
filtered keys; editing a switch does not overwrite a saved preset. Existing
JSON keys and presets remain supported, while missing assets now block apply
with a diagnostic. Avoid simultaneous edits from another tool during apply.
