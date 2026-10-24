# Primeiros passos / Getting started

Este fork mantém o visual do end4-pC: barra, dock, dashboard, sidebars,
widgets, shaders e animações existentes. As screenshots no README são do
projeto original. Consulte [o estado da validação](validation.md).

## Antes de iniciar

É necessário ter CachyOS/Arch com sessão Hyprland/Wayland e o ambiente
illogical-impulse já preparado. Este repositório contém a shell; não contém
um instalador completo de Hyprland, PAM, portais, fontes, ambiente Python de
cores e templates matugen. Não execute instaladores de terceiros como root
para tentar resolver uma dependência sem entender quais arquivos modificam.

| Componente | Para que serve |
|---|---|
| Quickshell + módulos Qt Quick, Controls, Effects, Positioning, Kirigami | Executar a interface |
| Hyprland e `hyprctl` | Janelas, monitores e integração do compositor |
| Python 3, Bash, jq, ImageMagick (`magick`) | Presets, validação e imagens |
| matugen + templates e venv do illogical-impulse | Geração/aplicação de cores |
| Fontes configuradas, Material Symbols, Nerd Font | Texto e símbolos no visual original |
| cliphist + ferramentas wl-clipboard | Histórico e cópia de clipboard, opcionais |
| mpvpaper + ffmpeg | Wallpapers em vídeo, opcionais |
| GeoClue/backend Qt Positioning | Localização automática, opcional; cidade manual disponível |

A versão local usada nos testes foi Quickshell **0.3.2**. Ainda não foi
estabelecida uma versão mínima de Quickshell/Hyprland nem testada uma matriz
de distribuições. O doctor informa presença e versão; não certifica compatibilidade.

## Usar o checkout local

Entre na pasta `end4-pC` deste checkout pelo terminal. Os comandos abaixo
podem ser digitados no Fish e no Bash. Scripts `.sh` são executados com Bash.

Primeiro, faça somente diagnóstico:

```sh
python3 scripts/doctor.py
python3 scripts/doctor.py --lang en
```

Não há instalação automática. Resolva as dependências indicadas com o
gerenciador da sua distribuição. A documentação do ambiente base continua
sendo necessária para instalar seus templates/venv, que não estão neste fork.

O código usa a configuração ativa do illogical-impulse. Faça uma cópia privada
antes da primeira execução (caminho padrão; ajuste se usa XDG personalizado):

```sh
python3 scripts/preset_resources.py "$HOME/.config/illogical-impulse/config.json" --backup-only
```

Não execute duas versões da shell contra essa configuração. Identifique a
instância atual com `qs list`. Se ela usa o nome `ii`, pare **somente ela**:

```sh
qs kill -c ii
```

Inicie este checkout, estando na pasta dele:

```sh
qs -p . --daemonize
```

Isso inicia a shell e seus serviços normais, incluindo integrações do ambiente
base. Esses comandos de início/parada são instruções para você; **não foram
executados contra sua sessão durante o desenvolvimento**. Não é necessário
encerrar o Hyprland. Se a shell não abrir, execute `qs -p .` no terminal para
ver os erros. Para voltar à shell anterior, pare este checkout com `qs kill -p .`
e inicie a anterior com `qs -c ii --daemonize`, se esse era seu nome original.

Não altere seu autostart antes de validar o fork manualmente. O repositório
não modifica seus atalhos nem escolhe um novo wallpaper ao ser testado.

## Primeira configuração

Abra as configurações pelo atalho já configurado. `Escape` fecha o overlay.
No launcher, procure `wallpaper`, `transparency` ou `blur`; veja também
[configuração](configuration.md), [Glassy UI](glassy-ui.md) e [FAQ](faq.md).
No dashboard, os controles de modo claro/escuro ficam na área de aparência;
na página Quick, são os botões de sol/lua. Eles podem chamar o sistema de
cores do ambiente base: veja a distinção entre shell e aplicativos no FAQ.

**English:** run the read-only doctor first, back up the shared active config,
stop only the previous shell instance and start this checkout with `qs -p .`.
The full illogical-impulse environment is a prerequisite, not installed here.
No packages, dotfiles, autostart entries or remote forks are installed automatically.
