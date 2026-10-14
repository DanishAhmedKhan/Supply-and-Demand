
from pathlib import Path

ROOT = Path(__file__).parent
SOURCE = ROOT / "main.pine"
OUTPUT = ROOT / "dist" / "SupplyAndDemandZones.pine"


def build():
    content = SOURCE.read_text(encoding="utf-8")

    while True:
        lines = content.splitlines(keepends=True)
        include_found = False

        for index, line in enumerate(lines):
            marker = line.strip()

            if marker.startswith("// @include "):
                relative_path = marker[len("// @include "):].strip()
                include_path = ROOT / relative_path

                if not include_path.is_file():
                    raise FileNotFoundError(
                        f"Included file not found: {include_path}"
                    )

                included_content = include_path.read_text(encoding="utf-8")
                lines[index] = included_content.rstrip() + "\n"
                content = "".join(lines)
                include_found = True
                break

        if not include_found:
            break

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(content, encoding="utf-8")
    print(f"Build successful: {OUTPUT}")


if __name__ == "__main__":
    build()
