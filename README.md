# Basic-ChatGPT-Discord-Bot
A basic discord bot that uses the ChatGPT API for its responses
### Hi there, I'm back? I guess
A few months ago I did this little experiment with the ChatGPT API, I know it is a very basic bot but at the time I developed this, the bots using ChatGPT were very scarce

The code has some bugs it seems to me, sometimes **if you give a "prompt" that is too long and specific it takes a little while to respond, no more than approximately 1 minute**

Also keep in mind that **it will use the API Key of your OpenAI account, when it runs out of uses or "tokens" the bot will stop responding unless you buy more "tokens" on the OpenAI developers website**

> I hope this code helps you for your future project, enjoy it!

### Added Docker Support!
1.  **Run Docker Compose:**
    ```bash
    DISCORD_TOKEN=YourDiscordToken OPENAI_API_KEY=YourOpenAIKey docker-compose up -d
    ```
    * Replace `YourDiscordToken` and `YourOpenAIKey` with your actual Discord bot token and OpenAI API key.
## Configuration
* The `config.json` file contains non-sensitive configurations such as the bot's prefix.
* Sensitive credentials (Discord token and OpenAI API key) are configured using environment variables directly in the `docker-compose up` command.

## How the bot responds on discord?

![That´s the Help Embed uwuwuwuw](/Examples/helpembed.PNG)

![a respo0o0o0o0o0o0o0o0nse uwuwuwuw](/Examples/response.PNG)

![anoda responsada uwuwuwuw](/Examples/anodaone.PNG)
