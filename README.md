# CTF cogs for Redbot cogs

These are a collection of CTF related cogs for the Red Discord Bot.

## Development Guide

### Installation

To install required dependencies, run the following command:

```bash
poetry install
```

### Setup Redbot

Setup Redbot with the following command:

```bash
poetry run redbot-setup
```

Follow the prompts to set up Redbot.

### Run Redbot

To run the bot, use the following command:

```bash
poetry run redbot instance_name --dev
```

replace `instance_name` with the name of your Redbot instance set up in the previous step.

### Add Directory to cog Paths

Message the bot with the following command to add the directory to the cog paths:

```bash
[p]addpath <directory>
```

Where `[p]` is the prefix of your bot and `<directory>` is the path to the directory containing the cogs.

### Load Cogs

To load the cogs, use the following command:

```bash
[p]load <cog_name>
```

Where `[p]` is the prefix of your bot and `<cog_name>` is the name of the cog you want to load.
