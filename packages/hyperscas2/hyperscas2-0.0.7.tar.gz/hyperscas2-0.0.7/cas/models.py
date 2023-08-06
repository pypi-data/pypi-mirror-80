import logging
import requests
from .domain import Domain
from .cache import cacheByTime
from django.contrib.auth import get_user_model

logger = logging.getLogger("cas")


@cacheByTime()
def getHacIdMap():
    domain = Domain.get()
    url = f"{domain.hac.url}/api/admin/users"
    response = requests.get(url, headers=domain.hac.identify, verify=False)
    try:
        result = response.json()
        items = result.get("result", {}).get("items", [])
    except Exception:
        items = []
        logger.error(f"Error Response From HAC: {response.text}")
    return {x["email"]: x["id"] for x in items}


def getHacId(self):
    hac_id = getHacIdMap().get(self.email, 0)
    if not hac_id:
        logger.debug("%s hac id 为空" % self.email)
    return hac_id


User = get_user_model()
User.hacId = property(getHacId)
