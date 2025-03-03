from main import client
from unittest.mock import patch
import discord
from discord.ext import commands
from unittest.mock import MagicMock
import pytest
from unittest.mock import AsyncMock
from klucze import *
import sys

@pytest.fixture
def bot_client():
    with patch.object(commands.Bot, 'run'):
        yield client
        
@pytest.mark.asyncio
async def test_ping_command(bot_client):
            
        mock_ctx = AsyncMock()
        mock_ctx.send = AsyncMock()

        command = bot_client.get_command('hello')
        await command(mock_ctx)

        mock_ctx.send.assert_called_with("Hi!")
