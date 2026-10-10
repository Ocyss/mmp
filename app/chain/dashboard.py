from typing import TYPE_CHECKING, List, Optional

from app.chain import ChainBase

if TYPE_CHECKING:
    from app import schemas


class DashboardChain(ChainBase):
    """
    各类仪表板统计处理链
    """

    def media_statistic(self, server: str | None = None) -> list[schemas.Statistic] | None:
        """
        媒体数量统计
        """
        return self.run_module("media_statistic", server=server)

    def downloader_info(self, downloader: str | None = None) -> list[schemas.DownloaderInfo] | None:
        """
        下载器信息
        """
        return self.run_module("downloader_info", downloader=downloader)
