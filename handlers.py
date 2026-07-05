import os
import re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
import database
import placeholder_generator
import utils
import keyboards
from config import TEMP_DIR

DIMENSIONS_STAGE, COLOR_STAGE, TEXT_STAGE = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    utils.ensure_temp_directory()
    uid = update.effective_user.id
    await database.register_user(uid)
    
    welcome = (
        "👋 Welcome to *PlaceGen Bot*!\n"
        "Instantly generate beautiful placeholder images for websites, apps, mockups, and presentations.\n\n"
        "🖼 *Create custom placeholder images*\n"
        "📐 *Choose any custom canvas dimensions parameters*\n"
        "🎨 *Customize text headers and backdrop colors code strings*\n\n"
        "Select an option below or enter your preferred image size to begin."
    )
    if update.message:
        await update.message.reply_text(welcome, reply_markup=keyboards.get_main_menu(), parse_mode="Markdown")
    return ConversationHandler.END

async def start_convo_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["gen_data"] = {}
    
    kb = [[InlineKeyboardButton("1080×1080 (Instagram)", callback_data="sz_1080x1080")],
          [InlineKeyboardButton("1920×1080 (FHD Web)", callback_data="sz_1920x1080")],
          [InlineKeyboardButton("1200×630 (Facebook OpenGraph)", callback_data="sz_1200x630")]]
    await query.message.reply_text("📐 Please enter target dimensions explicitly as `WIDTHxHEIGHT` (e.g. `800x600`) or select a baseline preset configuration model item row below:", 
                                   reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    return DIMENSIONS_STAGE

async def handle_dimensions_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text if update.message else update.callback_query.data.split("_")[1]
    msg_obj = update.message if update.message else update.callback_query.message
    
    # Extract structural dimensions bounding matching matrices parameters using regex evaluations patterns
    match = re.match(r"^(\d+)[x×](\d+)$", text.strip().lower())
    if not match:
        await msg_obj.reply_text("❌ Formatting input tracking match validation trace error loop. Please use exact format rule style: `800x600`")
        return DIMENSIONS_STAGE
        
    w, h = int(match.group(1)), int(match.group(2))
    if not (50 <= w <= 5000 and 50 <= h <= 5000):
        await msg_obj.reply_text("❌ Target boundary parameters out of active scope limits. Please maintain dimension thresholds bounded between 50px up to 5000px metrics values scales.")
        return DIMENSIONS_STAGE
        
    context.user_data["gen_data"]["w"] = w
    context.user_data["gen_data"]["h"] = h
    
    await msg_obj.reply_text("🎨 Enter background and text hex color values separated by a space string (e.g. `4F46E5 FFFFFF` or color names like `blue white`):")
    return COLOR_STAGE

async def handle_color_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    parts = update.message.text.strip().split()
    bg = parts[0] if len(parts) >= 1 else "4F46E5"
    tx = parts[1] if len(parts) >= 2 else "FFFFFF"
    
    context.user_data["gen_data"]["bg"] = bg
    context.user_data["gen_data"]["tx"] = tx
    
    await update.message.reply_text("📝 Enter custom label text display overlay string, or type `/skip` to show default image metric dimensions markers instead:")
    return TEXT_STAGE

async def handle_text_and_compile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    input_text = update.message.text.strip()
    display_string = "" if input_text.lower() == "/skip" else input_text
    
    await update.message.reply_text("⚡ Processing vector bounding configurations models rules constraints... Rendering dummy image placeholder canvas asset now.")
    
    data = context.user_data["gen_data"]
    output_img_file = placeholder_generator.create_placeholder(data["w"], data["h"], data["bg"], data["tx"], display_string, uid)
    
    if output_img_file and os.path.exists(output_img_file):
        dim_str = f"{data['w']}x{data['h']}"
        with open(output_img_file, "rb") as f:
            await update.message.reply_document(document=f, filename=f"placeholder_{dim_str}.png", caption=f"✅ Dummy placeholder generation complete maps successfully via PlaceGen Engine layers.")
        await database.save_placeholder_log(uid, dim_str, data["bg"], display_string if display_string else dim_str)
        utils.clean_user_files(uid)
    else:
        await update.message.reply_text("❌ System canvas layout generation exception trace thread error loop block execution failure.")
        
    return ConversationHandler.END

async def menu_navigation_routing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    
    if query.data == "nav_view_history":
        history = await database.get_user_history(uid)
        if not history:
            await query.message.reply_text("📂 No creation operations footprints log tracks recorded within your cloud database records matrix history index yet.", reply_markup=keyboards.get_main_menu())
        else:
            msg = "📂 *Your Recent Dummy Layout Creation Logs Footprints History Index:*\n\n" + "\n".join([f"- Dimensions: `{item['dimensions']}` | Color: `{item['bg_color']}` | Label: `{item['text_content']}`" for item in history])
            await query.message.reply_text(msg, reply_markup=keyboards.get_main_menu(), parse_mode="Markdown")
    elif query.data == "nav_view_help":
        help_text = (
            "❓ *PlaceGen Core Engineering Documentation Manual*\n\n"
            "Placeholder dummy layout containers enable rapid interface mapping validation parameters routines "
            "allowing front-end app interface modules to align accurately before raw graphic prints components production loops initialization.\n\n"
            "💡 *Usage:* Click 'Generate Placeholder', supply target grid footprints width and height metrics ratios rules, and download raw transparent print blocks data."
        )
        await query.message.reply_text(help_text, reply_markup=keyboards.get_main_menu(), parse_mode="Markdown")
