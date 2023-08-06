import io
import json
from PIL import Image, UnidentifiedImageError
import requests
from typing import Generator as Gen, List, Union
from .auth import AuthBearer
from .utils import api_request


class _iFunnyBaseAPI:
    """Private API class, only interacts with iFunny API endpoints"""

    BASE = "https://api.ifunny.mobi/v4"

    def __init__(self, token: str):
        self.token = token
        self.auth = AuthBearer(self.token)

    @api_request
    def _get(self, path: str, **kwargs) -> dict:
        r = requests.get(iFunnyAPI.BASE + path, auth=self.auth, **kwargs)
        return r.json()

    @api_request
    def _post(self, path: str, **kwargs) -> dict:
        r = requests.post(iFunnyAPI.BASE + path, auth=self.auth, **kwargs)
        return r.json()

    @api_request
    def _put(self, path: str, **kwargs) -> dict:
        r = requests.put(iFunnyAPI.BASE + path, auth=self.auth, **kwargs)
        return r.json()

    @api_request
    def _delete(self, path: str, **kwargs) -> dict:
        r = requests.delete(iFunnyAPI.BASE + path, auth=self.auth, **kwargs)
        return r.json()

    @property
    def account(self) -> dict:
        r = self._get("/account")
        return r["data"]

    def _get_paging_items(self, path: str, label: str,
                          limit: int = None) -> List[dict]:

        def get_next(r) -> int:
            return r["data"][label]["paging"]["cursors"]["next"]

        def has_next(r) -> bool:
            return r["data"][label]["paging"]["hasNext"]

        def get_items(r) -> list:
            return r["data"][label]["items"]

        path += "?limit=100"
        batch = self._get(path)
        items = get_items(batch)
        if not has_next(batch):
            return items
        while has_next(batch := self._get(f"{path}&next={get_next(batch)}")):
            items.extend(get_items(batch))
        items.extend(get_items(batch))
        return items

    def my_activity(self, limit: int = None) -> List[dict]:
        return self._get_paging_items(
            f"/news/my",
            "news",
            limit
        )

    def my_comments(self, limit: int = None) -> List[dict]:
        return self._get_paging_items(
            f"/users/my/comments",
            "comments",
            limit
        )

    def user_subscribers(self, *, user_id, limit: int = None) -> List[dict]:
        return self._get_paging_items(
            f"/users/{user_id}/subscribers",
            "users",
            limit
        )

    def user_subscriptions(self, *, user_id, limit: int = None) -> List[dict]:
        return self._get_paging_items(
            f"/users/{user_id}/subscriptions",
            "users",
            limit
        )

    def user_posts(self, *, user_id, limit: int = None) -> List[dict]:
        return self._get_paging_items(
            f"/timelines/users/{user_id}",
            "content",
            limit
        )

    def user_by_nick(self, nick: str) -> dict:
        return self._get(f"/users/by_nick/{nick}")

    def featured(self, *, limit: Union[int, None], read=True
                 ) -> Gen[dict, None, None]:
        iterator = iter(int, 1) if limit is None else range(limit)
        for _ in iterator:
            r = self._get("/feeds/featured?limit=1")
            feat = r["data"]["content"]["items"][0]
            if read:
                self._put(f"/reads/{feat['id']}?from=feat",
                          headers={"User-Agent": "*"})
            yield feat

    def collective(self, *, limit: Union[int, None]) -> Gen[dict, None, None]:
        iterator = iter(int, 1) if limit is None else range(limit)
        for _ in iterator:
            r = self._post("/feeds/collective?limit=1")
            coll = r["data"]["content"]["items"][0]
            yield coll

    def subscriptions(self, *, limit: Union[int, None], read=True
                      ) -> Gen[dict, None, None]:
        iterator = iter(int, 1) if limit is None else range(limit)
        for _ in iterator:
            r = self._get("/timelines/home?limit=1")
            subscr = r["data"]["content"]["items"][0]
            if read:
                self._put(f"/reads/{subscr['id']}?from=subs",
                          headers={"User-Agent": "*"})
            yield subscr

    def popular(self, *, limit: Union[int, None]) -> Gen[dict, None, None]:
        iterator = iter(int, 1) if limit is None else range(limit)
        for _ in iterator:
            r = self._get("/feeds/popular?limit=1")
            pop = r["data"]["content"]["items"][0]
            yield pop

    def upload(self, media: Union[bytes, str], description: str = None,
               tags: list = None, public: bool = True):
        media = media if type(media) is bytes else open(media, "rb").read()
        try:
            im = Image.open(io.BytesIO(media))
            mtype = "gif" if im.format == "GIF" else "pic"
            ftype = "image"
        except UnidentifiedImageError:
            mtype = "video_clip"
            ftype = "video"
        self._post(
            "/content",
            data={"description": description or "",
                  "tags": json.dumps(tags or []),
                  "type": mtype,
                  "visibility": "public" if public else "subscribers"},
            files={ftype: media}
        )

    def smile_post(self, *, post_id: str):
        self._put(f"/content/{post_id}/smiles?from=feat")

    def unsmile_post(self, *, post_id: str):
        self._delete(f"/content/{post_id}/smiles?from=feat")

    def delete_post(self, *, post_id: str):
        self._delete(f"/content/{post_id}")

    def comment(self, comment: str, *, post_id: str):
        self._post(
            f"/content/{post_id}/comments?from=feat",
            data={"text": comment}
        )

    def reply(self, reply: str, *, post_id: str, comment_id: str):
        self._post(
            f"/content/{post_id}/comments/{comment_id}/replies",
            data={"text": reply}
        )

    def smile_comment(self, *, post_id: str, comment_id: str):
        self._put(f"/content/{post_id}/comments/{comment_id}/smiles")

    def unsmile_comment(self, *, post_id: str, comment_id: str):
        self._delete(f"/content/{post_id}/comments/{comment_id}/smiles")

    def delete_comment(self, *, post_id: str, comment_id: str):
        self._delete(f"/content/{post_id}/comments/{comment_id}")

    def is_nick_available(self, nick: str):
        j = self._get(f"/users/nicks_available?nick={nick}")
        return j["data"]["available"]

    def is_email_available(self, email: str) -> bool:
        j = self._get(f"/users/emails_available?email={email}")
        return j["data"]["available"]


class iFunnyAPI(_iFunnyBaseAPI):
    """Public API class, including extra features"""

    @property
    def pfp(self) -> Image:
        url = self.account["photo"]["url"]
        return Image.open(requests.get(url, stream=True).raw)

    @classmethod
    def crop_watermark(cls, im: Image) -> Image:
        w, h = im.size
        return im.crop((0, 0, w, h - 20))
