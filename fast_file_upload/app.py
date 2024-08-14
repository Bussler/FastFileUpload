import uvicorn
from fastapi import FastAPI

from fast_file_upload import logger

app = FastAPI()


@app.get("/hello")
async def say_hello() -> str:
    return "Success! Connection is working."


def main() -> None:
    uvicorn.run("fast_file_upload.app:app", host="localhost", port=8001, reload=True)


if __name__ == "__main__":
    main()
