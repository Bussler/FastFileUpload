import requests

BASE_URL = "http://localhost:8001"


def upsert_version_zip_file(path_to_zip: str) -> None:
    with open(path_to_zip, "rb") as f:
        files = [
            (
                "file",
                (
                    "zip",
                    f,
                    "application/x-zip-compressed",
                ),
            )
        ]
        create_response = requests.post(f"{BASE_URL}/", files=files)
        print(f"Success: {create_response.text}")


def main() -> None:
    upsert_version_zip_file("test.zip")


if __name__ == "__main__":
    main()
