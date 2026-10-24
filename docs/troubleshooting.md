# Diagnóstico / Troubleshooting

Comece na pasta do checkout com `python3 scripts/doctor.py`. O comando não
escreve configuração, não instala pacotes e não acessa a rede. O resultado
separa dependência obrigatória, opcional e arquivos ainda não gerados.
Validação de schema é direcionada aos campos críticos; não certifica todos os
valores aninhados do JSON. Versões são informadas sem inventar compatibilidade.

Na interface da fase 2, abra **Verificar configuração** no dashboard ou em
**Sobre** nos estilos tradicional/mínimo. A tela reutiliza o mesmo doctor e
mostra caminhos de imagens problemáticas localmente. Essa saída privada não é
um relatório para compartilhar; a CLI `--report` continua omitindo os caminhos.
Se o JSON impedir a shell de iniciar, use a recuperação CLI descrita em
[presets](presets.md); a nova tela não substitui esse procedimento.

## Fluxo de decisão

```text
Shell não abre?
  → qs -p . no terminal → erro de import/dependência? → conferir ambiente base
  → JSON inválido? → parar apenas esta shell → restaurar snapshot
Shell abre, wallpaper/vidro falha?
  → doctor → recurso ausente? → preset_resources.py no JSON correto
  → candidato único? → aceitar explicitamente --repair-missing
  → ambíguo? → escolher manualmente o arquivo desejado; validar novamente
  → só na tela bloqueada? → verificar lockWall, não apenas wallpaperPath
  → imagem válida? → testar as opções originais, thumbnail e compositor
Ícone quebrado?
  → conferir tema selecionado → testar fallback SVG interno → registrar caso
Widget ausente?
  → conferir enable/monitor/preset ativo → conferir recurso e dependência
```

## Ícones

O resolvedor mantém o tema atual como primeira escolha. Se não houver
`cachyos`, `cachyos-symbolic`, `arch-symbolic`, `user-desktop` ou `image-missing`,
usa os SVGs já incluídos no projeto. Outros ícones sem fallback usam o SVG
interno de desktop; consultas de existência continuam retornando vazio quando
não há ícone. Não copie arquivos para `/usr/share/icons` nem use sudo para
esse fallback.

Esse caminho atende os consumidores de `SystemAppearance.iconPath`.
Componentes que chamam provedores/ícones diretamente precisam de diagnóstico
próprio; não foi substituído globalmente o sistema de ícones.

## Cores e arquivos opcionais

- `colors.json` ausente na primeira execução: a shell conserva a paleta
  embutida; verifique geração de cores somente se ela era esperada.
- JSON de cores inválido: loader mantém a última paleta válida em memória.
  Falha na geração SCSS mantém o arquivo SCSS anterior.
- `wallpaper_order.json` ausente: normal até haver ordem personalizada;
  o serviço usa ordem padrão, sem erro de abertura no log.
- `cliphist` ausente: histórico indisponível; o serviço verifica uma vez e
  evita repetir inicialização de processo ausente. Após instalar a dependência,
  reinicie apenas a shell para nova detecção.
- GeoClue indisponível: selecione cidade manual nas opções existentes de clima
  e desative GPS. O serviço já usa a cidade quando GPS está inativo.
  O doctor inspeciona presença do descritor; não promete que D-Bus/GPS esteja saudável.

Se uma aplicação de preset falhar, a notificação informa o processo e snapshot.
Quando `switchwall.sh` retorna erro, sua saída fica em arquivo `.log` privado
junto ao backup. Esse log **pode conter dados pessoais**; não o anexe bruto a
uma issue. A recuperação do JSON não reverte todos os temas externos.

## Logs e relatório compartilhável

Use `qs list` para identificar a instância correta. `qs log --help` explica as
opções da versão instalada. O console de `qs -p .` também mostra o log.
Se você salvou uma cópia textual, pode agrupá-la por causas conhecidas:

```sh
python3 scripts/doctor.py --log "/caminho/para/log-textual.txt"
python3 scripts/doctor.py --report > end4-diagnostic.json
python3 scripts/doctor.py --log "/caminho/para/log-textual.txt" --report > end4-diagnostic.json
```

`--report` usa allowlist: presença/versões, categorias, causas e contagens.
Não inclui configuração bruta, caminhos, candidatos de imagem, nomes de fontes,
linhas de log, tokens, SSIDs ou localização. Revise o relatório antes de enviar.
Sem `--report`, o diagnóstico local de assets mostra os caminhos necessários
para corrigir o problema. Os códigos de saída são 0 (sem erro obrigatório),
1 (erros encontrados) e 2 (falha ao executar o verificador).

## Reiniciar e recuperar

Na pasta deste checkout:

```sh
qs kill -p .
qs -p . --daemonize
```

Isso não encerra Hyprland. Não use `killall qs`, pois ele atinge outras
instâncias. Para restaurar JSON corrompido, siga [presets e recuperação](presets.md).
Não restaure um backup enquanto a shell ou outro editor puder sobrescrevê-lo.

**English:** run the read-only doctor; inspect assets locally and share only
the allowlisted `--report`. Missing order/colors files may be normal on first
run. Stop only the selected shell instance before recovery. Raw logs are private.
