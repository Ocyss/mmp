from types import SimpleNamespace
from unittest.mock import patch

from app.chain.subscribe import SubscribeChain


def _make_chain() -> SubscribeChain:
    """绕过 ChainBase 初始化构造订阅链实例。"""
    return SubscribeChain.__new__(SubscribeChain)


def _subscribe(**overrides):
    defaults = {
        "id": 1,
        "name": "仙逆",
        "type": "电视剧",
        "tmdbid": 223911,
        "season": 1,
        "note": [],
    }
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def test_sync_skips_when_server_unavailable():
    """媒体服务器查询失败（None）时不写任何 note。"""
    chain = _make_chain()
    subscribes = [_subscribe()]
    with (
        patch("app.chain.subscribe.SubscribeOper") as subscribe_oper,
        patch("app.chain.subscribe.MediaServerChain") as ms_chain,
        patch.object(SubscribeChain, "backfill_existing_episodes") as backfill,
    ):
        subscribe_oper.return_value.list.return_value = subscribes
        ms_chain.return_value.tv_episodes_by_tmdb.return_value = None
        chain.sync_existing_episodes_from_mediaserver(["emby"])
    backfill.assert_not_called()


def test_sync_backfills_existing_episodes():
    """媒体服务器已有集应补写为订阅 note，不连续集同样以 note 记录。"""
    chain = _make_chain()
    subscribes = [_subscribe()]
    with (
        patch("app.chain.subscribe.SubscribeOper") as subscribe_oper,
        patch("app.chain.subscribe.MediaServerChain") as ms_chain,
        patch.object(SubscribeChain, "backfill_existing_episodes") as backfill,
    ):
        subscribe_oper.return_value.list.return_value = subscribes
        ms_chain.return_value.tv_episodes_by_tmdb.return_value = {1: [1, 2, 5, 7], 2: [1]}
        backfill.return_value = {"accepted": [5, 7]}
        chain.sync_existing_episodes_from_mediaserver(["emby"])
    backfill.assert_called_once()
    kwargs = backfill.call_args.kwargs
    assert kwargs["subscribe"] is subscribes[0]
    assert kwargs["episodes"] == [1, 2, 5, 7]
    assert kwargs["scene"] == "mediaserver_sync"


def test_sync_merges_episodes_across_servers():
    """多个媒体服务器的同一季集数应取并集。"""
    chain = _make_chain()
    subscribes = [_subscribe()]
    with (
        patch("app.chain.subscribe.SubscribeOper") as subscribe_oper,
        patch("app.chain.subscribe.MediaServerChain") as ms_chain,
        patch.object(SubscribeChain, "backfill_existing_episodes") as backfill,
    ):
        subscribe_oper.return_value.list.return_value = subscribes
        ms_chain.return_value.tv_episodes_by_tmdb.side_effect = [{1: [1, 2]}, {1: [2, 3]}]
        backfill.return_value = {"accepted": [3]}
        chain.sync_existing_episodes_from_mediaserver(["emby", "jellyfin"])
    assert backfill.call_args.kwargs["episodes"] == [1, 2, 3]


def test_sync_skips_non_tv_or_missing_tmdb():
    """电影订阅或缺少 TMDB ID 的订阅不参与已有集同步。"""
    chain = _make_chain()
    subscribes = [
        _subscribe(id=2, type="电影"),
        _subscribe(id=3, tmdbid=None),
    ]
    with (
        patch("app.chain.subscribe.SubscribeOper") as subscribe_oper,
        patch("app.chain.subscribe.MediaServerChain") as ms_chain,
        patch.object(SubscribeChain, "backfill_existing_episodes") as backfill,
    ):
        subscribe_oper.return_value.list.return_value = subscribes
        chain.sync_existing_episodes_from_mediaserver(["emby"])
    ms_chain.return_value.tv_episodes_by_tmdb.assert_not_called()
    backfill.assert_not_called()


def test_sync_skips_when_no_episode_exists():
    """媒体服务器无该季任何集时不触发回写。"""
    chain = _make_chain()
    subscribes = [_subscribe()]
    with (
        patch("app.chain.subscribe.SubscribeOper") as subscribe_oper,
        patch("app.chain.subscribe.MediaServerChain") as ms_chain,
        patch.object(SubscribeChain, "backfill_existing_episodes") as backfill,
    ):
        subscribe_oper.return_value.list.return_value = subscribes
        ms_chain.return_value.tv_episodes_by_tmdb.return_value = {1: []}
        chain.sync_existing_episodes_from_mediaserver(["emby"])
    backfill.assert_not_called()
