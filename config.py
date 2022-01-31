#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")

    # APP_ID = os.environ.get("MicrosoftAppId", "2f962698-d19f-46c6-948b-ddb68de11024")
    # APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "lYj7Q~Ccte_wg2BxEeExFtYudFtbGr3fA-N~d")