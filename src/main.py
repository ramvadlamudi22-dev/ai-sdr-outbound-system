from pathlib import Path


def main():
    project_root = Path(__file__).resolve().parent.parent
    print("AI SDR Outbound System")
    print("Project scaffold ready")
    print(f"Root: {project_root}")


if __name__ == "__main__":
    main()
