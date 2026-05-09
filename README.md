# Port Scanner Personalizado em Python

![Max Müller](https://img.shields.io/badge/Autor-Max%20M%C3%BCller-darkred?style=for-the-badge&logo=github)
![Python](https://img.shields.io/badge/Python-3.8%2B-black?style=for-the-badge&logo=python)
![Port Scanner](https://img.shields.io/badge/Port%20Scanner-TCP%20Only-darkred?style=for-the-badge&logo=codefactor)
![Multithreading](https://img.shields.io/badge/Multithreading-Enabled-black?style=for-the-badge&logo=threadless)
![Ethical Use](https://img.shields.io/badge/Ethical%20Hacking-Legal%20Use%20Only-darkred?style=for-the-badge&logo=security)
![CLI](https://img.shields.io/badge/CLI-Argparse-black?style=for-the-badge&logo=terminal)
![Networking](https://img.shields.io/badge/Networking-Port%20Scanning-darkred?style=for-the-badge&logo=wifi)
![Dependencies](https://img.shields.io/badge/Dependencies-None-black?style=for-the-badge&logo=pypi)
[![Sponsor](https://img.shields.io/badge/Apoie_este_projeto-Sponsor-ea4aaa?style=for-the-badge&logo=github-sponsors)](https://github.com/sponsors/MMVonnSeek)


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

---
<img width="1419" height="365" alt="Captura de tela de 2025-11-26 15-50-50" src="https://github.com/user-attachments/assets/16398b3e-4639-4760-af9e-89e7f03e3f75" />

---




## Como usar

1. Faça um Fork do Repositório:
Antes de tudo, crie sua própria cópia deste projeto:

- Clique no botão Fork no canto superior direito do GitHub.

- Isso criará uma versão do repositório na sua conta.

2. Clone o Seu Repositório Forkado:

```
git clone https://github.com/SEU-USUARIO/Port-Scanner.git
cd Port-Scanner
```


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

----------

## Contribuição

Se você gostou do projeto, não esqueça de:

-   ⭐ Deixar uma estrela no Repositório
    
-    Reportar bugs encontrados
    
-    Sugerir novas funcionalidades
    
-    Fazer um fork e contribuir
    

----------

<div align="center"> <sub> Feito por <strong>Prof. Max Muller - MMVonnSeek</strong> para a comunidade de segurança </sub>

  
  

[![Stars](https://img.shields.io/github/stars/MMVonnSeek/Port-Scanner?style=social)](https://github.com/MMVonnSeek/Port-Scanner/stargazers)
[![Forks](https://img.shields.io/github/forks/MMVonnSeek/Port-Scanner?style=social)](https://github.com/MMVonnSeek/Port-Scanner/network/members)
[![Follow](https://img.shields.io/github/followers/MMVonnSeek?style=social)](https://github.com/MMVonnSeek)

[![Sponsor](https://img.shields.io/badge/Apoie_este_projeto-Sponsor-ea4aaa?style=for-the-badge&logo=github-sponsors)](https://github.com/sponsors/MMVonnSeek)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Max_Muller-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/max-muller-685705248/)

<br>

  [Voltar ao topo](#-Port-Scanner)

</div>
