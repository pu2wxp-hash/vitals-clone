# RaioX Mac

Aplicativo de barra de menus para acompanhar a atividade local do Mac. Esta é uma personalização do fork de [Samin12/vitals-clone](https://github.com/Samin12/vitals-clone); o app utiliza SwiftUI e o fluxo de inspeção do REA como referência.

## Recursos

- CPU, memória, disco, rede e GPU, no sistema e por aplicativo.
- Processos agrupados por app e por projeto de desenvolvimento.
- Portas em escuta, servidores de desenvolvimento ociosos e apps que impedem o repouso.
- Alertas locais para uso sustentado de recursos.
- Ações para encerrar processos e projetos. *Force Quit* pode encerrar processos imediatamente e descartar alterações não salvas.

## Requisitos

- macOS 13 ou posterior.
- Para compilar localmente: Xcode ou Command Line Tools com Swift 6 e o SDK macOS apropriado.

## Compilar no Mac

```sh
./build-app.sh
open "build/RaioX Mac.app"
"build/RaioX Mac.app/Contents/MacOS/RaioXMac" --dump
```

O script usa o Xcode selecionado no sistema e o SDK macOS encontrado por `xcrun`. O aplicativo fica em `build/RaioX Mac.app`.

O ícone do bundle é construído a partir de `Assets/RaioXMac-1024.png`; a fonte programática está em `scripts/generate_app_icon.py`. Para regenerar a imagem-fonte, instale Pillow e execute `python3 scripts/generate_app_icon.py`.

## Build universal

O workflow manual em `.github/workflows/build-macos.yml` compila e testa as arquiteturas Apple Silicon e Intel, combina os binários e gera um `.dmg` e um `.zip` universais.

## Avisos

O app monitora informações locais de processos, como nome, caminho, identificador, uso de recursos e portas. Não foi feita auditoria formal de segurança. A assinatura de build é ad hoc e o app não é notarizado pela Apple; o macOS pode pedir confirmação na primeira abertura. O workflow não publica uma release automaticamente.
