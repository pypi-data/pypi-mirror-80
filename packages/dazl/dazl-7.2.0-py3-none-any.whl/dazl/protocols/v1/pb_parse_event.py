# Copyright (c) 2017-2020 Digital Asset (Switzerland) GmbH and/or its affiliates. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Conversion methods from Ledger API Protobuf-generated types to dazl/Pythonic types.
"""
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Union

# noinspection PyPackageRequirements
from google.protobuf.empty_pb2 import Empty

from ... import LOG
from ...damlast.daml_lf_1 import ModuleRef, PackageRef, DottedName, TypeConName
from ...model.core import ContractId
from ...model.reading import BaseEvent, TransactionFilter, ContractCreateEvent, \
    TransactionStartEvent, TransactionEndEvent, ContractArchiveEvent, OffsetEvent, \
    ContractExercisedEvent, ActiveContractSetEvent, ContractFilter
from ...model.core import Party
from ...model.types import RecordType, Type, VariantType, ContractIdType, ListType, \
    TypeEvaluationContext, type_evaluate_dispatch_default_error, TextMapType, OptionalType, TypeReference
from ...model.types_store import PackageStore
from ...util.prim_types import to_date, to_datetime


@dataclass(frozen=True)
class BaseEventDeserializationContext:
    """
    Attributes required throughout the deserialization of an event stream.
    """
    client: Any
    store: PackageStore
    party: Party
    ledger_id: str

    def offset_event(self, time: datetime, offset: str) -> OffsetEvent:
        return OffsetEvent(self.client, self.party, time, self.ledger_id, self.store, offset)

    def active_contract_set(self, offset: str, workflow_id: str) \
            -> 'ActiveContractSetEventDeserializationContext':
        return ActiveContractSetEventDeserializationContext(
            self.client, self.store, self.party, self.ledger_id,
            offset, workflow_id)

    def transaction(self, time: datetime, offset: str, command_id: str, workflow_id: str) \
            -> 'TransactionEventDeserializationContext':
        return TransactionEventDeserializationContext(
            self.client, self.store, self.party, self.ledger_id,
            time, offset, command_id, workflow_id)


@dataclass(frozen=True)
class ActiveContractSetEventDeserializationContext(BaseEventDeserializationContext):
    """
    Attributes required throughout the deserialization of the Active Contract Set.
    """
    offset: str
    workflow_id: str

    def active_contract_set_event(self, contract_events: 'Sequence[ContractCreateEvent]') \
            -> 'ActiveContractSetEvent':
        return ActiveContractSetEvent(self.client, self.party, None, self.ledger_id, self.store,
                                      self.offset, contract_events)

    def contract_created_event(self, cid, cdata, event_id, witness_parties) -> ContractCreateEvent:
        return ContractCreateEvent(
            client=self.client, party=self.party, time=None, ledger_id=self.ledger_id,
            package_store=self.store, offset=self.offset,
            command_id='', workflow_id=self.workflow_id,
            cid=cid, cdata=cdata, event_id=event_id, witness_parties=witness_parties)


@dataclass(frozen=True)
class TransactionEventDeserializationContext(BaseEventDeserializationContext):
    """
    Attributes required throughout the deserialization of an event stream.
    """
    time: datetime
    offset: str
    command_id: str
    workflow_id: str

    def transaction_start_event(self, contract_events) -> TransactionStartEvent:
        return TransactionStartEvent(self.client, self.party, self.time, self.ledger_id, self.store,
                                     self.offset, self.command_id, self.workflow_id, contract_events)

    def transaction_end_event(self, contract_events) -> TransactionEndEvent:
        return TransactionEndEvent(self.client, self.party, self.time, self.ledger_id, self.store,
                                   self.offset, self.command_id, self.workflow_id, contract_events)

    def contract_created_event(self, cid, cdata, event_id, witness_parties) -> ContractCreateEvent:
        return ContractCreateEvent(
            client=self.client, party=self.party, time=self.time, ledger_id=self.ledger_id,
            package_store=self.store, offset=self.offset,
            command_id=self.command_id, workflow_id=self.workflow_id,
            cid=cid, cdata=cdata, event_id=event_id, witness_parties=witness_parties)

    def contract_exercised_event(self, cid, cdata, event_id, witness_parties,
                                 contract_creating_event_id: str, choice: str, choice_argument: Any,
                                 acting_parties, consuming, child_event_ids, exercise_result) \
            -> ContractExercisedEvent:
        return ContractExercisedEvent(
            client=self.client, party=self.party, time=self.time, ledger_id=self.ledger_id,
            package_store=self.store, offset=self.offset,
            command_id=self.command_id, workflow_id=self.workflow_id,
            cid=cid, cdata=cdata, event_id=event_id, witness_parties=witness_parties,
            contract_creating_event_id=contract_creating_event_id, acting_parties=acting_parties,
            choice=choice, choice_args=choice_argument, consuming=consuming,
            child_event_ids=child_event_ids,
            exercise_result=exercise_result)

    def contract_archived_event(self, cid, cdata, event_id, witness_parties) \
            -> ContractArchiveEvent:
        return ContractArchiveEvent(
            client=self.client, party=self.party, time=self.time, ledger_id=self.ledger_id,
            package_store=self.store, offset=self.offset,
            command_id=self.command_id, workflow_id=self.workflow_id,
            cid=cid, cdata=cdata, event_id=event_id, witness_parties=witness_parties)


def serialize_transactions_request(f: 'TransactionFilter', ledger_id: str, party: str) \
        -> 'G.GetTransactionsRequest':
    from . import model as G

    if f.current_offset is not None:
        ledger_offset = G.LedgerOffset()
        ledger_offset.absolute = f.current_offset
    else:
        ledger_offset = G.LedgerOffset()
        ledger_offset.boundary = 0

    if f.destination_offset is not None:
        final_offset = G.LedgerOffset()
        final_offset.absolute = f.destination_offset
    else:
        final_offset = G.LedgerOffset()
        final_offset.boundary = 1

    return G.GetTransactionsRequest(
        ledger_id=ledger_id,
        begin=ledger_offset,
        end=final_offset,
        filter=serialize_transaction_filter(f, party))


def serialize_acs_request(f: 'ContractFilter', ledger_id: str, party: str) -> 'G.GetActiveContractsRequest':
    from . import model as G

    return G.GetActiveContractsRequest(
        ledger_id=ledger_id,
        filter=serialize_transaction_filter(f, party))


def serialize_event_id_request(ledger_id: str, event_id: str, requesting_parties: 'Sequence[str]') \
        -> 'G.GetTransactionByEventIdRequest':
    from . import model as G
    return G.GetTransactionByEventIdRequest(ledger_id=ledger_id,
                                            event_id=event_id,
                                            requesting_parties=requesting_parties)


def serialize_transaction_filter(contract_filter: 'ContractFilter', party: str) -> 'G.TransactionFilter':
    from . import model as G
    from .pb_ser_command import as_identifier

    identifiers = [as_identifier(tt) for tt in contract_filter.templates] \
        if contract_filter.templates is not None else None

    parties = [party]
    if contract_filter.party_groups is not None:
        parties.extend(contract_filter.party_groups)

    filters_by_party = {}
    for party in parties:
        if identifiers is not None:
            filters_by_party[party] = G.Filters(inclusive=G.InclusiveFilters(template_ids=identifiers))
        else:
            filters_by_party[party] = G.Filters()

    return G.TransactionFilter(filters_by_party=filters_by_party)


def to_transaction_events(
        context: 'BaseEventDeserializationContext',
        tx_stream_pb: 'Iterable[G.GetTransactionsResponse]',
        tt_stream_pb: 'Optional[Iterable[G.GetTransactionTreesResponse]]',
        last_offset_override: 'Optional[str]') -> 'Sequence[BaseEvent]':
    """
    Convert a stream of :class:`GetTransactionsResponse` into a sequence of events.

    :param context:
        Additional data required for deserializing wire information into easily-consumable
        application events.
    :param tx_stream_pb:
        A stream of :class:`GetTransactionsResponse`.
    :param tt_stream_pb:
        An optional stream of :class:`GetTransactionTreesResponse`, used to enrich the stream with
        exercise events. Transactions included in this message that are _not_ in ``tx_stream_pb``
        will be discarded.
    :param last_offset_override:
        An optional last offset, that, if specified AND different from the last offset of the
        stream, causes a synthetic :class:`OffsetEvent` to be created at the end.
    :return:
    """
    events = []  # type: List[OffsetEvent]

    events_by_offset = dict()  # type: Dict[str, List[OffsetEvent]]
    for item_pb in tx_stream_pb:
        for transaction_pb in item_pb.transactions:
            events_by_offset[transaction_pb.offset] = list(
                to_transaction_chunk(context, transaction_pb))

    if tt_stream_pb is not None:
        for transaction_tree_pb in tt_stream_pb:
            for transaction_pb in transaction_tree_pb.transactions:
                tx_events = events_by_offset.get(transaction_pb.offset)
                if tx_events is not None:
                    tx_events[-1:-1] = from_transaction_tree(context, transaction_pb)

    for tx_events in events_by_offset.values():
        events.extend(tx_events)

    if last_offset_override is not None:
        last_time = None if not events else events[-1].time
        last_offset = None if not events else events[-1].offset
        if last_offset != last_offset_override:
            events.append(context.offset_event(last_time, last_offset_override))

    return events


def to_acs_events(
        context: 'BaseEventDeserializationContext',
        acs_stream_pb: 'Iterable[Any]') -> 'Sequence[ActiveContractSetEvent]':
    return [acs_evt
            for acs_response_pb in acs_stream_pb
            for acs_evt in to_acs_event(context, acs_response_pb)]


def from_transaction_tree(context: 'BaseEventDeserializationContext', tt_pb: 'G.TransactionTree') \
        -> 'Sequence[OffsetEvent]':

    t_context = context.transaction(
        time=to_datetime(tt_pb.effective_at),
        offset=tt_pb.offset,
        command_id=tt_pb.command_id,
        workflow_id=tt_pb.workflow_id)

    events = []
    for evt_pb in tt_pb.events_by_id.values():
        evt = to_event(t_context, evt_pb)
        if isinstance(evt, ContractExercisedEvent):
            events.append(evt)

    return events


def to_acs_event(context: BaseEventDeserializationContext, acs_pb: 'G.ActiveContractSetResponse'):
    acs_context = context.active_contract_set(acs_pb.offset, acs_pb.workflow_id)
    contract_events = \
        [evt
         for evt in (to_created_event(acs_context, evt_pb) for evt_pb in acs_pb.active_contracts)
         if evt is not None]
    return [acs_context.active_contract_set_event(contract_events)]


def to_transaction_chunk(context: BaseEventDeserializationContext, tx_pb: 'G.Transaction') \
        -> 'Sequence[OffsetEvent]':
    """
    Return a sequence of events parsed from a Ledger API ``Transaction`` protobuf message.

    :param context:
        Additional information taken from the enclosing message.
    :param tx_pb:
        The Ledger API ``Transaction`` to parse.
    :return:
        A :class:`TransactionStartEvent`, followed by zero or more :class:`ContractCreateEvent`
        and/or :class:`ContractArchiveEvent`, followed by :class:`TransactionEndEvent`.
    """

    t_context = context.transaction(
        time=to_datetime(tx_pb.effective_at),
        offset=tx_pb.offset,
        command_id=tx_pb.command_id,
        workflow_id=tx_pb.workflow_id)

    contract_events = [to_event(t_context, evt_pb) for evt_pb in tx_pb.events]
    contract_events = [evt for evt in contract_events if evt is not None]

    return [t_context.transaction_start_event(contract_events),
            *contract_events,
            t_context.transaction_end_event(contract_events)]


def to_event(
        context: 'Union[TransactionEventDeserializationContext, ActiveContractSetEventDeserializationContext]',
        evt_pb: 'G.Event') \
        -> 'Optional[BaseEvent]':
    try:
        event_type = evt_pb.WhichOneof('event')
    except ValueError:
        try:
            event_type = evt_pb.WhichOneof('kind')
        except ValueError:
            LOG.error('Deserialization error into an event of %r', evt_pb)
            raise

    if 'created' == event_type:
        return to_created_event(context, evt_pb.created)
    elif 'exercised' == event_type:
        return to_exercised_event(context, evt_pb.exercised)
    elif 'archived' == event_type:
        return to_archived_event(context, evt_pb.archived)
    else:
        raise ValueError(f'unknown event type: {event_type}')


def to_created_event(
        context: 'Union[TransactionEventDeserializationContext, ActiveContractSetEventDeserializationContext]',
        cr: 'G.CreatedEvent') \
        -> 'Optional[ContractCreateEvent]':
    type_ref = to_type_ref(cr.template_id)
    candidates = context.store.resolve_template_type(type_ref)
    if len(candidates) == 0:
        LOG.warning('Could not find metadata for %s!', type_ref)
        return None
    elif len(candidates) > 1:
        LOG.error('The template identifier %s is not unique within its metadata!', candidates)
        return None

    ((type_ref, tt),) = candidates.items()

    tt_context = TypeEvaluationContext.from_store(context.store)

    cid = ContractId(cr.contract_id, type_ref)
    cdata = to_record(tt_context, tt, cr.create_arguments)
    event_id = cr.event_id
    witness_parties = tuple(cr.witness_parties)

    return context.contract_created_event(cid, cdata, event_id, witness_parties)


def to_exercised_event(
        context: 'TransactionEventDeserializationContext',
        er: 'G.ExercisedEvent') \
        -> 'Optional[ContractExercisedEvent]':
    type_ref = to_type_ref(er.template_id)
    candidates = context.store.resolve_template_type(type_ref)
    if len(candidates) == 0:
        LOG.warning('Could not find metadata for %s!', type_ref)
        return None
    elif len(candidates) > 1:
        LOG.error('The template identifier %s is not unique within its metadata!', candidates)
        return None

    ((type_ref, tt),) = candidates.items()

    tt_context = TypeEvaluationContext.from_store(context.store)
    choice_candidates = context.store.resolve_choice(type_ref, er.choice)
    if len(candidates) == 0:
        LOG.warning('Could not find metadata for %s!', type_ref)
        return None
    elif len(candidates) > 1:
        LOG.error('The template identifier %s is not unique within its metadata!', candidates)
        return None

    ((choice_ref, cc),) = choice_candidates.items()

    cid = ContractId(er.contract_id, type_ref)
    event_id = er.event_id
    witness_parties = tuple(er.witness_parties)
    try:
        contract_creating_event_id = er.contract_creating_event_id
    except AttributeError:
        contract_creating_event_id = None
    choice = er.choice
    choice_args = to_natural_type(tt_context, cc.data_type, er.choice_argument)
    acting_parties = tuple(er.acting_parties)
    consuming = er.consuming
    child_event_ids = er.child_event_ids
    exercise_result = to_natural_type(tt_context, cc.return_type, er.exercise_result)

    return context.contract_exercised_event(
        cid, None, event_id, witness_parties, contract_creating_event_id,
        choice, choice_args, acting_parties, consuming, child_event_ids, exercise_result)


def to_archived_event(
        context: 'TransactionEventDeserializationContext',
        ar: 'G.ArchivedEvent') \
        -> 'Optional[ContractArchiveEvent]':
    type_ref = to_type_ref(ar.template_id)
    candidates = context.store.resolve_template_type(type_ref)
    if len(candidates) == 0:
        LOG.warning('Could not find metadata for %s!', type_ref)
        return None
    elif len(candidates) > 1:
        LOG.error('The template identifier %s is not unique within its metadata!', candidates)
        return None

    ((type_ref, tt),) = candidates.items()
    event_id = ar.event_id
    witness_parties = tuple(ar.witness_parties)

    cid = ContractId(ar.contract_id, type_ref)
    return context.contract_archived_event(cid, None, event_id, witness_parties)


def to_type_ref(identifier: 'G.Identifier') -> 'TypeReference':
    return TypeReference(
        TypeConName(
            ModuleRef(
                PackageRef(identifier.package_id),
                DottedName(identifier.module_name.split('.'))
            ),
            DottedName(identifier.entity_name.split('.')).segments))


def to_natural_type(context: TypeEvaluationContext, data_type: Type, obj: 'G.Value') -> Any:
    ctor = obj.WhichOneof('Sum')
    if ctor == 'record':
        return to_record(context, data_type, obj.record)
    elif ctor == 'variant':
        return to_variant(context, data_type, obj.variant)
    elif ctor == 'map':
        return to_map(context, data_type, obj.map)
    elif ctor == 'contract_id':
        return to_contract_id(context, data_type, obj.contract_id)
    elif ctor == 'list':
        return to_list(context, data_type, obj.list)
    elif ctor == 'optional':
        return to_optional(context, data_type, obj.optional)
    elif ctor == 'enum':
        return to_enum(obj.enum)
    elif ctor == 'int64':
        return to_int64(obj.int64)
    elif ctor == 'numeric':
        return to_decimal(obj.numeric)
    elif ctor == 'text':
        return to_text(obj.text)
    elif ctor == 'date':
        return to_date(obj.date)
    elif ctor == 'timestamp':
        return to_datetime(obj.timestamp)
    elif ctor == 'party':
        return to_party(obj.party)
    elif ctor == 'bool':
        return to_bool(obj.bool)
    elif ctor == 'unit':
        return to_unit(obj.unit)
    elif ctor is None:
        return None
    else:
        raise ValueError(f'unhandled value type: {ctor!r}')


def to_record(context: TypeEvaluationContext, tt: Type, record: 'G.Record') -> dict:
    def process(child_context: TypeEvaluationContext, rt: RecordType) -> dict:
        args_list = rt.as_args_list()

        natural = dict()
        for (name, field_type), field in zip(args_list, record.fields):
            natural[name] = to_natural_type(child_context.append_path(name), field_type, field.value)
        return natural

    return type_evaluate_dispatch_default_error(on_record=process)(context, tt)


def to_variant(context: TypeEvaluationContext, tt: Type, variant: 'G.Variant') -> Any:
    """
    Convert an on-the-wire :class:`G.Variant` to a Python type.

    :param context: The :class:`TypeEvaluationContext`
    :param tt: The DAML :class:`Type` to convert to.
    :param variant: The on-the-wire :class:`G.Variant` Protobuf message.
    :return: The native Python representation of this variant.
    """
    def process(child_context: TypeEvaluationContext, vt: VariantType) -> dict:
        ctor = variant.constructor
        field_type = vt.field_type(ctor)
        return {ctor: to_natural_type(child_context.append_path(ctor), field_type, variant.value)}

    return type_evaluate_dispatch_default_error(on_variant=process)(context, tt)


def to_map(context: TypeEvaluationContext, tt: Type, map_pb: 'G.Map') -> 'Mapping[str, Any]':
    def process(child_context: TypeEvaluationContext, mt: TextMapType) -> dict:
        return {
            entry_pb.key:
            to_natural_type(child_context.append_path(f'[{entry_pb.key}]'),
                            mt.value_type,
                            entry_pb.value)
            for entry_pb in map_pb.entries}

    return type_evaluate_dispatch_default_error(on_text_map=process)(context, tt)


def to_contract_id(context: TypeEvaluationContext, tt: Type, contract_id: str) \
        -> ContractId:
    def process(_: TypeEvaluationContext, ct: ContractIdType) -> ContractId:
        return ContractId(contract_id, ct.type_parameter)
    return type_evaluate_dispatch_default_error(on_contract_id=process)(context, tt)


def to_list(context: TypeEvaluationContext, tt: Type, list_: 'G.List') -> list:
    def process(child_context: TypeEvaluationContext, lt: ListType) -> list:
        return [to_natural_type(child_context.append_path(f'[{i}]'), lt.type_parameter, element)
                for i, element in enumerate(list_.elements)]
    return type_evaluate_dispatch_default_error(on_list=process)(context, tt)


def to_optional(context: TypeEvaluationContext, tt: Type, optional: 'G.Optional') -> Any:
    def process(child_context: TypeEvaluationContext, ot: OptionalType) -> list:
        return to_natural_type(child_context.append_path(f'?'), ot.type_parameter, optional.value)
    return type_evaluate_dispatch_default_error(on_optional=process)(context, tt)


def to_enum(enum: 'Union[str, G.Enum]') -> str:
    return getattr(enum, 'constructor', enum)


def to_int64(int64: int) -> int:
    return int64


def to_decimal(decimal: str) -> Decimal:
    return Decimal(decimal)


def to_text(text: str) -> str:
    return text


def to_party(party: str) -> str:
    return party


def to_bool(bool_: bool) -> bool:
    return bool_


def to_unit(_: Empty) -> dict:
    return {}
