# Presets, portabilidade e recuperação / Presets and recovery

## Uso normal

Use Dashboard → Presets para salvar, aplicar, instalar, importar/exportar,
renomear e excluir. O desenho dessa página foi preservado. Este fork retorna
erros por notificações existentes. Falhas de download também aparecem no
estado de erro já existente da galeria.

Comandos equivalentes, a partir da pasta do checkout:

```sh
bash scripts/presets.sh --save persona-teste "Minha variação"
bash scripts/presets.sh --apply persona-teste
bash scripts/presets.sh --rename persona-teste persona-teste-2
bash scripts/presets.sh --export-zip persona-teste-2
bash scripts/presets.sh --import-zip "/caminho/para/persona-teste-2.zip"
```

Esses comandos são **ações**, não diagnóstico. Salvar captura o estado ativo;
sobrescrever cria backup do preset anterior. Renomear não altera arquivos de
imagem. Excluir remove o JSON e, para caches legados, sua pasta de assets pelo
nome. Não exclua um preset legado cujas imagens ainda são usadas na configuração
ativa; instale/copie primeiro seus recursos e confirme os caminhos.

`--online` e `--imported` selecionam a origem para aplicar/instalar/remover.
Uma importação repetida usa novo nome, sem sobrescrever a anterior. Caches
novos de assets usam diretórios únicos; não há coletor automático dos caches
órfãos nesta etapa, para evitar apagar imagens ainda referenciadas.

## O caso Persona: PNG ausente, JPEG existente

Examine primeiro o **JSON que você pretende corrigir**:

```sh
python3 scripts/preset_resources.py "$HOME/.config/illogical-impulse/config.json"
```

O resultado informa campo, caminho, causa e candidatos válidos com mesmo nome
base na mesma pasta. Se só existir `wallpaper.jpeg`, o comando sugere esse
arquivo. Não altera nada. Se houver JPEG e WebP, informa ambiguidade.

Para aceitar explicitamente **todas** as correções inequívocas desse arquivo:

```sh
python3 scripts/preset_resources.py "$HOME/.config/illogical-impulse/config.json" --repair-missing
```

O comando cria backup e troca somente referências ausentes com candidato único.
Se algum problema for ambíguo, corrompido ou não corrigível, não modifica o JSON.
Pode ser usado também em um preset salvo, passando o caminho desse preset.
Corrigir o estado ativo não repara automaticamente os presets Persona/Maomao
salvos. Valide e salve cada um quando desejar preservar a correção.

## Formato portátil

A exportação preserva o JSON convencional e `meta.json`, acrescentando
`asset-manifest.json` versão 1 com campo, arquivo relativo e SHA-256. Imagens
com mesmo basename e conteúdo diferente recebem nomes distintos. Os caminhos
locais conhecidos são reescritos para referências relativas no pacote. A
blacklist de privacidade original continua aplicada.

A importação aceita ZIPs legados planos ou com uma pasta, sem manifesto,
desde que exista exatamente um JSON de preset e assets sem ambiguidade. Um
caminho de outro usuário só é relocalizado para uma imagem realmente contida
no pacote. Não procura a primeira imagem de mesmo nome em sua pasta Pictures.
ZIP com traversal, symlink, JSON ambíguo ou hash inválido é rejeitado.
Limites: 2.048 entradas e 256 MiB descompactados.

Na instalação, arquivos pessoais com mesmo nome e conteúdo diferente são
preservados; o novo asset recebe sufixo de hash. O caminho Pictures é mantido
por compatibilidade com o instalador original, sem mover imagens já existentes.

Compatibilidade: o manifesto é aditivo e os nomes de campos não mudam.
Recursos inválidos agora bloqueiam aplicação/exportação. Não há substituição
implícita por outra extensão. Imagens acima do limite da galeria requerem
redimensionar uma cópia antes de exportar; esta etapa não as recomprime
silenciosamente. Ao preparar novamente uma pasta de upload com o mesmo nome,
a anterior é guardada em `presets_share/backups/` antes da substituição.

## Aplicação e rollback

Ordem: filtrar → mesclar → validar → snapshot → substituir JSON atomicamente
→ executar `switchwall.sh` → verificar. Falha do processo ou da verificação
restaura os bytes anteriores do JSON. A UI pausa suas escritas durante esse
fluxo e descarrega alterações pendentes antes de começar. Aplicações via CLI
são serializadas por lock; editores e scripts externos não participam dele.

Temas GTK/Qt, arquivos produzidos por matugen e processos de vídeo **não fazem
parte de uma transação global**. O processo filho pode produzir efeitos antes
de falhar. O backup do JSON não promete reverter esses efeitos.

Para restaurar, pare somente a instância deste checkout e escolha um snapshot:

```sh
qs kill -p .
python3 scripts/preset_recover.py "/caminho/para/config.json.SNAPSHOT.bak" "$HOME/.config/illogical-impulse/config.json"
qs -p . --daemonize
```

O arquivo atual é guardado em outro backup, mesmo se estiver corrompido.
Para voltar explicitamente aos defaults embutidos, também com backup:

```sh
python3 scripts/preset_recover.py --safe-default "$HOME/.config/illogical-impulse/config.json"
```

Esse último comando muda preferências ativas; use somente quando essa for a
recuperação desejada. Nenhum backup é apagado automaticamente.

**English:** validation is read-only unless `--repair-missing` is explicitly
selected. Unique same-stem repairs are backed up; ambiguity blocks writes.
Legacy bundles remain supported. Transactions restore config JSON on failure,
not all external theme/process effects. Stop this shell before restoring a backup.
