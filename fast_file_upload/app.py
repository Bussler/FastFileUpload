import uvicorn
from fastapi import FastAPI, UploadFile

app = FastAPI()


@app.get("/")
async def say_hello() -> str:
    return "Success! Connection is working."


@app.post("/")
async def file_upload(
    file: UploadFile,
) -> str:

    file_contents = file.file.read()
    return "Success! File uploaded."


def main() -> None:
    uvicorn.run("fast_file_upload.app:app", host="localhost", port=8001, reload=True)


if __name__ == "__main__":
    main()
