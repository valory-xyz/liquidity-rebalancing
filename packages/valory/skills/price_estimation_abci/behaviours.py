# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2021 Valory AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This module contains the behaviours for the 'abci' skill."""
from abc import ABC
from typing import Any, cast

from aea.skills.behaviours import FSMBehaviour, State
from aea_ledger_ethereum import EthereumCrypto

from packages.fetchai.protocols.http import HttpMessage
from packages.fetchai.protocols.signing import SigningMessage
from packages.fetchai.protocols.signing.custom_types import RawMessage, Terms
from packages.valory.skills.price_estimation_abci.behaviours_utils import (
    AsyncBehaviour,
    DONE_EVENT,
    WaitForConditionBehaviour,
)
from packages.valory.skills.price_estimation_abci.dialogues import SigningDialogues
from packages.valory.skills.price_estimation_abci.models import (
    RegistrationPayload,
    Transaction,
)
from packages.valory.skills.price_estimation_abci.tendermint_rpc import BehaviourUtils


class PriceEstimationConsensusBehaviour(FSMBehaviour):
    """This behaviour manages the consensus stages for the price estimation."""

    def setup(self) -> None:
        """Set up the behaviour."""
        self.register_state(
            "wait_tendermint",
            WaitForConditionBehaviour(
                condition=self.wait_tendermint_rpc_is_ready,
                name="wait_tendermint",
                skill_context=self.context,
            ),
            initial=True,
        )
        self.register_state(
            "register",
            RegistrationBehaviour(name="register", skill_context=self.context),
        )
        self.register_state(
            "wait_registration_threshold",
            WaitForConditionBehaviour(
                condition=self.wait_registration_threshold,
                name="wait_registration_threshold",
                skill_context=self.context,
            ),
        )
        self.register_state(
            "end",
            EndBehaviour(name="end", skill_context=self.context),
        )

        self.register_transition("wait_tendermint", "register", DONE_EVENT)
        self.register_transition("register", "wait_registration_threshold", DONE_EVENT)
        self.register_transition("wait_registration_threshold", "end", DONE_EVENT)

    def teardown(self) -> None:
        """Tear down the behaviour"""

    def wait_tendermint_rpc_is_ready(self) -> bool:
        """Wait Tendermint RPC server is up."""
        return self.context.state.info_received

    def wait_registration_threshold(self) -> bool:
        """Wait registration threshold is reached."""
        return self.context.state.current_round.registration_threshold_reached


class BaseState(State, ABC):
    """Base class for FSM states."""

    is_programmatically_defined = True

    def handle_signing_failure(self):
        """Handle signing failure."""
        self.context.logger.error("the transaction could not be signed.")

    def _send_signing_request(self, raw_message: bytes):
        """Send a signing request."""
        signing_dialogues = cast(SigningDialogues, self.context.signing_dialogues)
        signing_msg, signing_dialogue = signing_dialogues.create(
            counterparty=self.context.decision_maker_address,
            performative=SigningMessage.Performative.SIGN_MESSAGE,
            raw_message=RawMessage(EthereumCrypto.identifier, raw_message),
            terms=Terms(
                ledger_id=EthereumCrypto.identifier,
                sender_address="",
                counterparty_address="",
                amount_by_currency_id={},
                quantities_by_good_id={},
                nonce="",
            ),
        )
        self.context.decision_maker_message_queue.put_nowait(signing_msg)


class RegistrationBehaviour(AsyncBehaviour, BaseState, BehaviourUtils):
    """Register to the next round."""

    is_programmatically_defined = True

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the behaviour."""
        AsyncBehaviour.__init__(self)
        BaseState.__init__(self, **kwargs)
        self._is_done: bool = False

    def is_done(self) -> bool:
        """Check whether the state is done."""
        return self._is_done

    def async_act(self) -> None:
        """
        Do the action.

        Steps:
        - Build a registration transaction
        - Request the signature of the payload to the Decision Maker
        - Request a registration transaction to the 'price-estimation' app,
          until the transaction is not mined.
        - Go to the next state.
        """
        payload = RegistrationPayload(self.context.agent_address)
        self._send_signing_request(payload.encode())
        signature = yield from self.wait_for_message()
        if signature is None:
            self.handle_signing_failure()
            return
        signature_bytes = signature.body
        transaction = Transaction(payload, signature_bytes)
        while True:
            response = yield from self.broadcast_tx_commit(transaction.encode())
            response = cast(HttpMessage, response)
            if self._check_transaction_delivered(response):
                # done
                break
            # otherwise, repeat until done
        self.context.logger.info("Registration done.")
        # set flag 'done' and event to "done"
        self._is_done = True
        self._event = DONE_EVENT


class EndBehaviour(BaseState):
    """Final state."""

    is_programmatically_defined = True

    def is_done(self) -> bool:
        """Check if the behaviour is done."""
        return True

    def act(self) -> None:
        """Do the act."""
        self.context.logger.info("The end.")
