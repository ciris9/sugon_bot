class ApiDatapack:
    def __init__(self, guild_id):
        self.api_datapack = {

            "url": f"/guilds/{guild_id}/api_permission/demand",
            "datapack":
                {
                    "channel_id": "123456",
                    "api_identify": {
                        "path": " ",
                        "method": "GET"
                    },
                    "desc": "显示频道信息"
                }

        }

        self.api_url = {
            "get_roles_list":
                {
                    "url": f"/guilds/{guild_id}/roles",
                    "desc": "获取频道身份组列表"
                },
            "get_power_list":
                {
                    "url": f"/guilds/{guild_id}/api_permission",
                    "desc": "获取权限列表"
                }

        }
