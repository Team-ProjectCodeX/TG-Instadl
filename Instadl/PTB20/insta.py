# SOURCE https://github.com/Team-ProjectCodeX
# CREATED BY https://t.me/O_okarma
# PROVIDED BY https://t.me/ProjectCodeX

# <============================================== IMPORTS =========================================================>
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from httpx import AsyncClient, Timeout

from Mikobot import function

# <=======================================================================================================>

DOWNLOADING_STICKER_ID = (
    "CAACAgIAAxkBAAEDv_xlJWmh2-fKRwvLywJaFeGy9wmBKgACVQADr8ZRGmTn_PAl6RC_MAQ"
)
API_URL = "https://karma-api2.vercel.app/instadl"  # Replace with your actual API URL

# HTTPx Async Client
state = AsyncClient(
    http2=True,
    verify=False,
    headers={
        "Accept-Language": "en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edge/107.0.1418.42",
    },
    timeout=Timeout(20),
)

# <================================================ FUNCTION =======================================================>
async def instadl_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /instadl [Instagram URL]")
        return

    link = context.args[0]
    try:
        downloading_sticker = await update.message.reply_sticker(DOWNLOADING_STICKER_ID)

        # Make an asynchronous GET request to the API using httpx
        response = await state.get(API_URL, params={"url": link})
        data = response.json()

        # Check if the API request was successful
        if "content_url" in data:
            content_url = data["content_url"]

            # Determine content type from the URL
            content_type = "video" if "video" in content_url else "photo"

            # Reply with either photo or video
            if content_type == "photo":
                await update.message.reply_photo(content_url)
            elif content_type == "video":
                await update.message.reply_video(content_url)
            else:
                await update.message.reply_text("Unsupported content type.")
        else:
            await update.message.reply_text(
                "Unable to fetch content. Please check the Instagram URL or try with another Instagram link."
            )

    except Exception as e:
        print(e)
        await update.message.reply_text(
            "An error occurred while processing the request."
        )

    finally:
        await downloading_sticker.delete()


function(
    CommandHandler(["ig", "instagram", "insta", "instadl"], instadl_command_handler)
)
# <================================================ END =======================================================>
