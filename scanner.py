#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Port Scanner Personalizado com Python
- Varredura rápida, completa ou personalizada de portas TCP
- Multithreading para alto desempenho
- CLI com argparse
- Saída amigável com banner, tempo e resumo
- Termo de uso ético embutido

Exemplos:
  python3 scanner.py -t 192.168.0.1 -m full --accept-terms
  python3 scanner.py -t scanme.nmap.org -m fast
  python3 scanner.py -t 192.168.0.10 -m custom -p 22,80,443,8000-8100 -T 400 --timeout 0.5
"""

import argparse
import concurrent.futures as futures
import ipaddress
import socket
import sys
import time
from datetime import datetime
from typing import Iterable, List, Set

BANNER = r"""
██████╗  ██████╗ ██████╗ ████████╗     ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ 
██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝     ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗
██████╔╝██║   ██║██████╔╝   ██║        ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
██╔═══╝ ██║   ██║██╔══██╗   ██║        ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
██║     ╚██████╔╝██║  ██║   ██║███████╗███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║
╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
      Scanner educacional de portas TCP — uso ético apenas
"""


TERMO_USO = """
TERMO DE USO ÉTICO
Este software destina-se exclusivamente a fins educacionais e de testes
autorizados. Você deve possuir permissão explícita para escanear o alvo.
O uso indevido pode violar leis locais e resultar em sanções civis/penais.
AO PROSSEGUIR, VOCÊ DECLARA QUE COMPREENDE E CONCORDA COM ESTES TERMOS.
"""

COMMON_PORTS = [
    20, 21, 22, 23, 25, 53, 67, 68, 69, 80, 110, 123, 137, 138, 139, 143,
    161, 162, 389, 443, 445, 465, 514, 587, 631, 636, 873, 993, 995, 1080,
    1433, 1521, 2049, 2181, 2375, 2376, 27017, 3000, 3128, 3306, 3389, 4444,
    5000, 5432, 5672, 5900, 5984, 6379, 6443, 7001, 7002, 8000, 8001, 8008,
    8080, 8081, 8088, 8443, 8888, 9200, 9300, 11211, 27017
]

def print_banner():
    print(BANNER)

def exigir_termos(args):
    if args.accept_terms:
        return
    print(TERMO_USO.strip())
    resp = input("Digite 'ACEITO' para continuar: ").strip().upper()
    if resp != "ACEITO":
        print("Operação cancelada. Utilize --accept-terms para pular este aviso.")
        sys.exit(2)

def validar_alvo(alvo: str) -> str:
    # Tenta IP literal; se falhar, resolve DNS
    try:
        ipaddress.ip_address(alvo)
        return alvo
    except ValueError:
        try:
            resolved = socket.gethostbyname(alvo)
            return resolved
        except socket.gaierror:
            print(f"[ERRO] Não foi possível resolver o alvo: {alvo}")
            sys.exit(2)

def parse_intervalos(spec: str) -> List[int]:
    """
    Aceita formatos como:
      '80,443,8080'  |  '20-25'  |  '22,80,8000-8100'
    """
    portas: Set[int] = set()
    for parte in spec.split(","):
        parte = parte.strip()
        if not parte:
            continue
        if "-" in parte:
            a, b = parte.split("-", 1)
            ini, fim = int(a), int(b)
            if ini > fim:
                ini, fim = fim, ini
            for p in range(max(1, ini), min(65535, fim) + 1):
                portas.add(p)
        else:
            p = int(parte)
            if 1 <= p <= 65535:
                portas.add(p)
    return sorted(portas)

def montar_lista_portas(modo: str, custom_spec: str | None) -> List[int]:
    if modo == "fast":
        return sorted(set(COMMON_PORTS))
    if modo == "full":
        return list(range(1, 65536))
    if modo == "custom":
        if not custom_spec:
            print("[ERRO] Para modo custom, informe -p/--ports (ex.: 22,80,443,8000-8100).")
            sys.exit(2)
        portas = parse_intervalos(custom_spec)
        if not portas:
            print("[ERRO] Nenhuma porta válida em --ports.")
            sys.exit(2)
        return portas
    print("[ERRO] Modo inválido.")
    sys.exit(2)

def tentar_conexao(ip: str, porta: int, timeout: float) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        try:
            s.connect((ip, porta))
            return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            return False

def nome_servico(porta: int) -> str:
    try:
        return socket.getservbyport(porta, "tcp")
    except OSError:
        return "-"

def worker(args_tuple) -> tuple[int, bool]:
    ip, porta, timeout = args_tuple
    aberto = tentar_conexao(ip, porta, timeout)
    return (porta, aberto)

def scan_ports(ip: str, portas: Iterable[int], threads: int, timeout: float) -> List[int]:
    abertos: List[int] = []
    total = len(list(portas)) if not isinstance(portas, list) else len(portas)
    if not isinstance(portas, list):
        portas = list(portas)

    print(f"\nIniciando varredura TCP em {ip}")
    print(f"Total de portas a verificar: {total}")
    print(f"Threads: {threads} | Timeout por porta: {timeout:.2f}s\n")

    with futures.ThreadPoolExecutor(max_workers=threads) as executor:
        tasks = ((ip, p, timeout) for p in portas)
        for porta, aberto in executor.map(worker, tasks, chunksize=256):
            if aberto:
                abertos.append(porta)
                svc = nome_servico(porta)
                print(f"[ABERTA] {porta:<5} serviço: {svc}")
    return sorted(abertos)

def construir_argparse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="scanner.py",
        description="Port Scanner Personalizado (educacional) com Python",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-t", "--target", required=True, help="IP ou hostname do alvo")
    parser.add_argument(
        "-m", "--mode", choices=["fast", "full", "custom"], default="fast",
        help="Modo de varredura: fast (comum), full (1-65535) ou custom"
    )
    parser.add_argument(
        "-p", "--ports", default=None,
        help="Especificação de portas (custom). Ex.: 22,80,443,8000-8100"
    )
    parser.add_argument(
        "-T", "--threads", type=int, default=300,
        help="Número de threads para varredura"
    )
    parser.add_argument(
        "--timeout", type=float, default=0.6,
        help="Timeout em segundos por tentativa de conexão"
    )
    parser.add_argument(
        "--accept-terms", action="store_true",
        help="Aceita o termo de uso ético sem prompt interativo"
    )
    return parser.parse_args()

def main():
    print_banner()
    args = construir_argparse()
    exigir_termos(args)

    # Resolve alvo e prepara portas
    ip = validar_alvo(args.target)
    portas = montar_lista_portas(args.mode, args.ports)

    inicio = time.perf_counter()
    inicio_humano = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"Alvo: {args.target}  (IP: {ip})  |  Início: {inicio_humano}")
    print(f"Modo: {args.mode}  |  Portas: {len(portas)}\n")

    abertos = scan_ports(ip, portas, threads=max(1, args.threads), timeout=args.timeout)

    duracao = time.perf_counter() - inicio
    print("\n" + "-" * 60)
    print("RESUMO")
    print("-" * 60)
    if abertos:
        print(f"Portas abertas ({len(abertos)}): " + ", ".join(str(p) for p in abertos))
    else:
        print("Nenhuma porta aberta identificada (pode haver filtros/firewalls).")
    print(f"Tempo total: {duracao:.2f} segundos")
    print("Concluído com sucesso.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrompido pelo usuário.")
        sys.exit(130)
