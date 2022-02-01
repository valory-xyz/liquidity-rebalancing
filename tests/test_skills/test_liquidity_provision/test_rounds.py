# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2021-2022 Valory AG
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

"""Tests for rounds.py file in valory/liquidity_provision."""

import json
from types import MappingProxyType
from typing import Dict, FrozenSet, Mapping, Optional  # noqa : F401
from unittest import mock

from packages.valory.skills.abstract_round_abci.base import StateDB
from packages.valory.skills.liquidity_provision.payloads import (
    StrategyEvaluationPayload,
    StrategyType,
)
from packages.valory.skills.liquidity_provision.rounds import (  # noqa: F401
    Event,
    PeriodState,
    StrategyEvaluationRound,
    TransactionHashBaseRound,
)
from packages.valory.skills.price_estimation_abci.payloads import TransactionHashPayload
from packages.valory.skills.transaction_settlement_abci.payloads import ValidatePayload

from tests.test_skills.test_abstract_round_abci.test_base_rounds import (
    BaseCollectSameUntilThresholdRoundTest,
)
from tests.test_skills.test_transaction_settlement_abci.test_rounds import (
    get_participant_to_signature,
)


MAX_PARTICIPANTS: int = 4


def get_participants() -> FrozenSet[str]:
    """Returns test value for participants"""
    return frozenset([f"agent_{i}" for i in range(MAX_PARTICIPANTS)])


def get_participant_to_strategy(
    participants: FrozenSet[str],
) -> Mapping[str, StrategyEvaluationPayload]:
    """Returns test value for participant_to_strategy"""
    return dict(
        [
            (participant, StrategyEvaluationPayload(sender=participant, strategy={}))
            for participant in participants
        ]
    )


def get_participant_to_transfers_result(
    participants: FrozenSet[str],
) -> Dict[str, ValidatePayload]:
    """Get participant_to_lp_result"""
    return {
        participant: ValidatePayload(sender=participant) for participant in participants
    }


def get_participant_to_tx_hash(
    participants: FrozenSet[str],
    hash_: Optional[str] = "tx_hash",
    data_: Optional[str] = "tx_data",
) -> Mapping[str, TransactionHashPayload]:
    """participant_to_tx_hash"""
    return {
        participant: TransactionHashPayload(
            sender=participant, tx_hash=json.dumps({"tx_hash": hash_, "tx_data": data_})
        )
        for participant in participants
    }


class TestTransactionHashBaseRound(BaseCollectSameUntilThresholdRoundTest):
    """Test TransactionHashBaseRound"""

    _period_state_class = PeriodState
    _event_class = Event

    def test_run(
        self,
    ) -> None:
        """Run tests."""

        test_round = TransactionHashBaseRound(self.period_state, self.consensus_params)
        payloads = get_participant_to_tx_hash(self.participants)
        self._complete_run(
            self._test_round(
                test_round=test_round,
                round_payloads=payloads,
                state_update_fn=lambda _period_state, _test_round: _period_state.update(
                    participant_to_tx_hash=MappingProxyType(payloads),
                    most_voted_tx_hash=json.loads(_test_round.most_voted_payload)[
                        "tx_hash"
                    ],
                    most_voted_tx_data=json.loads(_test_round.most_voted_payload)[
                        "tx_data"
                    ],
                ),
                state_attr_checks=[
                    lambda state: state.participant_to_tx_hash.keys(),
                ],
                most_voted_payload=payloads["agent_1"].tx_hash,
                exit_event=Event.DONE,
            )
        )


class TestStrategyEvaluationRound(BaseCollectSameUntilThresholdRoundTest):
    """Test StrategyEvaluationRound"""

    _period_state_class = PeriodState
    _event_class = Event

    def test_run_enter(
        self,
    ) -> None:
        """Run tests."""
        test_round = StrategyEvaluationRound(self.period_state, self.consensus_params)
        with mock.patch.object(
            StrategyEvaluationPayload, "strategy", return_value="strategy"
        ):
            self._complete_run(
                self._test_round(
                    test_round=test_round,
                    round_payloads=get_participant_to_strategy(self.participants),
                    state_update_fn=lambda _period_state, _test_round: _period_state.update(
                        participant_to_strategy=get_participant_to_strategy(
                            self.participants
                        ),
                        most_voted_strategy=test_round.most_voted_payload,
                    ),
                    state_attr_checks=[
                        lambda state: state.participant_to_strategy.keys(),
                    ],
                    most_voted_payload=StrategyEvaluationPayload.strategy,
                    exit_event=Event.RESET_TIMEOUT,
                )
            )


def test_period_state() -> None:
    """Test PeriodState."""

    participants = get_participants()
    period_count = 0
    period_setup_params: Dict = {}
    most_voted_strategy: Dict = {}
    most_voted_keeper_address = "0x_keeper"
    safe_contract_address = "0x_contract"
    multisend_contract_address = "0x_multisend"
    most_voted_tx_hash = "tx_hash"
    final_tx_hash = "tx_hash"
    participant_to_lp_result = get_participant_to_transfers_result(participants)
    participant_to_tx_hash = get_participant_to_tx_hash(participants)
    participant_to_signature = get_participant_to_signature(participants)
    participant_to_strategy = get_participant_to_strategy(participants)
    safe_operation = "safe_operation"

    period_state = PeriodState(
        StateDB(
            initial_period=period_count,
            initial_data=dict(
                participants=participants,
                period_setup_params=period_setup_params,
                most_voted_strategy=most_voted_strategy,
                most_voted_keeper_address=most_voted_keeper_address,
                safe_contract_address=safe_contract_address,
                multisend_contract_address=multisend_contract_address,
                most_voted_tx_hash=most_voted_tx_hash,
                final_tx_hash=final_tx_hash,
                participant_to_lp_result=participant_to_lp_result,
                participant_to_tx_hash=participant_to_tx_hash,
                participant_to_signature=participant_to_signature,
                participant_to_strategy=participant_to_strategy,
                safe_operation=safe_operation,
            ),
        )
    )

    assert period_state.participants == participants
    assert period_state.period_count == period_count
    assert period_state.most_voted_strategy == most_voted_strategy
    assert period_state.most_voted_keeper_address == most_voted_keeper_address
    assert period_state.safe_contract_address == safe_contract_address
    assert period_state.multisend_contract_address == multisend_contract_address
    assert period_state.most_voted_tx_hash == most_voted_tx_hash
    assert period_state.final_tx_hash == final_tx_hash
    assert period_state.participant_to_tx_hash == participant_to_tx_hash
    assert period_state.participant_to_signature == participant_to_signature
    assert period_state.participant_to_strategy == participant_to_strategy
    assert period_state.safe_operation == safe_operation
