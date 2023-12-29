# bot-first-vk-comment

VK Bot is a Python script designed to automate commenting on the latest posts in VKontakte (VK) groups. It utilizes the VK API to monitor specified groups and leaves comments based on a predefined set of messages.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/vk-bot.git
   cd vk-bot
   
2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt

3. **Fill in config.json**
    
## Configuration

- **group_ids**: List of VK group IDs to monitor.
- **messages**: List of messages to randomly choose from when leaving comments.
- **token**: Kate Mobile token obtained from [VK Host](https://vkhost.github.io/).
- **delay**: Delay in seconds between checking for new posts.
- **mode**: 1 - leave a random comment, 2 - leave all comments at once
## Disclaimer

This script is intended for educational purposes only. Use it responsibly and adhere to VK's terms of service.

