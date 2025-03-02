import time
from pathlib import Path
from pybootstrapui.components.progress import ProgressBar


def format_size(size):
    """Format size."""
    if size >= 1 << 30:
        return f"{size / (1 << 30):.2f} GB"
    elif size >= 1 << 20:
        return f"{size / (1 << 20):.2f} MB"
    elif size >= 1 << 10:
        return f"{size / (1 << 10):.2f} KB"
    return f"{size} B"


async def download_file(
    file_url: str,
    end_path: str | Path,
    progressbar: ProgressBar | None = None,
    progressbar_format: str = "{percentage}% - {downloaded_size} - {download_speed}",
):
    """Download a file asynchronously with an optional progress bar.

    Args:
        file_url (str): The URL of the file to download.
        end_path (str | Path): The local file path where the downloaded file will be saved.
        progressbar (ProgressBar | None, optional): An optional progress bar to visualize the download progress.
        progressbar_format (str, optional): A format string to customize progress display.

    Raises:
        httpx.HTTPStatusError: If the HTTP request fails.
        IOError: If file writing encounters an error.

    Example:
        await download_file(
            file_url='https://example.com/file.zip',
            end_path='downloads/file.zip',
            progressbar=my_progress_bar,
            progressbar_format='{percentage}% - {downloaded_size} - {download_speed}'
        )
    """

    import httpx
    import aiofiles

    end_path = Path(end_path)
    end_path.parent.mkdir(parents=True, exist_ok=True)

    async with httpx.AsyncClient() as client:
        async with client.stream("GET", file_url) as response:
            response.raise_for_status()
            total_size = int(response.headers.get("Content-Length", 0))
            if progressbar:
                progressbar.change_value(
                    0,
                    progressbar_format.format(
                        percentage=0, downloaded_size="0 KB", download_speed="0 KB/s"
                    ),
                )

            async with aiofiles.open(end_path, "wb") as file:
                downloaded_size = 0
                start_time = time.time()

                async for chunk in response.aiter_bytes(chunk_size=8192):
                    await file.write(chunk)
                    downloaded_size += len(chunk)
                    elapsed_time = time.time() - start_time
                    speed = downloaded_size / elapsed_time if elapsed_time > 0 else 0

                    if total_size > 0:
                        percent_complete = (downloaded_size / total_size) * 100
                        if progressbar:
                            progressbar.change_value(
                                percent_complete,
                                progressbar_format.format(
                                    percentage=f"{percent_complete:.2f}",
                                    downloaded_size=format_size(downloaded_size),
                                    download_speed=f"{format_size(speed)}/s",
                                ),
                            )

            if progressbar:
                progressbar.change_value(
                    100,
                    progressbar_format.format(
                        percentage="100.00",
                        downloaded_size=format_size(downloaded_size),
                        download_speed="Completed",
                    ),
                )
