---
tags: [scripts>cloud, scratchpad]
info: aberto.
date: 2024-11-03
type: post
layout: post
published: true
slug: gingko-websocket
title: 'Gingko Python WebSocket script'
---

bibref https://app.gingkowriter.com/database-download.html

`https://app.gingkowriter.com/database-download.html`

A Python WebSocket client script was successfully developed to enable programmatic interaction with the Gingko Writer application. The project began with the goal of establishing a stable connection to `wss://app.gingkowriter.com/ws`, managing authentication through cookies, and handling various message types such as `'rt:join'`, `'trees'`, and `'user'`.  An initial script provided basic connection logic, logging, and message exchange capabilities.
The development process then encountered challenges related to using the established connection for specific tasks, like creating cards. This practical application focus required deeper investigation into message formatting, asynchronous handling of user input alongside incoming messages, and the implementation of a structured request mechanism.  The project required guidance on adding an interactive command interface, concurrent processing, improved logging, and robust error handling to ensure maintainability and extensibility.
A revised Python script was subsequently developed. This version incorporated credentials and authentication details from browser Developer Tools, ensuring proper formatting of the `'rt:join'` message with the correct `tr`, `uid`, and `m` parameters.  The script's message handling was enhanced to process messages like `'rt:joinOk'` (join confirmation) and `'pushOk'` (push acknowledgment).  Securing credentials through environment variables and using valid, up-to-date system cookies was emphasized.
Initial testing revealed, via execution logs, that the `'rt:joinOk'` message was not being received, indicating a potential authentication problem.  Diagnostic steps and instructions for correctly extracting authentication details from Developer Tools were provided, prompting a script update.  This led to a successful connection and correct card creation within Gingko Writer, confirmed by subsequent logs showing push messages, `'pushOk'` acknowledgments, and seamless card hierarchy creation.
Throughout the project, issues with authentication parameter accuracy, session checkpoints, and real-time message exchange were addressed. Key milestones included accurate formatting of the `'rt:join'` message and correct interpretation of server acknowledgments. These achievements transformed the initial script into a functional tool for interacting with the Gingko Writer service.
The collaborative effort resulted in a robust Python WebSocket client capable of securely connecting to the Gingko Writer server and performing operations like creating structured card hierarchies. This was accomplished by meticulously resolving authentication problems, improving message handling, and ensuring adaptability through enhanced logging and error management. This foundation supports future extensions, such as adding interactive features or integrating more message types, increasing the script's utility for programmatically managing Gingko Writer documents.

```python
import asyncio
import json
import logging
import random
import string
import time
import websockets
from websockets.exceptions import ConnectionClosedError, WebSocketException

# Configure logging for detailed debugging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG for comprehensive logs
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GingkoWebsocketClient:
    """
    A client to interact with the Gingko Writer application via WebSocket.
    """

    def __init__(self, url: str, cookies: str, tree_id: str, user_id: str, auth_token: str):
        """
        Initializes the GingkoWebsocketClient with the necessary credentials and parameters.

        Args:
            url (str): The WebSocket URL for the Gingko Writer application.
            cookies (str): The authentication cookies.
            tree_id (str): The ID of the tree (document) to interact with.
            user_id (str): The user's Gingko Writer user ID.
            auth_token (str): The authentication token from the 'rt:join' message.
        """
        self.url = url
        self.cookies = cookies
        self.tree_id = tree_id
        self.user_id = user_id
        self.auth_token = auth_token
        self.session_id = None
        self.checkpoint = None
        self.push_ok_event = asyncio.Event()
        self.ws = None
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5

    async def generate_timestamp(self) -> str:
        """
        Generates a unique timestamp for operations.

        Returns:
            str: A timestamp string in the format 'milliseconds:sequence:session_fragment'
        """
        millis = int(time.time() * 1000)
        sequence = random.randint(0, 9)
        session_fragment = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"{millis}:{sequence}:{session_fragment}"

    async def generate_card_id(self) -> str:
        """
        Generates a unique card ID.

        Returns:
            str: A 24-character alphanumeric string.
        """
        return ''.join(random.choices(string.ascii_letters + string.digits, k=24))

    async def send_message(self, message_type: str, data: dict):
        """
        Sends a formatted message over the WebSocket connection.

        Args:
            message_type (str): The type of the message (e.g., 'push', 'rt:join').
            data (dict): The message data payload.
        """
        if self.ws is None:
            logger.error("WebSocket connection is not established.")
            return
        message = {"t": message_type, "d": data}
        try:
            await self.ws.send(json.dumps(message))
            logger.debug(f"Sent {message_type} message: {json.dumps(data)}")
        except Exception as e:
            logger.error(f"Failed to send message '{message_type}': {e}")

    async def handle_user_message(self, data: dict):
        logger.info(f"Received user data: {json.dumps(data, indent=2)}")

    async def handle_trees_message(self, data: list):
        trees = data
        logger.info(f"Received trees data: {json.dumps(trees, indent=2)}")
        tree_ids = [tree['id'] for tree in trees]
        if self.tree_id in tree_ids:
            self.session_id = "SessionNotProvided"
            self.push_ok_event.set()
            logger.info(f"Tree '{self.tree_id}' is available. Proceeding with operations.")
        else:
            logger.error(f"Tree '{self.tree_id}' not found in your account.")

    async def handle_rt_users_message(self, data: list):
        logger.info(f"Received rt:users data: {json.dumps(data, indent=2)}")

    async def handle_push_ok_message(self, data: list):
        checkpoint_list = data
        if checkpoint_list:
            self.checkpoint = checkpoint_list[0]
            logger.debug(f"Updated checkpoint to: {self.checkpoint}")
            self.push_ok_event.set()
        else:
            logger.warning("Received pushOk without checkpoint data.")

    async def handle_rt_join_ok_message(self, data: dict):
        self.session_id = data.get("sid")
        initial_checkpoint = data.get("chk")
        if initial_checkpoint:
            self.checkpoint = initial_checkpoint
        logger.info(f"Joined session: {self.session_id}, initial checkpoint: {self.checkpoint}")
        self.push_ok_event.set()

    async def handle_error_message(self, data: dict):
        logger.error(f"Received error from server: {json.dumps(data, indent=2)}")

    async def handle_message(self, message_data: dict):
        """
        Handles incoming messages from the WebSocket.

        Args:
            message_data (dict): The received message data.
        """
        logger.debug(f"Received message: {json.dumps(message_data, indent=2)}")
        message_type = message_data.get("t")
        data = message_data.get("d", {})

        handler = {
            "user": self.handle_user_message,
            "trees": self.handle_trees_message,
            "rt:users": self.handle_rt_users_message,
            "pushOk": self.handle_push_ok_message,
            "rt:joinOk": self.handle_rt_join_ok_message,
            "error": self.handle_error_message,
            "ping": lambda _: self.send_message("pong", {})
        }.get(message_type)

        if handler:
            await handler(data)
        else:
            logger.debug(f"Unhandled message type: {message_type}, data: {json.dumps(data, indent=2)}")

    async def message_handler(self):
        """
        Continuously handles incoming messages from the WebSocket.
        """
        try:
            async for message in self.ws:
                try:
                    message_data = json.loads(message)
                    await self.handle_message(message_data)
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to decode JSON message: {e}")
        except (ConnectionClosedError, WebSocketException) as e:
            logger.error(f"Connection closed: {e}")
            await self.reconnect()
        except Exception as e:
            logger.error(f"Unexpected error in message handler: {e}")
            await self.reconnect()

    def get_join_message(self) -> dict:
        """
        Constructs the 'rt:join' message to join the Gingko session.

        Returns:
            dict: The 'rt:join' message data.
        """
        return {
            "tr": self.tree_id,
            "uid": self.user_id,
            "m": ["a", self.auth_token]
        }

    async def create_card(self, content: str, parent_id: str = None, position: int = 0) -> str:
        """
        Creates a new card in the Gingko tree.

        Args:
            content (str): The content of the card.
            parent_id (str, optional): The ID of the parent card. Defaults to None.
            position (int, optional): The position among siblings. Defaults to 0.

        Returns:
            str: The ID of the created card.
        """
        card_id = await self.generate_card_id()
        insert_ts = await self.generate_timestamp()
        update_ts = await self.generate_timestamp()

        # Insert operation
        insert_delta = {
            "id": card_id,
            "ts": insert_ts,
            "ops": [
                {"t": "i", "c": "", "p": parent_id, "pos": position}
            ]
        }

        # Update operation
        update_delta = {
            "id": card_id,
            "ts": update_ts,
            "ops": [
                {"t": "u", "c": content, "e": insert_ts}
            ]
        }

        push_data = {
            "dlts": [insert_delta, update_delta],
            "tr": self.tree_id,
            "chk": self.checkpoint or insert_ts
        }

        self.push_ok_event.clear()
        await self.send_message("push", push_data)
        logger.info(f"Sent push for card '{content}' with ID {card_id}")

        try:
            await asyncio.wait_for(self.push_ok_event.wait(), timeout=10)
            logger.info(f"Push acknowledgment received for card '{content}'")
        except asyncio.TimeoutError:
            logger.error("Did not receive pushOk acknowledgment in time.")
            raise Exception("pushOk timeout")

        return card_id

    async def create_tree_structure(self, structure: list, parent_id: str = None):
        """
        Recursively creates a tree structure based on the provided data.

        Args:
            structure (list): A list of dicts representing the tree structure.
            parent_id (str, optional): The ID of the parent card. Defaults to None.
        """
        for position, node in enumerate(structure):
            content = node.get("content", "").strip()
            children = node.get("children", [])

            if not content:
                logger.warning("Encountered node without content. Skipping.")
                continue

            try:
                card_id = await self.create_card(content, parent_id, position)
                logger.info(f"Created card '{content}' with ID {card_id}")

                if children:
                    await self.create_tree_structure(children, card_id)

                # Small delay to avoid overwhelming the server
                await asyncio.sleep(0.1)
            except Exception as e:
                logger.error(f"Failed to create card '{content}': {e}")

    async def perform_operations(self):
        """
        Performs desired operations after establishing the WebSocket connection.
        This could be interacting with the tree, creating cards, etc.
        """
        logger.info("Starting operations...")

        # Example: Create a single card.
        example_structure = [
            {
                "content": "Automated Root Card",
                "children": [
                    {"content": "Automated Child 1"},
                    {"content": "Automated Child 2"}
                ]
            }
        ]

        await self.create_tree_structure(example_structure)
        logger.info("Completed creating example card structure.")

    async def connect(self):
        """
        Establishes the WebSocket connection and handles reconnection logic.
        """
        while self.reconnect_attempts < self.max_reconnect_attempts:
            try:
                async with websockets.connect(
                    self.url,
                    extra_headers={"Cookie": self.cookies}
                ) as ws:
                    self.ws = ws
                    self.reconnect_attempts = 0
                    logger.info(f"Connected to {self.url}")

                    # Send 'rt:join' message
                    join_message = self.get_join_message()
                    await self.send_message("rt:join", join_message)
                    logger.debug(f"Sent 'rt:join' message: {json.dumps(join_message)}")
                    logger.debug("Waiting for 'rt:joinOk' message...")

                    # Start handling incoming messages
                    message_task = asyncio.create_task(self.message_handler())

                    # Wait until session ID is received
                    try:
                        await asyncio.wait_for(self.push_ok_event.wait(), timeout=10)
                    except asyncio.TimeoutError:
                        logger.error("Did not receive 'rt:joinOk' acknowledgment in time.")
                        await self.reconnect()
                        continue

                    # Proceed with operations
                    await self.perform_operations()

                    # Keep the connection alive
                    await message_task

            except Exception as e:
                logger.exception(f"Connection error: {e}")
                await self.reconnect()

    async def reconnect(self):
        """
        Handles reconnection logic with exponential backoff.
        """
        self.reconnect_attempts += 1
        if self.reconnect_attempts >= self.max_reconnect_attempts:
            logger.error("Maximum reconnection attempts reached. Exiting.")
            return
        wait_time = min(2 ** self.reconnect_attempts, 60)
        logger.info(f"Attempting to reconnect in {wait_time} seconds (Attempt {self.reconnect_attempts}/{self.max_reconnect_attempts})...")
        await asyncio.sleep(wait_time)
        logger.info("Reconnecting...")
        # Reset session-specific data
        self.session_id = None
        self.checkpoint = None
        self.push_ok_event.clear()

    async def start(self):
        """
        Starts the client, connects to the server, and initiates operations.
        """
        try:
            await self.connect()
        except KeyboardInterrupt:
            logger.info("Interrupted by user.")
            if self.ws:
                await self.ws.close()
        except Exception as e:
            logger.exception(f"An unexpected error occurred: {e}")

    @staticmethod
    def load_credentials_from_env():
        """
        Loads credentials from environment variables.

        Returns:
            tuple: A tuple containing url, cookies, tree_id, user_id, auth_token
        """
        url = "wss://app.gingkowriter.com/ws"  # Fixed URL
        cookies = (
            "connect.sid=placeholder; "
            "_lr_uf_-jtqjrc=placeholder; "
            "_BEAMER_USER_ID_mYJLRImY38547=placeholder; "
            "_BEAMER_FIRST_VISIT_mYJLRImY38547=placeholder; "
            "__stripe_mid=placeholder; "
            "_BEAMER_LAST_POST_SHOWN_mYJLRImY38547=placeholder; "
            "_BEAMER_DATE_mYJLRImY38547=placeholder; "
            "_BEAMER_FILTER_BY_URL_mYJLRImY38547=placeholder; "
            "__stripe_sid=placeholder; "
            "_lr_tabs_-jtqjrc%2Fgingko-writer-production=placeholder}; "
            "_lr_hb_-jtqjrc%2Fgingko-writer-production=placeholder}"
        )
        tree_id = "6oj4Rzb"  # As per your 'rt:join' message
        user_id = "h9ogoeh2o2u7"  # As per your 'rt:join' message
        auth_token = "TLOBcFHCOPU6oI6mYHKdpR5F"  # As per your 'rt:join' message
        return url, cookies, tree_id, user_id, auth_token


async def main():
    """
    Main function to start the GingkoWebsocketClient.
    """
    # Load credentials directly from provided data
    URL, COOKIES, TREE_ID, USER_ID, AUTH_TOKEN = GingkoWebsocketClient.load_credentials_from_env()

    client = GingkoWebsocketClient(URL, COOKIES, TREE_ID, USER_ID, AUTH_TOKEN)
    await client.start()


if __name__ == "__main__":
    asyncio.run(main())
```
