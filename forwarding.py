import ipaddress
import socket
import sys


def parse_packet(IP_packet: bytes) -> dict:
    return {
        "ip": ".".join(str(b) for b in IP_packet[:4]),
        "port": int.from_bytes(IP_packet[4:6], "big"),
        "msg": IP_packet[6:].decode(),
    }


def create_packet(parsed_IP_packet: dict) -> bytes:
    ip = bytes(int(x) for x in parsed_IP_packet["ip"].split("."))
    port = parsed_IP_packet["port"].to_bytes(2, "big")
    return ip + port + parsed_IP_packet["msg"].encode()


def check_routes(routes_file_name: str, destination_address: tuple):
    dest_ip, dest_port = destination_address
    with open(routes_file_name) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            cidr, p_ini, p_fin, hop_ip, hop_port = line.split()
            if (ipaddress.ip_address(dest_ip) in ipaddress.ip_network(cidr, strict=False)
                    and int(p_ini) <= dest_port <= int(p_fin)):
                return (hop_ip, int(hop_port))
    return None


def run_router(router_ip, router_port, routes_file):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((router_ip, router_port))
    while True:
        data, _ = sock.recvfrom(1024)
        parsed = parse_packet(data)
        dest = (parsed["ip"], parsed["port"])
        if dest == (router_ip, router_port):
            print(parsed["msg"])
            continue
        next_hop = check_routes(routes_file, dest)
        if next_hop is not None:
            sock.sendto(create_packet(parsed), next_hop)


def send_message(ip_final, port_final, ip_envio, port_envio, msg):
    packet = create_packet({"ip": ip_final, "port": port_final, "msg": msg})
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(packet, (ip_envio, port_envio))


if __name__ == "__main__":
    if sys.argv[1] == "router":
        run_router(sys.argv[2], int(sys.argv[3]), sys.argv[4])
    elif sys.argv[1] == "send":
        send_message(sys.argv[2], int(sys.argv[3]), sys.argv[4], int(sys.argv[5]), sys.argv[6])