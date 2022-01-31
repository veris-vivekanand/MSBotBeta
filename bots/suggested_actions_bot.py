# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext, CardFactory, ConversationState, UserState
from botbuilder.schema import ChannelAccount, CardAction, ActionTypes, SuggestedActions, ChannelAccount, Mention, HeroCard, Activity, ActivityTypes, ReceiptCard, ReceiptItem
import data_models

from testcall import *
from resources import *
from typing import List
# import adaptive_card_content

from data_models import ConversationFlow, Question, user_profile, UserProfile

from adaptive_table import AdaptiveTable

from recognizers_number import recognize_number, Culture
from recognizers_date_time import recognize_datetime

from helpers.dialog_helper import DialogHelper
from botbuilder.dialogs import Dialog, WaterfallDialog, WaterfallStepContext, DialogTurnResult


class ValidationResult:
    def __init__(
        self, is_valid: bool = False, value: object = None, message: str = None
    ):
        self.is_valid = is_valid
        self.value = value
        self.message = message


def data_adap(rquery):
    try:
        tyam = rquery.get('amenities')
        if tyam:
            print('tyam: ', tyam)
        tybk = rquery.get('bookings')
        if tybk:
            print('tybk: ', tybk)
        else:
            tybk = None
        tynbk = rquery.get('next_booking')
        if tynbk:
            print('tynbk: ', tynbk)
        tybk1 = []
        it1 = []
        i = 0
        for ty in tyam:
            i = i+1
            text = ty.get('am_name')
            text1 = ty.get('am_quantity')
            it = {
                "type": "Column",
                "width": "auto",
                "items": [
                    {
                        "type": "TextBlock",
                        "size": "small",
                        "text": f'{i}.{text}',
                        "spacing": "none",
                        "weight": "bolder",
                    },

                ],
            }
            it1.append(it)
        print('tybk: ', it)
        it_bk1 = []
        print('text before ')
        text = rquery.get('bookings'[0], {}).get('valid_from', {}) if rquery.get(
            'bookings'[0], {}).get('valid_from', {}) else None
        # text = rquery.get('bookings')[0].get('valid_from')
        print('text: ', text)
        # text = None
        if text is not None:
            for ty in tybk:
                text = ty.get('valid_from')
                if not text:
                    text = None
                text1 = ty.get('valid_till')
                if not text1:
                    text1 = None
                text2 = ty.get('host_name')
                if not text2:
                    text2 = None
                it = {
                    "type": "Column",
                    "width": "auto",
                    "items": [
                        {
                            "type": "TextBlock",
                            "size": "small",
                            "text": f'Valid from: {text}',
                            "spacing": 1,
                            "weight": "bolder",
                        },
                        {
                            "type": "TextBlock",
                            "size": "small",
                            "text": f'Valid till: {text1}',
                            "spacing": 1,
                            "weight": "bolder",
                        },
                        {
                            "type": "TextBlock",
                            "size": "small",
                            "text": f'Host: {text2}',
                            "spacing": 1,
                            "weight": "bolder",
                        },
                    ],
                }
                it_bk1.append(it)
        else:
            it_bk1 = [{
                "type": "Column",
                "width": "auto",
                "items": [
                        {
                            "type": "TextBlock",
                            "size": "small",
                            "text": f'No Booking',
                            "spacing": 1,
                            "weight": "bolder",
                        },
                ]
            }]
        next_booking_from = tynbk.get('next_booking_from')
        if next_booking_from is None:
            next_booking_from = "No Booking"
        next_booking_till = tynbk.get('next_booking_till')
        if next_booking_till is None:
            next_booking_till = "No Booking"
        ADAPTIVE_CARD_CONTENT = {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.0",
            "type": "AdaptiveCard",
            "speak": "Venue 101",
            "body": [
                {
                    "type": "TextBlock",
                    "text": "Venue: " + rquery['name'] + "(" + rquery['venue'] + "}",
                    "weight": "bolder",
                    "isSubtle": False,
                    "size": "Large",
                    "fontType": "monospace",
                    "color": "accent",
                    "horizontalAlignment":"left",
                    "spacing": "large"
                },
                {
                    "type": "TextBlock",
                    "text": "",
                    "weight": "bolder",
                    "spacing": "medium",
                },
                {
                    "type": "TextBlock",
                    "text": "",
                    "weight": "bolder",
                    "spacing": "medium",
                },
                {"type": "TextBlock", "text": "Bookings", "separator": True,
                    "size": "Large", "weight": "bolder", "color": "good", "spacing": "none", "horizontalAlignment": "center"},
                {
                    "type": "ColumnSet",
                    "separator": True,
                    "columns": it_bk1,
                },
                {"type": "TextBlock", "text": "Amenities", "separator": True,
                    "size": "Large", "weight": "bolder", "color": "good", "spacing": "none", "horizontalAlignment": "center"},
                {
                    "type": "ColumnSet",
                    "separator": True,
                    "columns": it1,
                },
                {"type": "TextBlock", "text": "Next booking", "separator": True,
                    "size": "Large", "weight": "bolder", "color": "good", "spacing": "none", "horizontalAlignment": "center"},
                {
                    "type": "ColumnSet",
                    "separator": True,
                    "columns": [
                        {
                            "type": "Column",
                            "width": 2,
                            "items": [
                                {"type": "TextBlock", "text": "Valid From",
                                    "isSubtle": True},
                                {
                                    "type": "TextBlock",
                                    "size": "small",
                                    "color": "dark",
                                    "text": next_booking_from,
                                    "spacing": "none",
                                },
                            ],
                        },
                        {
                            "type": "Column",
                            "width": 1,
                            "items": [
                                {"type": "TextBlock", "text": "Valid Till",
                                    "isSubtle": True},
                                {
                                    "type": "TextBlock",
                                    "size": "small",
                                    "color": "dark",
                                    "text": next_booking_till,
                                    "spacing": "none",
                                },
                            ],
                        },
                    ],
                },
            ],
        }
        print("Ran before return adaptivecard content")
        return ADAPTIVE_CARD_CONTENT
    except Exception as e:
        print("Adap Exception: ", e)


class SuggestActionsBot(ActivityHandler):
    """
    This bot will respond to the user's input with suggested actions.
    Suggested actions enable your bot to present buttons that the user
    can tap to provide input.
    """

    def __init__(self, conversation_state: ConversationState, user_state: UserState,):
        if conversation_state is None:
            raise TypeError(
                "[CustomPromptBot]: Missing parameter. conversation_state is required but None was given"
            )
        if user_state is None:
            raise TypeError(
                "[CustomPromptBot]: Missing parameter. user_state is required but None was given"
            )

        # if dialog is None:
        #     raise Exception("[DialogBot]: Missing parameter. dialog is required")

        # self.add_dialog(
        #     WaterfallDialog(
        #         WaterfallDialog.__name__,
        #         [
        #             self.destination_step,
        #             self.origin_step,
        #             self.travel_date_step,
        #             self.confirm_step,
        #             self.final_step,
        #         ],
        #     )
        # )
        # self.initial_dialog_id = WaterfallDialog.__name__

        self.conversation_state = conversation_state
        self.user_state = user_state
        # self.dialog = dialog

        self.flow_accessor = self.conversation_state.create_property(
            "ConversationFlow")
        # self.profile_accessor = self.user_state.create_property("UserProfile")
        self.booking_accessor = self.user_state.create_property(
            "BookingProfile")

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        # Save any state changes that might have occurred during the turn.
        await self.conversation_state.save_changes(turn_context, False)
        await self.user_state.save_changes(turn_context, False)

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        """
        Send a welcome message to the user and tell them what actions they may perform to use this bot
        """

        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")

    async def on_message_activity(self, turn_context: TurnContext):
        """
        Respond to the users choice and display the suggested actions again.
        """
        # print("turn: ", turn_context.activity)
        flow = await self.flow_accessor.get(turn_context, ConversationFlow)
        print("flow: ", flow.last_question_asked)
        userQuery = f"{turn_context.activity.text}"
        if 'hi' in userQuery.lower() or 'hello' in userQuery.lower():
            return await self._send_welcome_options(turn_context)
        elif 'venue' in userQuery.lower():
            response_text = await self._resource_data(userQuery, turn_context)
            await turn_context.send_activity(response_text)
            await turn_context.send_activity(f"Type name to know more details ")
        elif 'status' in userQuery.lower():
            if 'health' in userQuery.lower() or 'work' in userQuery.lower():
                response_text = await self._process_input(userQuery, turn_context)
                await turn_context.send_activity(response_text)
            else:
                return await self._send_suggested_actions(turn_context)
        elif 'survey' in userQuery.lower():
            return await self._send_health_survey(turn_context)
        elif 'health' in userQuery.lower() or 'work' in userQuery.lower():
            response_text = await self._process_input(userQuery, turn_context)
            await turn_context.send_activity(response_text)
        elif 'fever' in userQuery.lower() or 'cough' in userQuery.lower() or 'loss' in userQuery.lower():
            await turn_context.send_activity(f"Please contact your org admin as you are not allowed to come to office due to COVID symptoms")
        elif 'no_symptom' in userQuery.lower():
            await turn_context.send_activity(f"You are good to go ")
        elif "book" in userQuery.lower():
            profile = await self.booking_accessor.get(turn_context, data_models.user_profile.BookingProfile)
            flow = await self.flow_accessor.get(turn_context, ConversationFlow)

            await self._fill_out_user_profile(flow, profile, turn_context)

            await self.conversation_state.save_changes(turn_context)
            await self.user_state.save_changes(turn_context)
        elif flow.last_question_asked != "Question.NONE":
            profile = await self.booking_accessor.get(turn_context, data_models.user_profile.BookingProfile)
            await self._fill_out_user_profile(flow, profile, turn_context)

            await self.conversation_state.save_changes(turn_context)
            await self.user_state.save_changes(turn_context)
        else:
            await turn_context.send_activity(f"You said '{ turn_context.activity.text }'")

    async def _send_welcome_message(self, turn_context: TurnContext):
        for member in turn_context.activity.members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    MessageFactory.text(
                        f"Welcome to SuggestedActionsBot {member.name}."
                        f" This bot will introduce you to suggestedActions."
                        f" Please answer the question: "
                    )
                )

                await self._send_suggested_actions(turn_context)

    async def _process_input(self, text: str, turn_context: TurnContext):
        # color_text = "is the best color, I agree."

        name = []
        to_date = []
        from_date = []
        status = []
        if "health" in text.lower():
            responseQuery = await fetch_users(text.replace(" ", "+"))
            reply_activity = MessageFactory()
            if responseQuery is not None:
                for responseQuery1 in responseQuery:
                    name.append(str(responseQuery1[f'name']))
                    from_date.append(str(responseQuery1[f'from_date']))
                    to_date.append(str(responseQuery1[f'to_date']))
                    status.append(str(responseQuery1[f'status']))
                col_name = AdaptiveTable.create_column(
                    "Name", name)
                col_from = AdaptiveTable.create_column(
                    "From Date", from_date)
                col_to = AdaptiveTable.create_column(
                    "To Date", to_date)
                col_status = AdaptiveTable.create_column(
                    "Status", status)
                col_set = AdaptiveTable.create_column_list(
                    [col_name, col_from, col_to, col_status])
                jsonObject = AdaptiveTable.prepare_json(col_set)
                message = Activity(type=ActivityTypes.message)
                message.attachments = [CardFactory.adaptive_card(jsonObject)]
                message.text = "Health Status"
            else:
                message = Activity(type=ActivityTypes.message)
                message.text = "No Data"
        elif "work" in text.lower():
            responseQuery = await fetch_users(text.replace(" ", "+"))
            if responseQuery is not None:
                for responseQuery1 in responseQuery:
                    name.append(str(responseQuery1[f'name']))
                    from_date.append(str(responseQuery1[f'from_date']))
                    to_date.append(str(responseQuery1[f'to_date']))
                    status.append(str(responseQuery1[f'status']))
                col_name = AdaptiveTable.create_column(
                    "Name", name)
                col_from = AdaptiveTable.create_column(
                    "From Date", from_date)
                col_to = AdaptiveTable.create_column(
                    "To Date", to_date)
                col_status = AdaptiveTable.create_column(
                    "Status", status)
                col_set = AdaptiveTable.create_column_list(
                    [col_name, col_from, col_to, col_status])
                jsonObject = AdaptiveTable.prepare_json(col_set)
                message = Activity(type=ActivityTypes.message)
                message.attachments = [CardFactory.adaptive_card(jsonObject)]
                message.text = "Work Status"
            else:
                message = Activity(type=ActivityTypes.message)
                message.text = "No Data"
        else:
            message = Activity(type=ActivityTypes.message)
            message.text = "Please select a box from the suggested action choices"
        return message

    async def _resource_data(self, text: str, turn_context: TurnContext):
        # color_text = "is the best color, I agree."
        print('text: ', text)
        text2 = text.lower().replace("venue", "")
        text2 = text2.replace(" ", "")
        print('text2: ', text2)
        rid = []
        name = []
        venue = []
        status = []
        venue_type = []
        responseQuery = await fetch_resources(text.replace(" ", "+"))
        print('function fetch resource worked')
        reply_activity = MessageFactory()
        if responseQuery is not None:
            for responseQuery1 in responseQuery:
                rid.append(str(responseQuery1[f'rid']))
                name.append(str(responseQuery1[f'name']))
                venue.append(str(responseQuery1[f'venue']))
                venue_type.append(str(responseQuery1[f'venue_type']))
                # to_date.append(str(responseQuery1[f'to_date']))
                status.append(str(responseQuery1[f'status']))
            if text2 in name:
                rquery = await resource_details(text2)
                card_data = data_adap(rquery)
                message = Activity(type=ActivityTypes.message)
                message.attachments = [CardFactory.adaptive_card(card_data)]
            else:
                col_rid = AdaptiveTable.create_column(
                    "Id", rid)
                col_name = AdaptiveTable.create_column(
                    "Name", name)
                col_from = AdaptiveTable.create_column(
                    "Venue", venue)
                col_venue_type = AdaptiveTable.create_column(
                    "Venue type", venue_type)
                col_status = AdaptiveTable.create_column(
                    "Status", status)
                col_set = AdaptiveTable.create_column_list(
                    [col_rid, col_name, col_from, col_status, col_venue_type])
                jsonObject = AdaptiveTable.prepare_json(col_set)
                message = Activity(type=ActivityTypes.message)
                message.attachments = [CardFactory.adaptive_card(jsonObject)]
                message.text = "Venues"
        else:
            message = Activity(type=ActivityTypes.message)
            message.text = "No Data"
        print('returning msg')
        return message

    async def _send_suggested_actions(self, turn_context: TurnContext):
        """
        Creates and sends an activity with suggested actions to the user. When the user
        clicks one of the buttons the text value from the "CardAction" will be displayed
        in the channel just as if the user entered the text. There are multiple
        "ActionTypes" that may be used for different situations.
        """
        card = HeroCard(
            title="Please select type of status you want to know",
            text="",
            # images=[CardImage(url="https://aka.ms/bf-welcome-card-image")],
            buttons=[
                CardAction(
                    type=ActionTypes.im_back,
                    title="HEALTH",
                    text="HEALTH",
                    display_text="HEALTH",
                    value="HEALTH",
                ),
                CardAction(
                    type=ActionTypes.im_back,
                    title="WORK",
                    text="WORK",
                    display_text="WORK",
                    value="WORK",
                ),
                # CardAction(
                #     type=ActionTypes.open_url,
                #     title="Learn how to deploy",
                #     text="Learn how to deploy",
                #     display_text="Learn how to deploy",
                #     value="https://docs.microsoft.com/en-us/azure/bot-service/bot-builder-howto-deploy-azure?view=azure-bot-service-4.0",
                # ),
            ],
        )
        # print('reply: ', reply)
        return await turn_context.send_activity(MessageFactory.attachment(CardFactory.hero_card(card)))

    async def _send_health_survey(self, turn_context: TurnContext):
        """
        Creates and sends an activity with suggested actions to the user. When the user
        clicks one of the buttons the text value from the "CardAction" will be displayed
        in the channel just as if the user entered the text. There are multiple
        "ActionTypes" that may be used for different situations.
        """
        card = HeroCard(
            title="Health Survey",
            text="Please select any if applicable",
            # images=[CardImage(url="https://aka.ms/bf-welcome-card-image")],
            buttons=[
                CardAction(
                    type=ActionTypes.im_back,
                    title="High temperature",
                    text="High temperature",
                    display_text="Do you have high temperature?",
                    value="fever",
                ),
                CardAction(
                    type=ActionTypes.im_back,
                    title="Continous cough",
                    text="Continous cough",
                    display_text="Do you have new continous cough?",
                    value="cough",
                ),
                CardAction(
                    type=ActionTypes.im_back,
                    title="Loss or change to your sense of smell or taste",
                    text="Loss or change to your sense of smell or taste",
                    display_text="Do you have loss or change to your sense of smell or taste?",
                    value="loss",
                ),
                CardAction(
                    type=ActionTypes.im_back,
                    title="No Symptom",
                    text="No Symptom",
                    display_text="I do not have any symptom",
                    value="no_symptom",
                )
            ],
        )
        # print('reply: ', reply)
        return await turn_context.send_activity(MessageFactory.attachment(CardFactory.hero_card(card)))

    async def _send_health_survey(self, turn_context: TurnContext):
        """
        Creates and sends an activity with suggested actions to the user. When the user
        clicks one of the buttons the text value from the "CardAction" will be displayed
        in the channel just as if the user entered the text. There are multiple
        "ActionTypes" that may be used for different situations.
        """
        card = HeroCard(
            title="Health Survey",
            text="Please select any if applicable",
            # images=[CardImage(url="https://aka.ms/bf-welcome-card-image")],
            buttons=[
                CardAction(
                    type=ActionTypes.im_back,
                    title="High temperature",
                    text="High temperature",
                    display_text="Do you have high temperature?",
                    value="fever",
                ),
                CardAction(
                    type=ActionTypes.im_back,
                    title="Continous cough",
                    text="Continous cough",
                    display_text="Do you have new continous cough?",
                    value="cough",
                ),
                CardAction(
                    type=ActionTypes.im_back,
                    title="Loss or change to your sense of smell or taste",
                    text="Loss or change to your sense of smell or taste",
                    display_text="Do you have loss or change to your sense of smell or taste?",
                    value="loss",
                ),
                CardAction(
                    type=ActionTypes.im_back,
                    title="No Symptom",
                    text="No Symptom",
                    display_text="I do not have any symptom",
                    value="no_symptom",
                )
            ],
        )
        # print('reply: ', reply)
        return await turn_context.send_activity(MessageFactory.attachment(CardFactory.hero_card(card)))

    async def _send_welcome_options(self, turn_context: TurnContext):
        """
        Creates and sends an activity with suggested actions to the user. When the user
        clicks one of the buttons the text value from the "CardAction" will be displayed
        in the channel just as if the user entered the text. There are multiple
        "ActionTypes" that may be used for different situations.
        """
        card = HeroCard(
            title="Please select any option to proceed",
            text="",
            # images=[CardImage(url="https://aka.ms/bf-welcome-card-image")],
            buttons=[
                CardAction(
                    type=ActionTypes.im_back,
                    title="Status",
                    text="Status",
                    # display_text="Do you have high temperature?",
                    value="Status",
                ),
                CardAction(
                    type=ActionTypes.im_back,
                    title="Health Survey",
                    text="Health Survey",
                    # display_text="Do you have new continous cough?",
                    value="Health Survey",
                ),
                CardAction(
                    type=ActionTypes.im_back,
                    title="Venue",
                    text="Venue",
                    # display_text="Do you have new continous cough?",
                    value="Venue",
                ),
                CardAction(
                    type=ActionTypes.im_back,
                    title="Book",
                    text="Book Venue",
                    # display_text="Do you have new continous cough?",
                    value="Book",
                )
            ],
        )
        # print('reply: ', reply)
        return await turn_context.send_activity(MessageFactory.attachment(CardFactory.hero_card(card)))


# For booking


    async def _fill_out_user_profile(
        self, flow: ConversationFlow, profile: data_models.user_profile.BookingProfile, turn_context: TurnContext
    ):
        user_input = turn_context.activity.text.strip()

        # print('flow: ', flow.last_question_asked)
        # ask for name
        if flow.last_question_asked == Question.NONE:
            await turn_context.send_activity(
                MessageFactory.text(
                    "Let's get started. Want to know available venues to book? Type 1 for availability check, 2 if you know venue name or 3 for exit.")
            )
            flow.last_question_asked = Question.BAVAIL

        elif flow.last_question_asked == Question.BAVAIL:
            profile.bavail = user_input
            if profile.bavail == "1":
                print('Yes')
                uqry = "availability"
                response_text = await self._resource_data(uqry, turn_context)
                await turn_context.send_activity(response_text)
                # if
                flow.last_question_asked = Question.BVENUE
            elif profile.bavail == "2":
                await turn_context.send_activity(
                    MessageFactory.text(
                        "Please type venue name you want to book ")
                )
                flow.last_question_asked = Question.BVENUE
            elif profile.bavail == "3":
                flow.last_question_asked = Question.NONE
                await turn_context.send_activity(
                    MessageFactory.text("Type anything to run the bot again.")
                )

        # validate name then ask for age
        elif flow.last_question_asked == Question.BVENUE:
            print("in age")
            validate_result = self._validate_bvenue(user_input)
            if not validate_result.is_valid:
                flow.last_question_asked = Question.NONE
                await turn_context.send_activity(
                    MessageFactory.text(validate_result.message)
                )
            else:
                profile.bvenue = validate_result.value
                if profile.bvenue == "3":
                    flow.last_question_asked = Question.FDATE
                    await turn_context.send_activity(
                        MessageFactory.text(
                            "Type anything to run the bot again.")
                    )
                await turn_context.send_activity(
                    MessageFactory.text(
                        f"Booking for Venue {profile.bvenue}'\n'. The meeting time should be between 15 minutes to 60 minutes in future.")
                )

                await turn_context.send_activity(
                    MessageFactory.text(
                        "From which date do you want to book? Type date and time.")
                )
                flow.last_question_asked = Question.FDATE

        # validate age then ask for date
        elif flow.last_question_asked == Question.FDATE:
            validate_result = self._validate_date(user_input)
            if not validate_result.is_valid:
                await turn_context.send_activity(
                    MessageFactory.text(validate_result.message)
                )
            else:
                profile.fdate = validate_result.value
                if profile.fdate == "3":
                    flow.last_question_asked = Question.NONE
                    await turn_context.send_activity(
                        MessageFactory.text(
                            "Type anything to run the bot again.")
                    )
                await turn_context.send_activity(
                    MessageFactory.text(
                        f"I have your start date as {profile.fdate}.")
                )
                await turn_context.send_activity(
                    MessageFactory.text("Till when do you wish to book?")
                )
                flow.last_question_asked = Question.TDATE

        # validate date and wrap it up
        elif flow.last_question_asked == Question.TDATE:
            validate_result = self._validate_date(user_input)
            if not validate_result.is_valid:
                await turn_context.send_activity(
                    MessageFactory.text(validate_result.message)
                )
            else:
                profile.tdate = validate_result.value
                if profile.tdate == "3":
                    await turn_context.send_activity(
                        MessageFactory.text(
                            "Type anything to run the bot again.")
                    )
                ty = await book_resource(profile)
                # result = ty.get('id', {}) if ty.get('id', {}) else ty.get('detail')
                # print('result: ', ty)
                if ty.get('id'):
                    result = f"Your booking id: {ty['id']}"
                    await turn_context.send_activity(
                        MessageFactory.text(
                            f"Your meeting is scheduled for {profile.fdate} - {profile.tdate}."
                        )
                    )
                    await turn_context.send_activity(
                        MessageFactory.text(
                            f"Thanks for completing the booking on venue- {profile.bvenue}."
                        )
                    )
                else:
                    result = f"Sorry can not book as {ty['detail']}"
                await turn_context.send_activity(
                    result
                )

                await turn_context.send_activity(
                    MessageFactory.text("Type anything to run the bot again.")
                )
                flow.last_question_asked = Question.NONE

    def _validate_bvenue(self, user_input: str) -> ValidationResult:
        print("User input: ", self, user_input)

        if not user_input:
            return ValidationResult(
                is_valid=False,
                message="Please enter a name that contains at least one character.",
            )

        return ValidationResult(is_valid=True, value=user_input)

    def _validate_age(self, user_input: str) -> ValidationResult:
        # Attempt to convert the Recognizer result to an integer. This works for "a dozen", "twelve", "12", and so on.
        # The recognizer returns a list of potential recognition results, if any.
        results = recognize_number(user_input, Culture.English)
        for result in results:
            if "value" in result.resolution:
                age = int(result.resolution["value"])
                if 18 <= age <= 120:
                    return ValidationResult(is_valid=True, value=age)

        return ValidationResult(
            is_valid=False, message="Please enter an age between 18 and 120."
        )

    def _validate_date(self, user_input: str) -> ValidationResult:
        try:
            # Try to recognize the input as a date-time. This works for responses such as "11/14/2018", "9pm",
            # "tomorrow", "Sunday at 5pm", and so on. The recognizer returns a list of potential recognition results,
            # if any.
            results = recognize_datetime(user_input, Culture.English)
            for result in results:
                for resolution in result.resolution["values"]:
                    if "value" in resolution:
                        now = datetime.datetime.now()

                        value = resolution["value"]
                        if resolution["type"] == "date":
                            candidate = datetime.datetime.strptime(
                                value, "%Y-%m-%d")
                        elif resolution["type"] == "time":
                            candidate = datetime.datetime.strptime(
                                value, "%H:%M:%S")
                            candidate = candidate.replace(
                                year=now.year, month=now.month, day=now.day
                            )
                        else:
                            candidate = datetime.datetime.strptime(
                                value, "%Y-%m-%d %H:%M:%S")

                        # user response must be more than an hour out
                        diff = candidate - now
                        if diff.total_seconds() >= 3600:
                            return ValidationResult(
                                is_valid=True,
                                value=candidate.strftime("%Y-%m-%d  %H:%M:%S"),
                            )

            return ValidationResult(
                is_valid=False,
                message="I'm sorry, please enter a date at least an hour out.",
            )
        except ValueError:
            return ValidationResult(
                is_valid=False,
                message="I'm sorry, I could not interpret that as an appropriate "
                "date. Please enter a date at least an hour out.",
            )

    async def destination_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """
        If a destination city has not been provided, prompt for one.
        :param step_context:
        :return DialogTurnResult:
        """
        booking_details = step_context.options

        if booking_details.destination is None:
            message_text = "Where would you like to travel to?"
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(booking_details.destination)

    async def origin_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        If an origin city has not been provided, prompt for one.
        :param step_context:
        :return DialogTurnResult:
        """
        booking_details = step_context.options

        # Capture the response to the previous step's prompt
        booking_details.destination = step_context.result
        if booking_details.origin is None:
            message_text = "From what city will you be travelling?"
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(booking_details.origin)

    async def travel_date_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """
        If a travel date has not been provided, prompt for one.
        This will use the DATE_RESOLVER_DIALOG.
        :param step_context:
        :return DialogTurnResult:
        """
        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.origin = step_context.result
        if not booking_details.travel_date or self.is_ambiguous(
            booking_details.travel_date
        ):
            return await step_context.begin_dialog(
                DateResolverDialog.__name__, booking_details.travel_date
            )
        return await step_context.next(booking_details.travel_date)

    async def confirm_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """
        Confirm the information the user has provided.
        :param step_context:
        :return DialogTurnResult:
        """
        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.travel_date = step_context.result
        message_text = (
            f"Please confirm, I have you traveling to: { booking_details.destination } from: "
            f"{ booking_details.origin } on: { booking_details.travel_date}."
        )
        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input
        )

        # Offer a YES/NO prompt.
        return await step_context.prompt(
            ConfirmPrompt.__name__, PromptOptions(prompt=prompt_message)
        )

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        Complete the interaction and end the dialog.
        :param step_context:
        :return DialogTurnResult:
        """
        if step_context.result:
            booking_details = step_context.options

            return await step_context.end_dialog(booking_details)
        return await step_context.end_dialog()

    def is_ambiguous(self, timex: str) -> bool:
        timex_property = Timex(timex)
        return "definite" not in timex_property.types
