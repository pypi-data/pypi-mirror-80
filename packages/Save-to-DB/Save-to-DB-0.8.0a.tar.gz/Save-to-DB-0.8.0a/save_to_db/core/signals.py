""" This models contains all the signals used by the library. """

from .utils.signal import Signal

all_signals = []


def __create_signal(name):
    global all_signals
    signal = Signal(name)
    all_signals.append(signal)
    return signal


#: Signal is emitted when a persistance process is started.
#:
#: :param item: The item that was used to persist the data.
#: :param item_structure: Dictionary with single item classes as keys and lists
#:     of single item instances as values.
before_db_persist = __create_signal("before_db_persist")

#: Signal is emitted when a persistance process is completed.
#:
#: :param items: List of persisted items.
#: :param models: List of lists of persisted models corresponding to the list of
#:     items. One item can have more then one model updated.
after_db_persist = __create_signal("after_db_persist")

#: Signal is emitted during persistence process for an item cannot that be used
#: for persistence.
#:
#:    .. note::
#:        If possible, related items will still be persisted.
#:
#: :param item: A dropped item.
#: :param str reason: A short explanation why the item was dropped.
item_dropped = __create_signal("item_dropped")

item_dropped.reason_cannot_create_get_only_mode = (
    "Get only mode with no model matching the item in database"
)
item_dropped.reason_cannot_create_update_only_mode = (
    "Update only mode with no model matching the item in database"
)
item_dropped.reason_cannot_create_not_enough_data = (
    "No models matching the item and not enouth data to create new model"
)
