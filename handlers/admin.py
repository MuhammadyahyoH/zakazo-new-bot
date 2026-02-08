
from aiogram.fsm.context import FSMContext

from core.db_settings import execute_query
from states import AdminState
from aiogram import Router,types,F
router = Router()


@router.message(F.text == '👀 Show all products')
async def show_all_products_handler(message: types.Message):
    products = execute_query(
        "SELECT id, title, price, description FROM products ORDER BY id",
        fetch="all"
    )
    if not products:
        await message.answer("📦 No products available")
        return

    for prod in products:
        text = f"ID: {prod[0]} | Title: {prod[1]} | Price: {prod[2]} | Desc: {prod[3]}"
        await message.answer(text=text)


@router.message(F.text == '📝Add new product')
async def add_product_handler(message: types.Message, state: FSMContext):
    await message.answer("📝 Enter product title")
    await state.set_state(AdminState.add_product_title)

@router.message(AdminState.add_product_title)
async def get_product_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("💰 Enter product price")
    await state.set_state(AdminState.add_product_price)

@router.message(AdminState.add_product_price)
async def get_product_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("📝 Enter product description")
    await state.set_state(AdminState.add_product_description)

@router.message(AdminState.add_product_description)
async def get_product_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    title = data['title']
    price = data['price']
    description = message.text

    execute_query(
        "INSERT INTO products (title, price, description) VALUES (%s, %s, %s)",
        (title, price, description)
    )
    await message.answer(f"✅ Product added: {title} | Price: {price}")
    await state.clear()


@router.message(F.text == "🗑️ Delete product")
async def delete_product_handler(message: types.Message, state: FSMContext):
    products = execute_query(
        "SELECT id, title, price FROM products ORDER BY id",
        fetch="all"
    )
    if not products:
        await message.answer("📦 No products to delete")
        return

    text = "Select product ID to delete:\n"
    for prod in products:
        text += f"{prod[0]}: {prod[1]} | {prod[2]}\n"
    await message.answer(text=text)
    await state.set_state(AdminState.delete_product_id)

@router.message(AdminState.delete_product_id)
async def process_delete_product(message: types.Message, state: FSMContext):
    product_id = message.text
    result = execute_query(
        "SELECT title FROM products WHERE id = %s",
        (product_id,),
        fetch="one"
    )

    if not result:
        await message.answer("❌ Invalid product ID")
    else:
        execute_query("DELETE FROM products WHERE id = %s", (product_id,))
        await message.answer(f"✅ Deleted product: {result[0]}")
    await state.clear()


@router.message(F.text == "📅 Show today's menu")
async def show_today_menu(message: types.Message):
    menu = execute_query(
        "SELECT p.id, p.title, p.price FROM menu_products tm "
        "JOIN products p ON tm.product_id = p.id ORDER BY p.id",
        fetch="all"
    )
    if not menu:
        await message.answer("📋 Today's menu is empty")
        return

    text = "📅 Today's Menu:\n"
    for prod in menu:
        text += f"{prod[0]}: {prod[1]} | {prod[2]}\n"
    await message.answer(text=text)


@router.message(F.text == "➕ Add product to today's menu")
async def add_to_today_menu_handler(message: types.Message, state: FSMContext):
    products = execute_query(
        "SELECT id, title, price FROM products ORDER BY id",
        fetch="all"
    )
    if not products:
        await message.answer("📦 No products available to add")
        return

    text = "Select product ID to add to today's menu:\n"
    for prod in products:
        text += f"{prod[0]}: {prod[1]} | {prod[2]}\n"

    await message.answer(text=text)
    await state.set_state(AdminState.add_to_menu_id)


@router.message(AdminState.add_to_menu_id)
async def process_add_to_menu(message: types.Message, state: FSMContext):
    product_id = message.text
    exists = execute_query(
        "SELECT 1 FROM products WHERE id = %s",
        (product_id,),
        fetch="one"
    )
    already_in_menu = execute_query(
        "SELECT 1 FROM menu_products WHERE product_id = %s",
        (product_id,),
        fetch="one"
    )

    if not exists:
        await message.answer("❌ Invalid product ID")
    elif already_in_menu:
        await message.answer("ℹ️ Product already in today's menu")
    else:
        execute_query(
            "INSERT INTO menu_products (date_of_menu, product_id) VALUES (CURRENT_DATE, %s)",
            (product_id,)
        )
        await message.answer(f"✅ Added product ID {product_id} to today's menu")
    await state.clear()


@router.message(F.text == "🗑️ Remove product from today's menu")
async def remove_from_todays_menu_handler(message: types.Message, state: FSMContext):
    menu = execute_query(
        "SELECT p.id, p.title, p.price FROM menu_products tm "
        "JOIN products p ON tm.product_id = p.id ORDER BY p.id",
        fetch="all"
    )
    if not menu:
        await message.answer("📋 Today's menu is empty")
        return

    text = "Select product ID to remove from today's menu:\n"
    for prod in menu:
        text += f"{prod[0]}: {prod[1]} | {prod[2]}\n"
    await message.answer(text=text)
    await state.set_state(AdminState.remove_from_menu_id)


@router.message(AdminState.remove_from_menu_id)
async def process_remove_from_menu(message: types.Message, state: FSMContext):
    product_id = message.text
    exists = execute_query(
        "SELECT 1 FROM menu_products WHERE product_id = %s",
        (product_id,),
        fetch="one"
    )

    if not exists:
        await message.answer("❌ Product not in today's menu")
    else:
        execute_query(
            "DELETE FROM menu_products WHERE product_id = %s",
            (product_id,)
        )
        await message.answer(f"✅ Removed product ID {product_id} from today's menu")
    await state.clear()
