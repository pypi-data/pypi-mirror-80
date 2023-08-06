import asyncio

from feishu import FeishuClient

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
cli = FeishuClient(run_async=False)
cli_async = FeishuClient(run_async=True)


def sometest():
    result = cli.get_bot_info()
    # result = loop.run_until_complete(cli_async.list_chat_all())
    print(result)


if __name__ == "__main__":
    sometest()
