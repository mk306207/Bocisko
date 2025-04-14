from main import client
from unittest.mock import patch
import discord
from discord.ext import commands
from unittest.mock import MagicMock
import pytest
from unittest.mock import AsyncMock
from klucze import *
import sys
import asyncio

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

@pytest.mark.asyncio
async def test_fakePlayer(bot_client):
    mock_ctx = AsyncMock()
    mock_ctx.send = AsyncMock()
    testName = "Cristiano Ronaldo"
    command = bot_client.get_command('checkPlayer')
    await command(mock_ctx,name = testName)
    mock_ctx.send.assert_called_with(f"Player {testName} not found.")

@pytest.mark.asyncio
async def test_TOP10(bot_client):
    mock_ctx = AsyncMock()
    mock_ctx.send = AsyncMock()

    mock_player_data = {
        "results": [
            {
                "player": {"name": "Erling Haaland", "id": 101},
                "team": {"name": "Manchester City"}
            },
            {
                "player": {"name": "Mohamed Salah", "id": 102},
                "team": {"name": "Liverpool"}
            }
        ]
    }
    mock_single_player_data = (10, 5, 0)
    command = bot_client.get_command("TOP10_PL")

    with patch("main.scraper.PlayerData", return_value=mock_player_data), \
         patch("main.scraper.SinglePlayer", return_value=mock_single_player_data):
        
        await command(mock_ctx)

    mock_ctx.send.assert_any_call("1. Erling Haaland - Manchester City - G/A: 15\n")
    mock_ctx.send.assert_any_call("2. Mohamed Salah - Liverpool - G/A: 15\n")
    
@pytest.mark.asyncio
async def test_OnJoin(bot_client):
    mock_member = AsyncMock()
    mock_member.mention = "<@1234567890>"
    mock_member.name = "TestUser"
    mock_member.id = 1234567890
    mock_member.__radd__.side_effect = lambda other: other + mock_member.mention
    mock_channel = AsyncMock()
    mock_channel.send = AsyncMock()
    with patch.object(bot_client, "get_channel", return_value=mock_channel):
        await bot_client.on_member_join(mock_member)
    mock_channel.send.assert_called_once_with(f"Hello <@1234567890>")
    
@pytest.mark.asyncio
async def test_OnLeave(bot_client):
    mock_member = AsyncMock()
    mock_channel = AsyncMock()
    mock_channel.send = AsyncMock()
    with patch.object(bot_client, "get_channel",return_value = mock_channel):
        await bot_client.on_member_remove(mock_member)
    mock_channel.send.assert_called_once_with("Goodbye :(")