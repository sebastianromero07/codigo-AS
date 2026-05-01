import os
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
H2_JAR = ROOT_DIR / "drivers" / "h2.jar"
H2_DATA_DIR = ROOT_DIR / "data" / "h2"

H2_TCP_PORT = os.getenv("H2_TCP_PORT", "9092")
H2_WEB_PORT = os.getenv("H2_WEB_PORT", "8082")


def main() -> None:
    if not H2_JAR.exists():
        print("No existe drivers/h2.jar")
        print("Ejecuta primero: python scripts/download_h2.py")
        sys.exit(1)

    H2_DATA_DIR.mkdir(parents=True, exist_ok=True)

    jdbc_url = f"jdbc:h2:tcp://localhost:{H2_TCP_PORT}/./factoring_platform"

    print("Levantando H2...")
    print(f"TCP: localhost:{H2_TCP_PORT}")
    print(f"Consola web: http://localhost:{H2_WEB_PORT}")
    print(f"JDBC URL: {jdbc_url}")
    print("Usuario: sa")
    print("Password: vacío")

    command = [
        "java",
        "-cp",
        str(H2_JAR),
        "org.h2.tools.Server",
        "-tcp",
        "-tcpPort",
        H2_TCP_PORT,
        "-web",
        "-webPort",
        H2_WEB_PORT,
        "-ifNotExists",
        "-baseDir",
        str(H2_DATA_DIR),
    ]

    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()