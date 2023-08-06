#Quart-OAuth2-Discord.py
______
A library to make the discord authentication system easier for Quart Users.  

To install this library:
```bash
$ python3 -m pip install Quart-OAuth2-Discord.py
```
If you're in Windows:
```bash
python -m pip install Quart-OAuth2-Discord.py
```

An example of Quart-app-with-Discord-Bot
```python
from typing import List

from quart import Quart, redirect, render_template_string, request, url_for

from quart_oauth2_discord_py import DiscordOauth2Client, Guild

app = Quart(__name__)
app.secret_key = b"random bytes representing quart secret key"
app.config['DISCORD_CLIENT_ID'] = "Client ID here"
app.config['DISCORD_CLIENT_SECRET'] = 'CLIENT_SECRET_HERE'
app.config['SCOPES'] = ['identify', 'guilds']
app.config['DISCORD_REDIRECT_URI'] = 'http://127.0.0.1:5000/callback'
app.config['DISCORD_BOT_TOKEN'] = None

client = DiscordOauth2Client(app)


@app.route('/')
async def index():
    return "Hello!"


@app.route('/login/', methods=['GET'])
async def login():
    return await client.create_session()


@app.route('/callback')
async def callback():
    await client.callback()
    return redirect(url_for('index'))


def return_guild_names_owner(guilds_: List[Guild]):
    # print(list(sorted([fetch_guild.name for fetch_guild in guilds_ if fetch_guild.is_owner_of_guild()])))
    return list(sorted([fetch_guild.name for fetch_guild in guilds_ if fetch_guild.is_owner_of_guild()]))


def search_guilds_for_name(guilds_, query):
    # print(list(sorted([fetch_guild.name for fetch_guild in guilds_ if fetch_guild.is_owner_of_guild() and fetch_guild.name == query])))
    return list(sorted([fetch_guild.name for fetch_guild in guilds_ if fetch_guild.is_owner_of_guild() and fetch_guild.name == query]))


@app.route('/guilds')
async def guilds():
    template_string = """
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Guilds</title>
        </head>
        <body>
            <h1>Your guilds: </h1>
            <ol>
            {% for guild_name in guild_names %}
                <li>{{ guild_name }}</li>
            {% endfor %}
            </ol>
        </body>
    </html>
    """
    if request.args.get('guild_name'):
        return await render_template_string(template_string, guild_names=search_guilds_for_name(await client.fetch_guilds(), request.args.get('guild_name')))
    return await render_template_string(template_string, guild_names=return_guild_names_owner(await client.fetch_guilds()))


@app.route('/me')
@client.is_logged_in
async def me():
    user = await client.fetch_user()
    image = user.avatar_url
    # noinspection HtmlUnknownTarget
    return await render_template_string("""
        <html lang="en">
            <body>
                <p>Login Successful</p>
                <img src="{{ image_url }}" alt="Avatar url">
            </body>
        </html>
        """, image_url=image)


if __name__ == '__main__':
    app.run()


```
This is not yet documented. It will be documented soon.