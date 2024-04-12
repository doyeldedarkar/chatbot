# Copyright (c) 2023 Robert Bosch GmbH and its subsidiaries.  This program and the accompanying materials are made
# available under the terms of the Bosch Internal Open Source License v4 which accompanies this distribution, and is
# available at http://bios.intranet.bosch.com/bioslv4.txt
from PIL import Image
"""Prompts to show in our frontends."""

MY_IMAGE = Image.open('MY_logo.jpg') #Logo for ED
My_IMAGE = MY_IMAGE.resize((120,90))
Logo_image = Image.open('logo.jpg')

PAGE_ICON = BOSCH_image

NUM_REQUESTS_WARNING = """You've reached the maximum number of requests.
Your request may be incomplete.
If you want more information, change the _"Max. number of requests"_ parameter in the settings.
"""
TITLE = "ChatED"
WELCOME_MESSAGE = "Feel free to ask me anything, I'm here to help. :heart:"
DATA_PROTECTION_MESSAGE = """\
Queries to our models are processed on-prem. \
However, do not submit any confidential information for now. \
"""
ABOUT = """Made in short time with for the employees of ED only

"""




MENU_ITEMS = {
    "Get help": "https://github.boschdevcloud.com/bios-bcai/chatbosch/discussions",
    "Report a Bug": "https://github.boschdevcloud.com/bios-bcai/chatbosch/issues",
    "About": ABOUT,
}
