# Glassy UI: funcionamento e diagnóstico

Glassy UI usa a imagem do wallpaper como entrada do shader existente em
`WindowGlass.qml`/`FrostedGlass.qml`. Ele recorta a região correspondente à
superfície para produzir o efeito de vidro. Não basta o switch estar ligado:
a imagem precisa existir e ser decodificável. Em vídeos, usa a thumbnail.
Na tela bloqueada, `background.lockWall` é independente do wallpaper normal.

| Opção | Responsabilidade |
|---|---|
| `background.widgets.glass.enable` | Liga o shader Glassy UI |
| `appearance.transparency.enable` | Controla transparência do fundo conforme implementação original |
| `appearance.transparency.automatic` | Escolhe cálculo automático ou valores manuais |
| Transparência manual | Valores preservados quando se usa o modo automático |
| Blur do compositor/lockscreen | Desfoque separado, dependente das opções existentes |

As fórmulas de conteúdo e fundo continuam as originais. Não foram “corrigidas”
invertendo toggle nem forçando transparência manual. Os controles mantêm os
identificadores e a persistência. Dicas aparecem apenas ao passar o mouse nos
controles existentes do dashboard.

## Quando o vidro não aparece

1. Rode `python3 scripts/doctor.py` na pasta deste checkout.
2. Examine `background.wallpaperPath` com `preset_resources.py`, conforme
   [presets](presets.md). Confirme extensão real, permissões e decodificação.
3. Se o problema ocorre só bloqueado, examine `background.lockWall` separadamente.
4. Para vídeo, examine `background.thumbnailPath` e dependências ffmpeg/mpvpaper.
5. Com imagem válida, teste o switch e as opções originais; não use uma mudança
   de transparência como substituto de corrigir a imagem.

Ao faltar imagem persistida, o novo serviço compartilhado impede que cada
instância de `WindowGlass` tente abri-la. Há um aviso por caminho e o fundo
usa a cor de fallback do tema. **Isso não significa vidro funcionando**.
Restaurar o arquivo no mesmo caminho é detectado novamente em até 10 s;
alterar o caminho provoca nova validação. Arquivos válidos removidos depois da
validação precisam de nova validação/reinício: não há watcher completo de assets.
Pré-visualizações do seletor continuam imediatas e usam seu fluxo original.

ImageMagick valida a integridade antes de aplicar presets. Na renderização,
se não houver decoder CLI, uma imagem existente ainda pode ser aberta pelo
Qt; isso gera aviso de integridade não verificada. O doctor distingue essa
dependência ausente. Codecs de vídeo precisam de teste na sessão real.

**English:** Glassy UI samples a valid wallpaper (or a video thumbnail).
The toggle and transparency formulas are unchanged. A missing image disables
the glass source and shows a themed fallback, not a simulated success. Check
the lock wallpaper separately. Offscreen tests cover persistence, not GPU output.
