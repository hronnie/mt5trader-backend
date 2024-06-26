from dao.basePlatformDAO import BasePlatformDAO
from dao.mt5CommonDAO import Mt5CommonDAO

class DAOFactory:

    @staticmethod
    def getDAO(platform: str) -> BasePlatformDAO:
        if platform == 'mt5':
            return Mt5CommonDAO()
        # elif platform == 'ctrader':
        #    return CTraderDAO()
        else:
            raise ValueError(f"Unknown platform: {platform}")
