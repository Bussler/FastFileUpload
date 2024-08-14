import requests
from requests_toolbelt import MultipartEncoder

from fast_file_upload import logger

BASE_URL = "http://localhost:8001"


# Fastest way to upload large files
def upload_zip_file(path_to_zip: str) -> None:
    """Automatically create multipart formdata by reading the file as a stream and passing to the files field of the post request.

    Args:
        path_to_zip (str): path to the zip file to upload.
    """
    with open(path_to_zip, "rb") as f:
        create_response = requests.post(
            f"{BASE_URL}/",
            files=[
                (
                    "file",
                    (
                        "zip",
                        f,
                        "application/x-zip-compressed",
                    ),
                )
            ],
        )

        logger.info(f"Success: {create_response.text}")


# Best way to upload large files with less memory usage
def upload_zip_multipart_encoder(path_to_zip: str) -> None:
    """Create multipart formdata to pass to the data field of the post request.

    Args:
        path_to_zip (str): path to the zip file to upload.
    """
    encoder = MultipartEncoder(
        fields={"file": ("zip", open(path_to_zip, "rb"), "application/x-zip-compressed")}
    )
    response = requests.post(
        f"{BASE_URL}/", data=encoder, headers={"Content-Type": encoder.content_type}
    )
    logger.info(f"Success: {response.text}")


def main() -> None:
    # upload_zip_file("test.zip")
    upload_zip_multipart_encoder("test.zip")


if __name__ == "__main__":
    main()
