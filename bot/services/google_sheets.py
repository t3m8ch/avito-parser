from typing import Iterable

from bot.misc.models import AdModel
from gspread_asyncio import AsyncioGspreadClientManager


class GoogleSheetsService:
    def __init__(self, spreadsheet_client_manager: AsyncioGspreadClientManager):
        self._spreadsheet_client_manager = spreadsheet_client_manager

    async def get_url_to_ads_spreadsheet(self, ads: Iterable[AdModel]) -> str:
        spreadsheet_client = await self._spreadsheet_client_manager.authorize()

        spreadsheet = await spreadsheet_client.create("Ваши подписки")
        spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet.id}"

        await spreadsheet_client.insert_permission(
            file_id=spreadsheet.id,
            value=None,
            perm_type="anyone",
            role="writer"
        )

        worksheet = await spreadsheet.get_worksheet(0)
        
        await worksheet.insert_row(["Загаловок", "Цена", "Адрес"])
        await worksheet.insert_rows([
            [ad.title, str(ad.price) if ad.price else "", ad.url]
            for ad in ads
        ], row=2)
        
        return spreadsheet_url
