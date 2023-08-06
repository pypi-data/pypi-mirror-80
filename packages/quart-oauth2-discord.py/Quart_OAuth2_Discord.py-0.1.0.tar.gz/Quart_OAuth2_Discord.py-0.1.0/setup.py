# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quart_oauth2_discord_py', 'quart_oauth2_discord_py.models']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0',
 'authlib>=0.14.3,<0.15.0',
 'httpx>=0.15.4,<0.16.0',
 'quart>=0.13.1,<0.14.0']

setup_kwargs = {
    'name': 'quart-oauth2-discord.py',
    'version': '0.1.0',
    'description': 'A library to make the discord authentication system easier for Quart Users',
    'long_description': '#Quart-OAuth2-Discord.py\n______\nA library to make the discord authentication system easier for Quart Users.  \n\nTo install this library:\n```bash\n$ python3 -m pip install Quart-OAuth2-Discord.py\n```\nIf you\'re in Windows:\n```bash\npython -m pip install Quart-OAuth2-Discord.py\n```\n\nAn example of Quart-app-with-Discord-Bot\n```python\nfrom typing import List\n\nfrom quart import Quart, redirect, render_template_string, request, url_for\n\nfrom quart_oauth2_discord_py import DiscordOauth2Client, Guild\n\napp = Quart(__name__)\napp.secret_key = b"random bytes representing quart secret key"\napp.config[\'DISCORD_CLIENT_ID\'] = "Client ID here"\napp.config[\'DISCORD_CLIENT_SECRET\'] = \'CLIENT_SECRET_HERE\'\napp.config[\'SCOPES\'] = [\'identify\', \'guilds\']\napp.config[\'DISCORD_REDIRECT_URI\'] = \'http://127.0.0.1:5000/callback\'\napp.config[\'DISCORD_BOT_TOKEN\'] = None\n\nclient = DiscordOauth2Client(app)\n\n\n@app.route(\'/\')\nasync def index():\n    return "Hello!"\n\n\n@app.route(\'/login/\', methods=[\'GET\'])\nasync def login():\n    return await client.create_session()\n\n\n@app.route(\'/callback\')\nasync def callback():\n    await client.callback()\n    return redirect(url_for(\'index\'))\n\n\ndef return_guild_names_owner(guilds_: List[Guild]):\n    # print(list(sorted([fetch_guild.name for fetch_guild in guilds_ if fetch_guild.is_owner_of_guild()])))\n    return list(sorted([fetch_guild.name for fetch_guild in guilds_ if fetch_guild.is_owner_of_guild()]))\n\n\ndef search_guilds_for_name(guilds_, query):\n    # print(list(sorted([fetch_guild.name for fetch_guild in guilds_ if fetch_guild.is_owner_of_guild() and fetch_guild.name == query])))\n    return list(sorted([fetch_guild.name for fetch_guild in guilds_ if fetch_guild.is_owner_of_guild() and fetch_guild.name == query]))\n\n\n@app.route(\'/guilds\')\nasync def guilds():\n    template_string = """\n    <!DOCTYPE html>\n    <html lang="en">\n        <head>\n            <meta charset="UTF-8">\n            <title>Guilds</title>\n        </head>\n        <body>\n            <h1>Your guilds: </h1>\n            <ol>\n            {% for guild_name in guild_names %}\n                <li>{{ guild_name }}</li>\n            {% endfor %}\n            </ol>\n        </body>\n    </html>\n    """\n    if request.args.get(\'guild_name\'):\n        return await render_template_string(template_string, guild_names=search_guilds_for_name(await client.fetch_guilds(), request.args.get(\'guild_name\')))\n    return await render_template_string(template_string, guild_names=return_guild_names_owner(await client.fetch_guilds()))\n\n\n@app.route(\'/me\')\n@client.is_logged_in\nasync def me():\n    user = await client.fetch_user()\n    image = user.avatar_url\n    # noinspection HtmlUnknownTarget\n    return await render_template_string("""\n        <html lang="en">\n            <body>\n                <p>Login Successful</p>\n                <img src="{{ image_url }}" alt="Avatar url">\n            </body>\n        </html>\n        """, image_url=image)\n\n\nif __name__ == \'__main__\':\n    app.run()\n\n\n```\nThis is not yet documented. It will be documented soon.',
    'author': 'sairam4123',
    'author_email': 'sairamkumar2022@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
