from aiogram.fsm.state import StatesGroup, State


class AdminState(StatesGroup):
    add_product_title = State()
    add_product_description = State()
    remove_from_menu_id = State()
    add_to_menu_id = State()
    delete_product_id = State()
    add_product_price = State()
    add_product_name = State()
    AdminState = State()
    message = State()
    confirmation = State()
