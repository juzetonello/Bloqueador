# -*- coding: utf-8 -*-
"""
Bloqueador de Entretenimento/Jogos - Laboratórios Escolares
Windows 10/11

Uso:
    python bloqueador_escola.py install
    python bloqueador_escola.py remove
    python bloqueador_escola.py status

O programa:
- cria backup do HOSTS antes da primeira alteração;
- adiciona somente uma seção própria, delimitada por marcadores;
- não apaga regras existentes fora da seção;
- usa 0.0.0.0, conforme prática comum para hosts;
- limpa o cache DNS ao instalar/remover.

IMPORTANTE:
O arquivo HOSTS do Windows NÃO aceita curingas como *.roblox.com.
Por isso a lista contém nomes exatos. Para bloquear subdomínios
dinâmicos em escala, prefira DNS filtering/proxy/firewall.
"""

import ctypes
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

HOSTS = Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32" / "drivers" / "etc" / "hosts"
BACKUP_DIR = HOSTS.parent / "hosts_backups_escola"
MARK_BEGIN = "# >>> BLOQUEIO ESCOLAR - INICIO >>>"
MARK_END = "# <<< BLOQUEIO ESCOLAR - FIM <<<"
BLOCK_IP = "0.0.0.0"

DOMAINS = [
    # ROBLOX
    'roblox.com',
    # ROBLOX
    'www.roblox.com',
    # ROBLOX
    'web.roblox.com',
    # ROBLOX
    'create.roblox.com',
    # ROBLOX
    'developer.roblox.com',
    # ROBLOX
    'api.roblox.com',
    # ROBLOX
    'auth.roblox.com',
    # ROBLOX
    'games.roblox.com',
    # ROBLOX
    'gameinternational.roblox.com',
    # ROBLOX
    'avatar.roblox.com',
    # ROBLOX
    'catalog.roblox.com',
    # ROBLOX
    'friends.roblox.com',
    # ROBLOX
    'groups.roblox.com',
    # ROBLOX
    'inventory.roblox.com',
    # ROBLOX
    'notifications.roblox.com',
    # ROBLOX
    'presence.roblox.com',
    # ROBLOX
    'thumbnails.roblox.com',
    # ROBLOX
    'trades.roblox.com',
    # ROBLOX
    'economy.roblox.com',
    # ROBLOX
    'chat.roblox.com',
    # ROBLOX
    'voice.roblox.com',
    # ROBLOX
    'setup.roblox.com',
    # ROBLOX
    'download.roblox.com',
    # ROBLOX
    'status.roblox.com',
    # ROBLOX
    'blog.roblox.com',
    # FREE_FIRE_GARENA
    'freefiremobile.com',
    # FREE_FIRE_GARENA
    'ff.garena.com',
    # FREE_FIRE_GARENA
    'garena.com',
    # FREE_FIRE_GARENA
    'garena.co.id',
    # FREE_FIRE_GARENA
    'garena.sg',
    # FREE_FIRE_GARENA
    'garena.tw',
    # FREE_FIRE_GARENA
    'garena.ph',
    # FREE_FIRE_GARENA
    'garena.vn',
    # FREE_FIRE_GARENA
    'garena.my',
    # FREE_FIRE_GARENA
    'garena.co.th',
    # FREE_FIRE_GARENA
    'garena.in',
    # FREE_FIRE_GARENA
    'garenanow.com',
    # FREE_FIRE_GARENA
    'garena.com.br',
    # FREE_FIRE_GARENA
    'freefire.com',
    # FREE_FIRE_GARENA
    'freefiremobile.com.br',
    # FORTNITE_EPIC
    'fortnite.com',
    # FORTNITE_EPIC
    'www.fortnite.com',
    # FORTNITE_EPIC
    'epicgames.com',
    # FORTNITE_EPIC
    'www.epicgames.com',
    # FORTNITE_EPIC
    'store.epicgames.com',
    # FORTNITE_EPIC
    'launcher-website-prod07.ol.epicgames.com',
    # FORTNITE_EPIC
    'epicgames.dev',
    # FORTNITE_EPIC
    'unrealengine.com',
    # FORTNITE_EPIC
    'fortniteapi.io',
    # FORTNITE_EPIC
    'fortniteapi.com',
    # FORTNITE_EPIC
    'epicgamescdn.com',
    # FORTNITE_EPIC
    'epicgamescdn.net',
    # STEAM_VALVE
    'steampowered.com',
    # STEAM_VALVE
    'store.steampowered.com',
    # STEAM_VALVE
    'steamcommunity.com',
    # STEAM_VALVE
    'steamgames.com',
    # STEAM_VALVE
    'steamcdn-a.akamaihd.net',
    # STEAM_VALVE
    'steamcontent.com',
    # STEAM_VALVE
    'steamstatic.com',
    # STEAM_VALVE
    'steam-chat.com',
    # STEAM_VALVE
    'steamdb.info',
    # STEAM_VALVE
    'steamcharts.com',
    # STEAM_VALVE
    'steamgifts.com',
    # STEAM_VALVE
    'steampowered.net',
    # STEAM_VALVE
    'valvesoftware.com',
    # STEAM_VALVE
    'counter-strike.net',
    # STEAM_VALVE
    'dota2.com',
    # STEAM_VALVE
    'dota2.com.cn',
    # STEAM_VALVE
    'artifactgame.com',
    # STEAM_VALVE
    'underlords.com',
    # STEAM_VALVE
    'half-life.com',
    # STEAM_VALVE
    'teamfortress.com',
    # STEAM_VALVE
    'left4dead.com',
    # STEAM_VALVE
    'portal2.com',
    # RIOT_GAMES
    'riotgames.com',
    # RIOT_GAMES
    'leagueoflegends.com',
    # RIOT_GAMES
    'www.leagueoflegends.com',
    # RIOT_GAMES
    'playvalorant.com',
    # RIOT_GAMES
    'valorant.com',
    # RIOT_GAMES
    'teamfighttactics.leagueoflegends.com',
    # RIOT_GAMES
    'tft.lol',
    # RIOT_GAMES
    'wildrift.leagueoflegends.com',
    # RIOT_GAMES
    'wildrift.com',
    # RIOT_GAMES
    'lolesports.com',
    # RIOT_GAMES
    'leagueoflegends.com.br',
    # RIOT_GAMES
    'valorantesports.com',
    # RIOT_GAMES
    'riotcdn.net',
    # RIOT_GAMES
    'pvp.net',
    # RIOT_GAMES
    'na.leagueoflegends.com',
    # RIOT_GAMES
    'br.leagueoflegends.com',
    # ACTIVISION_BLIZZARD
    'blizzard.com',
    # ACTIVISION_BLIZZARD
    'battle.net',
    # ACTIVISION_BLIZZARD
    'battle.net.cn',
    # ACTIVISION_BLIZZARD
    'activision.com',
    # ACTIVISION_BLIZZARD
    'callofduty.com',
    # ACTIVISION_BLIZZARD
    'callofduty.com.br',
    # ACTIVISION_BLIZZARD
    'warzone.com',
    # ACTIVISION_BLIZZARD
    'overwatch.blizzard.com',
    # ACTIVISION_BLIZZARD
    'overwatchleague.com',
    # ACTIVISION_BLIZZARD
    'hearthstone.com',
    # ACTIVISION_BLIZZARD
    'worldofwarcraft.com',
    # ACTIVISION_BLIZZARD
    'diablo4.com',
    # ACTIVISION_BLIZZARD
    'diablo3.com',
    # ACTIVISION_BLIZZARD
    'diabloimmortal.com',
    # ACTIVISION_BLIZZARD
    'starcraft2.com',
    # ACTIVISION_BLIZZARD
    'starcraft.com',
    # ACTIVISION_BLIZZARD
    'heroesofthestorm.com',
    # ACTIVISION_BLIZZARD
    'destinythegame.com',
    # ACTIVISION_BLIZZARD
    'bungie.net',
    # ACTIVISION_BLIZZARD
    'bungie.com',
    # ACTIVISION_BLIZZARD
    'marathon.bungie.com',
    # EA_GAMES
    'ea.com',
    # EA_GAMES
    'origin.com',
    # EA_GAMES
    'eaassets.com',
    # EA_GAMES
    'eaplay.com',
    # EA_GAMES
    'battlefield.com',
    # EA_GAMES
    'battlefield2042.com',
    # EA_GAMES
    'fifa.com',
    # EA_GAMES
    'ea-sports.com',
    # EA_GAMES
    'fc.ea.com',
    # EA_GAMES
    'ultimateteam.com',
    # EA_GAMES
    'tiberiumalliances.com',
    # EA_GAMES
    'thesims.com',
    # EA_GAMES
    'thesims4.com',
    # EA_GAMES
    'apexlegends.com',
    # EA_GAMES
    'needforspeed.com',
    # EA_GAMES
    'mass-effect.com',
    # EA_GAMES
    'dragonage.com',
    # EA_GAMES
    'plantsvszombies.com',
    # EA_GAMES
    'starwars.com',
    # EA_GAMES
    'starwarsbattlefront.com',
    # EA_GAMES
    'eafootball.com',
    # UBISOFT
    'ubisoft.com',
    # UBISOFT
    'store.ubisoft.com',
    # UBISOFT
    'connect.ubisoft.com',
    # UBISOFT
    'account.ubisoft.com',
    # UBISOFT
    'rainbow6.com',
    # UBISOFT
    'rainbowsixsiege.com',
    # UBISOFT
    'farcrygame.com',
    # UBISOFT
    'assassinscreed.com',
    # UBISOFT
    'thedivisiongame.com',
    # UBISOFT
    'thecrewgame.com',
    # UBISOFT
    'trackmania.com',
    # UBISOFT
    'justdancegame.com',
    # UBISOFT
    'ghostrecon.com',
    # UBISOFT
    'watchdogs-game.com',
    # UBISOFT
    'princeofpersiagame.com',
    # ROCKSTAR_TAKE_TWO
    'rockstargames.com',
    # ROCKSTAR_TAKE_TWO
    'socialclub.rockstargames.com',
    # ROCKSTAR_TAKE_TWO
    'launcher.rockstargames.com',
    # ROCKSTAR_TAKE_TWO
    'reddeadredemption.com',
    # ROCKSTAR_TAKE_TWO
    'reddeadonline.com',
    # ROCKSTAR_TAKE_TWO
    'gta5.com',
    # ROCKSTAR_TAKE_TWO
    'gtaonline.com',
    # ROCKSTAR_TAKE_TWO
    'gtav.com',
    # ROCKSTAR_TAKE_TWO
    'take2games.com',
    # ROCKSTAR_TAKE_TWO
    '2k.com',
    # ROCKSTAR_TAKE_TWO
    'nba2k.com',
    # ROCKSTAR_TAKE_TWO
    'wwe2k.com',
    # ROCKSTAR_TAKE_TWO
    'borderlands.com',
    # ROCKSTAR_TAKE_TWO
    'civilization.com',
    # ROCKSTAR_TAKE_TWO
    'mafia-game.com',
    # ROCKSTAR_TAKE_TWO
    'xcom.com',
    # PLAYSTATION_XBOX_NINTENDO
    'playstation.com',
    # PLAYSTATION_XBOX_NINTENDO
    'store.playstation.com',
    # PLAYSTATION_XBOX_NINTENDO
    'my.playstation.com',
    # PLAYSTATION_XBOX_NINTENDO
    'sonyentertainmentnetwork.com',
    # PLAYSTATION_XBOX_NINTENDO
    'xbox.com',
    # PLAYSTATION_XBOX_NINTENDO
    'xboxlive.com',
    # PLAYSTATION_XBOX_NINTENDO
    'xboxservices.com',
    # PLAYSTATION_XBOX_NINTENDO
    'xboxlive.com.br',
    # PLAYSTATION_XBOX_NINTENDO
    'microsoftcasualgames.com',
    # PLAYSTATION_XBOX_NINTENDO
    'nintendo.com',
    # PLAYSTATION_XBOX_NINTENDO
    'nintendo.com.br',
    # PLAYSTATION_XBOX_NINTENDO
    'nintendo-europe.com',
    # PLAYSTATION_XBOX_NINTENDO
    'nintendo.co.uk',
    # PLAYSTATION_XBOX_NINTENDO
    'nintendo.jp',
    # PLAYSTATION_XBOX_NINTENDO
    'nintendo.net',
    # PLAYSTATION_XBOX_NINTENDO
    'nintendolife.com',
    # MOBILE_GAMES
    'supercell.com',
    # MOBILE_GAMES
    'supercell.net',
    # MOBILE_GAMES
    'clashofclans.com',
    # MOBILE_GAMES
    'clashroyale.com',
    # MOBILE_GAMES
    'brawlstars.com',
    # MOBILE_GAMES
    'hayday.com',
    # MOBILE_GAMES
    'boombeach.com',
    # MOBILE_GAMES
    'clashmini.com',
    # MOBILE_GAMES
    'stumbleguys.com',
    # MOBILE_GAMES
    'stumbleguys.com.br',
    # MOBILE_GAMES
    'innersloth.com',
    # MOBILE_GAMES
    'amongusgame.com',
    # MOBILE_GAMES
    'fallguys.com',
    # MOBILE_GAMES
    'rocketleague.com',
    # MOBILE_GAMES
    'psyonix.com',
    # MOBILE_GAMES
    'pubg.com',
    # MOBILE_GAMES
    'pubgmobile.com',
    # MOBILE_GAMES
    'pubgmobile.com.br',
    # MOBILE_GAMES
    'krafton.com',
    # MOBILE_GAMES
    'mobilelegends.com',
    # MOBILE_GAMES
    'moonton.com',
    # MOBILE_GAMES
    'pokemongolive.com',
    # MOBILE_GAMES
    'pokemon.com',
    # MOBILE_GAMES
    'nianticlabs.com',
    # MOBILE_GAMES
    'niantic.helpshift.com',
    # MOBILE_GAMES
    'genshin.hoyoverse.com',
    # MOBILE_GAMES
    'hoyoverse.com',
    # MOBILE_GAMES
    'mihoyo.com',
    # MOBILE_GAMES
    'zenless.hoyoverse.com',
    # MOBILE_GAMES
    'honkaistarrail.com',
    # MINECRAFT_NON_EDUCATIONAL
    'minecraft.net',
    # MINECRAFT_NON_EDUCATIONAL
    'minecraft.net.br',
    # MINECRAFT_NON_EDUCATIONAL
    'minecraftservices.com',
    # MINECRAFT_NON_EDUCATIONAL
    'minecraft-services.net',
    # MINECRAFT_NON_EDUCATIONAL
    'minecraftskins.com',
    # MINECRAFT_NON_EDUCATIONAL
    'minecraftskins.net',
    # MINECRAFT_NON_EDUCATIONAL
    'minecraftforum.net',
    # MINECRAFT_NON_EDUCATIONAL
    'planetminecraft.com',
    # MINECRAFT_NON_EDUCATIONAL
    'minecraft-mp.com',
    # MINECRAFT_NON_EDUCATIONAL
    'minecraftservers.org',
    # MINECRAFT_NON_EDUCATIONAL
    'minecraft-server-list.com',
    # MINECRAFT_NON_EDUCATIONAL
    'minecraftserverslist.com',
    # MINECRAFT_NON_EDUCATIONAL
    'curseforge.com',
    # MINECRAFT_NON_EDUCATIONAL
    'modrinth.com',
    # MINECRAFT_NON_EDUCATIONAL
    'optifine.net',
    # MINECRAFT_NON_EDUCATIONAL
    'spigotmc.org',
    # MINECRAFT_NON_EDUCATIONAL
    'papermc.io',
    # MINECRAFT_NON_EDUCATIONAL
    'bukkit.org',
    # MINECRAFT_NON_EDUCATIONAL
    'hypixel.net',
    # MINECRAFT_NON_EDUCATIONAL
    'mineplex.com',
    # MINECRAFT_NON_EDUCATIONAL
    'aternos.org',
    # GAME_PORTALS_BROWSER
    'poki.com',
    # GAME_PORTALS_BROWSER
    'crazygames.com',
    # GAME_PORTALS_BROWSER
    'miniclip.com',
    # GAME_PORTALS_BROWSER
    'y8.com',
    # GAME_PORTALS_BROWSER
    'kongregate.com',
    # GAME_PORTALS_BROWSER
    'addictinggames.com',
    # GAME_PORTALS_BROWSER
    'armorgames.com',
    # GAME_PORTALS_BROWSER
    'newgrounds.com',
    # GAME_PORTALS_BROWSER
    'kizi.com',
    # GAME_PORTALS_BROWSER
    'friv.com',
    # GAME_PORTALS_BROWSER
    'friv5online.com',
    # GAME_PORTALS_BROWSER
    'silvergames.com',
    # GAME_PORTALS_BROWSER
    'agame.com',
    # GAME_PORTALS_BROWSER
    'gamesgames.com',
    # GAME_PORTALS_BROWSER
    'fog.com',
    # GAME_PORTALS_BROWSER
    'fandom.com',
    # GAME_PORTALS_BROWSER
    'gamejolt.com',
    # GAME_PORTALS_BROWSER
    'itch.io',
    # GAME_PORTALS_BROWSER
    'gamedistribution.com',
    # GAME_PORTALS_BROWSER
    'gameflare.com',
    # GAME_PORTALS_BROWSER
    'yad.com',
    # GAME_PORTALS_BROWSER
    'notdoppler.com',
    # GAME_PORTALS_BROWSER
    'mousebreaker.com',
    # GAME_PORTALS_BROWSER
    'plonga.com',
    # GAME_PORTALS_BROWSER
    'twoplayergames.org',
    # GAME_PORTALS_BROWSER
    'coolmathgames.com',
    # GAME_PORTALS_BROWSER
    'coolmathgames.com.br',
    # GAME_PORTALS_BROWSER
    'jogos360.com.br',
    # GAME_PORTALS_BROWSER
    'clickjogos.com.br',
    # GAME_PORTALS_BROWSER
    'ojogos.com.br',
    # GAME_PORTALS_BROWSER
    'friv.com.br',
    # GAME_PORTALS_BROWSER
    'jogosonline.com.br',
    # GAME_PORTALS_BROWSER
    'jogosgratis.com.br',
    # GAME_PORTALS_BROWSER
    'jogosbrasil.com.br',
    # GAME_PORTALS_BROWSER
    'jogos123.com',
    # GAME_PORTALS_BROWSER
    '1001jogos.com',
    # GAME_PORTALS_BROWSER
    '1001jogos.com.br',
    # GAME_PORTALS_BROWSER
    'jogosdodia.com.br',
    # GAME_PORTALS_BROWSER
    'jogosonlinegratis.com.br',
    # GAME_DATABASES_COMMUNITIES
    'ign.com',
    # GAME_DATABASES_COMMUNITIES
    'gamespot.com',
    # GAME_DATABASES_COMMUNITIES
    'metacritic.com',
    # GAME_DATABASES_COMMUNITIES
    'imdb.com',
    # GAME_DATABASES_COMMUNITIES
    'giantbomb.com',
    # GAME_DATABASES_COMMUNITIES
    'rawg.io',
    # GAME_DATABASES_COMMUNITIES
    'howlongtobeat.com',
    # GAME_DATABASES_COMMUNITIES
    'backloggd.com',
    # GAME_DATABASES_COMMUNITIES
    'isthereanydeal.com',
    # GAME_DATABASES_COMMUNITIES
    'gg.deals',
    # GAME_DATABASES_COMMUNITIES
    'dekudeals.com',
    # GAME_DATABASES_COMMUNITIES
    'hltb.com',
    # GAME_DATABASES_COMMUNITIES
    'speedrun.com',
    # GAME_DATABASES_COMMUNITIES
    'speedrun.com.br',
    # GAME_DATABASES_COMMUNITIES
    'liquipedia.net',
    # GAME_DATABASES_COMMUNITIES
    'esportsearnings.com',
    # GAME_DATABASES_COMMUNITIES
    'esportscharts.com',
    # GAME_DATABASES_COMMUNITIES
    'vlr.gg',
    # GAME_DATABASES_COMMUNITIES
    'tracker.gg',
    # GAME_DATABASES_COMMUNITIES
    'op.gg',
    # GAME_DATABASES_COMMUNITIES
    'u.gg',
    # GAME_DATABASES_COMMUNITIES
    'porofessor.gg',
    # GAME_DATABASES_COMMUNITIES
    'mobalytics.gg',
    # GAME_DATABASES_COMMUNITIES
    'blitz.gg',
    # GAME_DATABASES_COMMUNITIES
    'dak.gg',
    # GAME_DATABASES_COMMUNITIES
    'fortnitetracker.com',
    # GAME_DATABASES_COMMUNITIES
    'tracker.network',
    # GAME_DATABASES_COMMUNITIES
    'faceit.com',
    # GAME_DATABASES_COMMUNITIES
    'esea.net',
    # GAME_DATABASES_COMMUNITIES
    'challengermode.com',
    # GAME_DATABASES_COMMUNITIES
    'battlefy.com',
    # GAME_DATABASES_COMMUNITIES
    'start.gg',
    # GAME_DATABASES_COMMUNITIES
    'toornament.com',
    # GAME_DATABASES_COMMUNITIES
    'esl.com',
    # GAME_DATABASES_COMMUNITIES
    'eslgaming.com',
    # DISCORD_STREAMING_SOCIAL
    'discord.com',
    # DISCORD_STREAMING_SOCIAL
    'discordapp.com',
    # DISCORD_STREAMING_SOCIAL
    'discord.gg',
    # DISCORD_STREAMING_SOCIAL
    'discordapp.net',
    # DISCORD_STREAMING_SOCIAL
    'twitch.tv',
    # DISCORD_STREAMING_SOCIAL
    'www.twitch.tv',
    # DISCORD_STREAMING_SOCIAL
    'clips.twitch.tv',
    # DISCORD_STREAMING_SOCIAL
    'ttvnw.net',
    # DISCORD_STREAMING_SOCIAL
    'tiktok.com',
    # DISCORD_STREAMING_SOCIAL
    'www.tiktok.com',
    # DISCORD_STREAMING_SOCIAL
    'tiktokcdn.com',
    # DISCORD_STREAMING_SOCIAL
    'tiktokv.com',
    # DISCORD_STREAMING_SOCIAL
    'musical.ly',
    # DISCORD_STREAMING_SOCIAL
    'kwai.com',
    # DISCORD_STREAMING_SOCIAL
    'kwai-video.com',
    # DISCORD_STREAMING_SOCIAL
    'kick.com',
    # DISCORD_STREAMING_SOCIAL
    'rumble.com',
    # DISCORD_STREAMING_SOCIAL
    'trovo.live',
    # DISCORD_STREAMING_SOCIAL
    'facebook.com',
    # DISCORD_STREAMING_SOCIAL
    'instagram.com',
    # DISCORD_STREAMING_SOCIAL
    'x.com',
    # DISCORD_STREAMING_SOCIAL
    'twitter.com',
    # DISCORD_STREAMING_SOCIAL
    'snapchat.com',
    # DISCORD_STREAMING_SOCIAL
    'reddit.com',
    # DISCORD_STREAMING_SOCIAL
    'threads.net',
    # DISCORD_STREAMING_SOCIAL
    'pinterest.com',
    # DISCORD_STREAMING_SOCIAL
    'tumblr.com',
    # DISCORD_STREAMING_SOCIAL
    'telegram.org',
    # DISCORD_STREAMING_SOCIAL
    'web.telegram.org',
    # GAME_LAUNCHERS_STORES
    'gog.com',
    # GAME_LAUNCHERS_STORES
    'goggalaxy.com',
    # GAME_LAUNCHERS_STORES
    'humblebundle.com',
    # GAME_LAUNCHERS_STORES
    'humblegames.com',
    # GAME_LAUNCHERS_STORES
    'greenmangaming.com',
    # GAME_LAUNCHERS_STORES
    'gamersgate.com',
    # GAME_LAUNCHERS_STORES
    'fanatical.com',
    # GAME_LAUNCHERS_STORES
    'nuuvem.com',
    # GAME_LAUNCHERS_STORES
    'nuuvem.com.br',
    # GAME_LAUNCHERS_STORES
    'gamivo.com',
    # GAME_LAUNCHERS_STORES
    'eneba.com',
    # GAME_LAUNCHERS_STORES
    'cdkeys.com',
    # GAME_LAUNCHERS_STORES
    'instant-gaming.com',
    # GAME_LAUNCHERS_STORES
    'ggsel.net',
    # GAME_LAUNCHERS_STORES
    'playkey.net',
    # GAME_LAUNCHERS_STORES
    'parsec.app',
    # GAME_LAUNCHERS_STORES
    'shadow.tech',
    # GAME_LAUNCHERS_STORES
    'playnite.link',
    # GAME_LAUNCHERS_STORES
    'lutris.net',
    # GAME_LAUNCHERS_STORES
    'heroicgameslauncher.com',
    # GAME_LAUNCHERS_STORES
    'amazon.com/gaming',
    # GAME_SERVICES_MODS
    'nexusmods.com',
    # GAME_SERVICES_MODS
    'moddb.com',
    # GAME_SERVICES_MODS
    'mod.io',
    # GAME_SERVICES_MODS
    'steamworkshopdownloader.io',
    # GAME_SERVICES_MODS
    'workshop.codes',
    # GAME_SERVICES_MODS
    'thunderstore.io',
    # GAME_SERVICES_MODS
    'fabricmc.net',
    # GAME_SERVICES_MODS
    'forgecdn.net',
    # GAME_SERVICES_MODS
    'cursecdn.com',
    # GAME_SERVICES_MODS
    'ggservers.com',
    # GAME_SERVICES_MODS
    'shockbyte.com',
    # GAME_SERVICES_MODS
    'bisecthosting.com',
    # GAME_SERVICES_MODS
    'apexminecrafthosting.com',
    # GAME_SERVICES_MODS
    'server.pro',
    # GAME_SERVICES_MODS
    'minehut.com',
    # GAME_SERVICES_MODS
    'gamemonitoring.net',
    # PROXIES_BYPASS
    'croxyproxy.com',
    # PROXIES_BYPASS
    'hide.me',
    # PROXIES_BYPASS
    'hidester.com',
    # PROXIES_BYPASS
    'kproxy.com',
    # PROXIES_BYPASS
    '4everproxy.com',
    # PROXIES_BYPASS
    'proxysite.com',
    # PROXIES_BYPASS
    'proxysite.one',
    # PROXIES_BYPASS
    'hidemyass.com',
    # PROXIES_BYPASS
    'whoer.net',
    # PROXIES_BYPASS
    'proxyium.com',
    # PROXIES_BYPASS
    'plainproxies.com',
    # PROXIES_BYPASS
    'proxyshare.com',
    # PROXIES_BYPASS
    'vpnbook.com',
    # PROXIES_BYPASS
    'psiphon.ca',
    # PROXIES_BYPASS
    'psiphon3.com',
    # PROXIES_BYPASS
    'torproject.org',
    # PROXIES_BYPASS
    'duckduckgo.com',
    # GENERAL_ENTERTAINMENT
    'netflix.com',
    # GENERAL_ENTERTAINMENT
    'netflix.net',
    # GENERAL_ENTERTAINMENT
    'primevideo.com',
    # GENERAL_ENTERTAINMENT
    'disneyplus.com',
    # GENERAL_ENTERTAINMENT
    'hbomax.com',
    # GENERAL_ENTERTAINMENT
    'max.com',
    # GENERAL_ENTERTAINMENT
    'paramountplus.com',
    # GENERAL_ENTERTAINMENT
    'pluto.tv',
    # GENERAL_ENTERTAINMENT
    'crunchyroll.com',
    # GENERAL_ENTERTAINMENT
    'funimation.com',
    # GENERAL_ENTERTAINMENT
    'globoplay.globo.com',
    # GENERAL_ENTERTAINMENT
    'spotify.com',
    # GENERAL_ENTERTAINMENT
    'soundcloud.com',
    # GENERAL_ENTERTAINMENT
    'deezer.com',
    # GENERAL_ENTERTAINMENT
    'deezer.com.br',
    # GENERAL_ENTERTAINMENT
    'last.fm',
    # GENERAL_ENTERTAINMENT
    'music.youtube.com',
    # GENERAL_ENTERTAINMENT
    'youtube.com',
    # GENERAL_ENTERTAINMENT
    'youtu.be',
]

def is_admin():
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False

def elevate():
    params = " ".join(f'"{x}"' for x in sys.argv)
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)

def read_hosts():
    return HOSTS.read_text(encoding="utf-8", errors="ignore")

def write_hosts(text):
    tmp = HOSTS.with_suffix(".tmp")
    tmp.write_text(text, encoding="utf-8", newline="")
    os.replace(tmp, HOSTS)

def backup():
    BACKUP_DIR.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = BACKUP_DIR / f"hosts_{stamp}.bak"
    shutil.copy2(HOSTS, dest)
    return dest

def strip_our_section(text):
    start = text.find(MARK_BEGIN)
    end = text.find(MARK_END)
    if start >= 0 and end >= start:
        end += len(MARK_END)
        text = text[:start].rstrip() + "\n" + text[end:].lstrip()
    return text.rstrip() + "\n"

def install():
    if not HOSTS.exists():
        raise FileNotFoundError(f"HOSTS não encontrado: {HOSTS}")

    original = read_hosts()
    if MARK_BEGIN in original:
        original = strip_our_section(original)

    bak = backup()
    lines = [
        "",
        MARK_BEGIN,
        "# Gerado pelo Bloqueador Escolar",
        f"# Total de entradas: {len(DOMAINS)}",
        "# Não altere esta seção manualmente.",
    ]
    for domain in sorted(set(DOMAINS)):
        lines.append(f"{BLOCK_IP} {domain}")
    lines.append(MARK_END)

    write_hosts(original.rstrip() + "\n" + "\n".join(lines) + "\n")
    flush_dns()
    print(f"[OK] Bloqueio instalado: {len(set(DOMAINS))} domínios.")
    print(f"[OK] Backup: {bak}")
    print(f"[OK] HOSTS: {HOSTS}")

def remove():
    if not HOSTS.exists():
        raise FileNotFoundError(f"HOSTS não encontrado: {HOSTS}")
    original = read_hosts()
    if MARK_BEGIN not in original:
        print("[INFO] Nenhuma seção do Bloqueador Escolar encontrada.")
        return
    bak = backup()
    write_hosts(strip_our_section(original))
    flush_dns()
    print("[OK] Seção do Bloqueador Escolar removida.")
    print(f"[OK] Backup: {bak}")

def status():
    text = read_hosts()
    if MARK_BEGIN in text:
        section = text[text.find(MARK_BEGIN):text.find(MARK_END)]
        count = sum(1 for line in section.splitlines()
                    if line.startswith(BLOCK_IP + " "))
        print(f"[ATIVO] {count} entradas encontradas no HOSTS.")
    else:
        print("[INATIVO] Nenhuma seção do Bloqueador Escolar.")

def flush_dns():
    try:
        subprocess.run(["ipconfig", "/flushdns"], capture_output=True, text=True)
    except Exception:
        pass

def main():
    if not is_admin():
        print("[INFO] Solicitando privilégios de administrador...")
        elevate()
        return

    cmd = sys.argv[1].lower() if len(sys.argv) > 1 else "status"
    if cmd == "install":
        install()
    elif cmd == "remove":
        remove()
    elif cmd == "status":
        status()
    else:
        print("Uso: bloqueador_escola.py [install|remove|status]")
        sys.exit(2)

if __name__ == "__main__":
    main()
