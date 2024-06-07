from dao.basePlatformDAO import BasePlatformDAO
from dao.mt5DAO import Mt5DAO

class DAOFactory:

    @staticmethod
    def getDAO(platform: str) -> BasePlatformDAO:
        if platform == 'mt5':
            return Mt5DAO()
        # elif platform == 'ctrader':
        #    return CTraderDAO()
        else:
            raise ValueError(f"Unknown platform: {platform}")
