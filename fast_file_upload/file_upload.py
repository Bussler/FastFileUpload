import requests

from fast_file_upload import logger

BASE_URL = "http://localhost:8001"


# Fastest way to upload small files
def upload_zip_file_small(path_to_zip: str) -> None:
    """Automatically create multipart formdata by reading the file as a stream and passing to the files field of the post request.

    Args:
        path_to_zip (str): path to the zip file to upload.
    """
    with open(path_to_zip, "rb") as f:
        create_response = requests.post(
            f"{BASE_URL}/small_file_upload/",
            files=[
                (
                    "file",
                    (
                        "test_small.zip",
                        f,
                        "application/x-zip-compressed",
                    ),
                )
            ],
        )

        logger.info(f"Success: {create_response.text}")


# Fastest way to upload large files
def upload_zip_file_big(path_to_zip: str) -> None:
    """Automatically create multipart formdata by reading the file as a stream and passing to the files field of the post request.

    Args:
        path_to_zip (str): path to the zip file to upload.
    """
    with open(path_to_zip, "rb") as f:
        create_response = requests.post(
            f"{BASE_URL}/large_file_upload/",
            files={"file": f},
            headers={"Filename": "test_big.zip"},
        )

        logger.info(f"Success: {create_response.text}")


def main() -> None:
    upload_zip_file_small("data/test_small.zip")
    # upload_zip_file_big("data/test_big.zip")


if __name__ == "__main__":
    main()
