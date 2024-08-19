import os

import aiofiles
import uvicorn
from fastapi import FastAPI, HTTPException, Request, UploadFile, status
from streaming_form_data import StreamingFormDataParser
from streaming_form_data.targets import FileTarget

app = FastAPI()


@app.get("/")
async def say_hello() -> str:
    return "Success! Connection is working."


@app.post("/small_file_upload/")
async def small_file_upload(
    file: UploadFile,
) -> int:
    """Read file in as Upload file and save it to a file async.

    Pro: Get good swagger documentation with UploadFile.
    Con: Slow, since Upload File is spooled and has to be loaded to memory first before saving.
    """

    file_contents = await file.read()
    async with aiofiles.open(f"{file.filename}", "wb") as out_file:
        await out_file.write(file_contents)
    return status.HTTP_200_OK


@app.post("/large_file_upload/")
async def large_file_upload(request: Request) -> int:
    """Read filedata as a stream from requests and save it to a file.
    Pro: Stream data directly to file, so no memory overhead.
    Con: Bad documentation and error handling, since data has to be parsed from request body.
    """

    filename = request.headers.get("Filename")

    if not filename:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Filename header is missing"
        )

    try:
        filepath = os.path.join("./", os.path.basename(filename))
        file_ = FileTarget(filepath)  # stream to load into file
        # data = ValueTarget() # stream to load into memory
        parser = StreamingFormDataParser(headers=request.headers)
        parser.register("file", file_)
        # parser.register('data', data)
        async for chunk in request.stream():
            parser.data_received(chunk)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return status.HTTP_200_OK


def main() -> None:
    uvicorn.run("fast_file_upload.app:app", host="localhost", port=8001, reload=True)


if __name__ == "__main__":
    main()
