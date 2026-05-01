from pathlib import Path
from urllib.request import urlretrieve

H2_VERSION = "2.4.240"
H2_URL = f"https://repo1.maven.org/maven2/com/h2database/h2/{H2_VERSION}/h2-{H2_VERSION}.jar"

ROOT_DIR = Path(__file__).resolve().parents[1]
DRIVERS_DIR = ROOT_DIR / "drivers"
H2_JAR = DRIVERS_DIR / "h2.jar"


def main() -> None:
    DRIVERS_DIR.mkdir(parents=True, exist_ok=True)

    if H2_JAR.exists():
        print(f"El driver ya existe en: {H2_JAR}")
        return

    print(f"Descargando H2 {H2_VERSION}...")
    urlretrieve(H2_URL, H2_JAR)
    print(f"Driver descargado en: {H2_JAR}")


if __name__ == "__main__":
    main()