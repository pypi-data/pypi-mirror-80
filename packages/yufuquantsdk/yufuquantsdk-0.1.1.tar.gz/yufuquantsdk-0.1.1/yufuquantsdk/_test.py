import logging
from pprint import pprint

from yufuquantsdk.clients import RESTAPIClient

# 开启日志
logger = logging.getLogger("yufuquantsdk")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


async def main():
    http_client = RESTAPIClient(
        base_url="https://demo.yufuquant.cc/api/v1",
        auth_token="472b6c269f7e84402ca8097d751fff92110bfb41",
    )

    result = await http_client.get_robot_config(robot_id=1)
    pprint(result)

    result = await http_client.post_robot_ping(robot_id=1)
    pprint(result)

    result = await http_client.patch_robot_asset_record(
        robot_id=1, data={"total_balance": 10000}
    )
    pprint(result)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
