# Port Scanner Personalizado em Python

Um **port scanner educacional** feito em Python, com foco em **ensino de redes e segurança da informação**. Permite varredura rápida, completa ou personalizada de portas TCP com **multithreading**.

## Funcionalidades

- Scan básico usando `socket`
- Scan avançado com **multithread**
- CLI interativa com `argparse`
- Exibição amigável dos resultados (banner, tempo, status)
- Termo de uso ético embutido

## Requisitos

- Python 3.8 ou superior
- Nenhuma biblioteca externa necessária


![Uploading Captura de tela de 2025-08-15 09-34-37.png…]()


## Como usar

### Scan rápido (portas comuns)
```bash
python3 scanner.py -t 192.168.0.1 -m fast --accept-terms
```

### Scan completo (todas as portas TCP)
```bash
python3 scanner.py -t 192.168.0.1 -m full --accept-terms
```
Pode demorar muito dependendo da rede.

### Scan personalizado
```bash
python3 scanner.py -t 192.168.0.1 -m custom -p 22,80,443,8000-8100 --accept-terms
```

### Ajustando threads e timeout
```bash
python3 scanner.py -t 192.168.0.1 -m fast -T 400 --timeout 0.5 --accept-terms
```
## Termo de uso ético

Este software somente deve ser utilizado em redes ou máquinas autorizadas. Qualquer uso indevido pode violar leis locais.















