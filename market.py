from serverside import *
import json
import squawker_errors
from utils import get_logger

logger = get_logger('squawker_market')

HEADERS = [
    'text',
    'sender',
    'adType',
    'txType',
    'txDatas',
    'title',
    'asset',
    'qt',
    'orders',
    'price',
    'price_asset',
    'link',
    'desc',
    'keywords',
    'channel',
    'sqp2p_ver'
]


class Listing:
    def __init__(self, tx):
        # tx is { address, message, block }
        if isinstance(tx, dict):
            self.tx = tx
        else:
            self.tx = json.loads(tx)
        try:
            self.raw_message = json.loads(self.get_raw_message())
            self.text = self.get_raw_msg_attr("desc")
            if isinstance(self.tx["address"], list):
                self.sender = self.tx["address"][0]
            else:
                self.sender = self.tx["address"]
            self.adType = self.get_raw_msg_attr('type')
            self.txType = self.get_raw_msg_attr('txType')
            self.txDatas = self.get_raw_msg_attr('txDatas')
            self.title = self.get_raw_msg_attr('title')
            self.asset = self.get_raw_msg_attr('asset')
            self.qt = self.get_raw_msg_attr('qt')
            self.orders = self.get_raw_msg_attr('orders')
            self.price = self.get_raw_msg_attr('price')
            self.price_asset = self.get_raw_msg_attr('price_asset')
            self.link = self.get_raw_msg_attr('link')
            self.desc = self.get_raw_msg_attr('desc')
            self.keywords = self.get_raw_msg_attr('keywords')
            self.channel = self.get_raw_msg_attr('channel')
            self.sqp2p_ver = self.get_raw_msg_attr('sqp2p_ver')
        except Exception as e:
            logger.info(f"failed building listing {tx} only loaded {self.__dict__}")
            raise squawker_errors.NotListing(
                f"No listing got exception {type(e)} {e} from {self.__dict__}")
        logger.info(f"built listing {str(self)}")

    def get_raw_message(self):
        try:
            ipfs_hash = self.tx["message"]
            ipfs_data = ipfs.cat(ipfs_hash)
            logger.info(f"listing {ipfs_hash}")
            logger.info(f"listing {ipfs_hash} is {ipfs_data}")
            œlogger.info(f"raw message is {raw_message} of type {type(raw_message)}")
            logger.info(f"json raw message is {json.loads(str(raw_message))} ")
            return raw_message
        except squawker_errors.NotMessage as e:
            raise squawker_errors.NotMessage(str(e))
        except Exception as e:
            # print(type(e), e)
            pass

    def get_raw_msg_attr(self, attr):
        try:
            logger.info(f"get raw_message is {self.raw_message} attribute is {attr} in {type(self.raw_message)}")
            logger.info("'"+self.raw_message.replace("'", '"')+"'")
            returnable =  eval(self.raw_message)[attr]
            logger.info(f"loaded {returnable}")
            return returnable
        except Exception as e:
            logging.info(f"got {e} trying to get raw attribute")
            return ""

    def __str__(self, headers=HEADERS):
        out = ""
        for aspect in headers:
            out += f"""{aspect}: {self.__dict__[aspect]}
"""
        return out

    def html(self, headers=HEADERS):
        logger.info(f"loading {self}")
        out = "<tr>"
        for aspect in headers:
            out += f"<td>{self.__dict__[aspect]}</td>"
        out += "</tr>"
        logger.info(f"output is {out}")
        return out
