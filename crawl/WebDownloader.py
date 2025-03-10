import os
import random
import aiohttp
import asyncio
import aiofiles
from tqdm import tqdm
import UserAgent
import logging
from typing import Optional

logging.basicConfig(level=logging.ERROR)


class WebDownloader:
    def __init__(
        self,
        urls: list,
        save_dir: Optional[str] = None,
        workers: int = 8,
        min_delay: int = 1,
        max_delay: int = 5,
        connect_timeout: int = 10,
        read_timeout: int = 60,
    ):
        if min_delay > max_delay:
            raise ValueError(
                f"min_delay ({min_delay}) must be ≤ max_delay ({max_delay})"
            )
        self.urls = urls
        self.save_dir = save_dir or os.getcwd()
        self.workers = workers
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.timeout = aiohttp.ClientTimeout(
            connect=connect_timeout, sock_read=read_timeout
        )
        os.makedirs(self.save_dir, exist_ok=True)

    async def __download_file(self, session, url: str):
        max_retries = 3
        file_name = os.path.basename(url)

        for attempt in range(max_retries):
            try:
                await asyncio.sleep(random.uniform(self.min_delay, self.max_delay))
                ua = UserAgent.Random_User_Agents().get()
                headers = {
                    "User-Agent": ua,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                }

                async with session.get(
                    url, headers=headers, timeout=self.timeout
                ) as response:
                    if response.status != 200:
                        raise aiohttp.ClientError(f"HTTP error {response.status}")

                    save_path = self.__get_unique_path(file_name)
                    total_size = int(response.headers.get("content-length", 0))

                    with tqdm(
                        total=total_size,
                        unit="B",
                        unit_scale=True,
                        desc=file_name,
                        ascii=True,
                        leave=True,
                    ) as progress:
                        async with aiofiles.open(save_path, "wb") as f:
                            while True:
                                chunk = await response.content.read(8192)
                                if not chunk:
                                    break
                                await f.write(chunk)
                                progress.update(len(chunk))
                    return

            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = 2**attempt
                    logging.warning(
                        f"Retrying {file_name} in {wait_time}s... (attempt {attempt+1}/{max_retries})"
                    )
                    await asyncio.sleep(wait_time)
                else:
                    self.__handle_exception(file_name, e)

    def __handle_exception(self, file_name, e):
        error_msg = f"Failed to download {file_name}: {str(e)}"
        if isinstance(e, aiohttp.ClientError):
            if isinstance(e, aiohttp.ClientConnectionError):
                error_msg += " (Connection Error: Unable to connect to the server)"
            elif isinstance(e, aiohttp.ServerDisconnectedError):
                error_msg += " (Server Disconnected: The server closed the connection unexpectedly)"
            elif isinstance(e, aiohttp.ClientPayloadError):
                error_msg += " (Payload Error: Error in the response payload)"
            else:
                error_msg += " (Network/Server Error)"
        elif isinstance(e, asyncio.TimeoutError):
            error_msg += " (Timeout: The request exceeded the allowed time)"
        elif isinstance(e, aiohttp.ClientResponseError):
            error_msg += f" (HTTP Error {e.status}: {e.message})"
        elif isinstance(e, aiohttp.TooManyRedirects):
            error_msg += " (Too Many Redirects: The request exceeded the maximum number of redirects)"
        elif isinstance(e, aiohttp.ContentTypeError):
            error_msg += " (Content Type Error: The response content type does not match the expected type)"
        elif isinstance(e, ValueError):
            error_msg += " (Value Error: Invalid URL or other input error)"
        elif isinstance(e, TypeError):
            error_msg += " (Type Error: Incorrect data type encountered)"
        elif isinstance(e, OSError):
            error_msg += " (OS Error: Operating system-related error, such as file access issues)"
        elif isinstance(e, IOError):
            error_msg += " (I/O Error: Input/output error, such as file write failure)"
        else:
            error_msg += " (Unknown Error: An unexpected error occurred)"

        logging.error(error_msg)

    def __get_unique_path(self, file_name):
        base, ext = os.path.splitext(file_name)
        counter = 1
        while True:
            path = os.path.join(self.save_dir, file_name)
            if not os.path.exists(path):
                return path
            file_name = f"{base}_{counter}{ext}"
            counter += 1

    async def __run_downloads(self):
        connector = aiohttp.TCPConnector(limit=self.workers)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [self.__download_file(session, url) for url in self.urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            failed = sum(1 for r in results if isinstance(r, Exception))
            if failed:
                logging.error(f"Download completed with {failed} errors")

    def start(self):
        asyncio.run(self.__run_downloads())


# 使用示例
if __name__ == "__main__":
    urls = [
        "https://www.modelscope.cn/models/Qwen/Qwen2.5-7B-Instruct/resolve/master/.gitattributes",
        "https://www.modelscope.cn/models/Qwen/Qwen2.5-7B-Instruct/resolve/master/config.json",
        "https://www.modelscope.cn/models/Qwen/Qwen2.5-7B-Instruct/resolve/master/configuration.json",
        "https://www.modelscope.cn/models/Qwen/Qwen2.5-7B-Instruct/resolve/master/generation_config.json",
        "https://www.modelscope.cn/models/Qwen/Qwen2.5-7B-Instruct/resolve/master/LICENSE",
        "https://www.modelscope.cn/models/Qwen/Qwen2.5-7B-Instruct/resolve/master/merges.txt",
        "https://www.modelscope.cn/models/Qwen/Qwen2.5-7B-Instruct/resolve/master/model-00001-of-00004.safetensors",
        "https://www.modelscope.cn/models/Qwen/Qwen2.5-7B-Instruct/resolve/master/model-00002-of-00004.safetensors",
        "https://www.modelscope.cn/models/Qwen/Qwen2.5-7B-Instruct/resolve/master/model-00003-of-00004.safetensors",
        "https://www.modelscope.cn/models/Qwen/Qwen2.5-7B-Instruct/resolve/master/model-00004-of-00004.safetensors",
        "https://www.modelscope.cn/models/Qwen/Qwen2.5-7B-Instruct/resolve/master/model.safetensors.index.json",
        "https://www.modelscope.cn/models/Qwen/Qwen2.5-7B-Instruct/resolve/master/README.md",
        "https://www.modelscope.cn/models/Qwen/Qwen2.5-7B-Instruct/resolve/master/tokenizer.json",
        "https://www.modelscope.cn/models/Qwen/Qwen2.5-7B-Instruct/resolve/master/tokenizer_config.json",
        "https://www.modelscope.cn/models/Qwen/Qwen2.5-7B-Instruct/resolve/master/vocab.json",
    ]

    downloader = WebDownloader(
        urls=urls,
        save_dir="LLM/Qwen2.5-7B",
        workers=6,
        min_delay=1,
        max_delay=5,
        connect_timeout=15,
        read_timeout=300,
    )
    downloader.start()
