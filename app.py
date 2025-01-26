import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ChatMemberUpdated
from aiogram.dispatcher.router import Router
from aiogram.filters import Command
import openai
import random

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Replace these with your actual keys
TELEGRAM_BOT_TOKEN = "8061761170:AAHU2sWpV3-5q6Mj3m4AzKeXKU1_JjjI1c4"
OPENAI_API_KEY = "sk-svcacct-6KTY_iNm2MbgNpwCVH2Q9-_XrEYQ8IgOggD9LhDny-Yg5cc5S5RCrAbdY2ZHU0fWOT3BlbkFJ43JV0cOYk4m0fvCxyBUAidHRBx2NHuMUg9Jxq_h5Ik6-gz-zMEA1pF6ajxHTil97QA"

# Set up OpenAI API key
openai.api_key = OPENAI_API_KEY

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
router = Router()  # Create a router for handling commands and messages

periodic_messages = [
    "It's going to be a tremendous day, folks. Stay focused!",
    "Winners don't just work hard—they work smart. Believe me.",
    "The future is in your hands, and it's going to be great. Trust me.",
    "Success is about making deals, and the best deal is with yourself—be the best version of you!",
    "The best is yet to come. Stay positive, folks.",
    "Great things are achieved when we believe in ourselves. You’ve got this!",
    "Big opportunities are right around the corner. Don’t miss them.",
    "Hard work and determination—an unbeatable combination. Believe me.",
    "Winning isn’t everything, but wanting to win is. Let’s aim high!",
    "When you’re confident, you’re already halfway there. Show the world your best!",
    "Every challenge is a chance to grow. Embrace it.",
    "Take action today—no excuses. Winners act, losers complain.",
    "You don’t build success overnight; you build it step by step.",
    "Nothing worth having comes easy. Keep working hard!",
    "Great leaders inspire action. Be the leader of your own life.",
    "Dream big, but don’t forget to plan and execute.",
    "Opportunities don’t wait. Grab them now!",
    "Confidence is key, but preparation unlocks the door.",
    "Every setback is a setup for a comeback. Never give up.",
    "When the going gets tough, the tough get going. Stay strong!",
    "Believe in your vision and never let anyone tell you otherwise.",
    "Discipline is the bridge between goals and achievements. Build it!",
    "Your mindset determines your success. Think big, act bold.",
    "Today’s small wins lead to tomorrow’s big successes.",
    "Surround yourself with positivity—it makes all the difference.",
    "The sky’s the limit when you work hard and stay focused.",
    "Take risks, but take smart ones. Fortune favors the bold.",
    "Success is a journey, not a destination. Enjoy the ride!",
    "Start where you are. Use what you have. Do what you can.",
    "Big results require big ambitions. Let’s aim high!",
    "Focus on solutions, not problems. That’s how winners think.",
    "Consistency beats intensity. Stay steady, stay strong.",
    "Success doesn’t wait for the lazy. Hustle every day.",
    "The people who succeed are those who outwork everyone else.",
    "Every day is a fresh start. Make it count.",
    "Persistence beats resistance. Keep pushing forward.",
    "Your network is your net worth. Build strong connections.",
    "Small steps every day lead to giant leaps over time.",
    "Believe in your ideas and work tirelessly to make them real.",
    "You were made for greatness—never settle for less.",
    "Greatness doesn’t come from comfort zones. Push your limits!",
    "The biggest risk is not taking any risks at all. Step up!",
    "Success favors those who show up every day. Be consistent.",
    "You can’t build a reputation on what you’re going to do. Take action now!",
    "Winners see opportunities in every challenge. Find yours.",
    "A goal without a plan is just a wish. Start planning today.",
    "Don't let fear stop you. Let it fuel your growth instead.",
    "Strong foundations lead to skyscraper successes. Build wisely.",
    "Change the game by bringing your A-game every day.",
    "Good things come to those who hustle and grind. Keep at it!",
    "Every decision shapes your destiny. Choose wisely.",
    "Stay hungry for success, but never forget to stay humble.",
    "Courage isn’t the absence of fear; it’s acting despite it.",
    "You’re closer to success than you think. Keep going!",
    "Don’t follow the crowd. Lead it with bold ideas.",
    "Think big, act bigger. That’s the secret to success.",
    "Your potential is limitless. Unlock it every single day.",
    "Challenges are proof that you’re leveling up. Face them head-on.",
    "Energy flows where focus goes. Stay laser-focused!",
    "Your vision is your greatest asset. Protect and pursue it.",
    "The world rewards doers, not dreamers. Be a doer.",
    "Don’t wait for the perfect moment. Create it.",
    "Every day is a new chance to be better than yesterday.",
    "Keep climbing. The view from the top is worth it.",
    "Never underestimate the power of a positive mindset.",
    "Setbacks are just setups for comebacks. Bounce back stronger!",
    "Big results come from taking bold actions.",
    "Winners are just losers who kept trying. Never give up.",
    "In the middle of every difficulty lies opportunity. Seek it.",
    "Success is built on the foundation of discipline and effort.",
    "The harder the struggle, the sweeter the victory.",
    "Be the kind of person others want to follow.",
    "Visionaries don’t wait for opportunities; they create them.",
    "The only limit is the one you set in your mind.",
    "Every moment is an opportunity to rewrite your story.",
    "You don’t need luck—you need strategy and hard work.",
    "Focus on progress, not perfection. Small steps matter.",
    "Your actions today define your success tomorrow.",
    "Success isn’t about luck—it’s about preparation and perseverance."
]

# Variable to store group chat ID
group_chat_id = None

# Categories: Facts, Quotes, Billionaires
facts = [
    "Donald Trump was the 45th president of the United States, serving from 2017 to 2021.",
    "Trump was born on June 14, 1946, in Queens, New York City.",
    "Before his presidency, Trump was a real estate developer and television personality.",
    "Donald Trump hosted the reality TV show 'The Apprentice' from 2004 to 2015.",
    "Trump's real estate company, The Trump Organization, was founded in 1927 by his grandmother and father.",
    "He graduated from the Wharton School of the University of Pennsylvania in 1968 with a degree in economics.",
    "Trump Tower, one of his most famous properties, is located on Fifth Avenue in New York City.",
    "In 2016, Trump became the first person without prior military or political experience to be elected president.",
    "Donald Trump has been married three times and has five children: Donald Jr., Ivanka, Eric, Tiffany, and Barron.",
    "Trump authored several books, including the best-selling 'The Art of the Deal' in 1987.",
    "During his presidency, Trump focused on tax reform, deregulation, and reshaping U.S. trade policies.",
    "He is the only president in U.S. history to have been impeached twice by the House of Representatives.",
    "Trump's campaign slogan in 2016 was 'Make America Great Again' (MAGA).",
    "As president, Trump appointed three Supreme Court justices: Neil Gorsuch, Brett Kavanaugh, and Amy Coney Barrett.",
    "Trump announced his candidacy for president in 2015 from Trump Tower in New York City.",
    "His administration passed the Tax Cuts and Jobs Act in 2017, which significantly reduced corporate tax rates.",
    "Trump withdrew the United States from the Paris Climate Agreement in 2017.",
    "He launched the Space Force in 2019 as the sixth branch of the U.S. military.",
    "Trump was the first sitting U.S. president to meet with a North Korean leader, Kim Jong Un, in 2018.",
    "In 2020, Trump tested positive for COVID-19 and was treated at Walter Reed National Military Medical Center.",
    "He oversaw the development and distribution of COVID-19 vaccines under Operation Warp Speed.",
    "Trump was a major figure in the U.S. real estate market, with properties in New York, Las Vegas, and Chicago.",
    "His Mar-a-Lago estate in Florida serves as both a private club and his personal residence.",
    "Trump's net worth has been a topic of debate, with estimates varying significantly over the years.",
    "He received a star on the Hollywood Walk of Fame in 2007 for his work on 'The Apprentice.'",
    "Donald Trump announced his 2024 presidential campaign in November 2022.",
    "He was involved in several high-profile legal and financial controversies throughout his career.",
    "Trump has a history of philanthropy, including donations to veterans’ causes and cancer research.",
    "His presidency saw record highs in the U.S. stock market before the COVID-19 pandemic.",
    "Trump brokered the Abraham Accords, normalizing relations between Israel and several Arab nations.",
    "He famously uses Twitter as a platform for communicating with supporters and critics alike.",
    "In 2019, Trump declared a national emergency to fund the construction of a wall along the U.S.-Mexico border.",
    "Trump has been a member of the Republican Party for most of his political career but was previously a Democrat.",
    "He was awarded an honorary degree from Liberty University in 2012.",
    "In 1983, Trump purchased the Mar-a-Lago estate, which later became his primary residence.",
    "The Trump International Hotel in Washington, D.C., opened in 2016 and became a focal point during his presidency.",
    "Donald Trump has been featured in cameo roles in movies like 'Home Alone 2: Lost in New York.'",
    "He was one of the most controversial and polarizing figures in modern American politics.",
    "Trump's presidency saw a significant increase in federal judicial appointments.",
    "He was a vocal critic of the Affordable Care Act and sought to repeal and replace it.",
    "Trump was the first president to be banned from several major social media platforms after the January 6 Capitol riots.",
    "He signed the USMCA trade agreement, replacing NAFTA, in 2020.",
    "Trump declared a trade war with China, imposing tariffs on hundreds of billions of dollars in goods.",
    "Donald Trump's campaign rallies drew massive crowds and were a hallmark of his political style.",
    "He supported the nomination of Jerusalem as the capital of Israel and moved the U.S. embassy there in 2018.",
    "Trump received a $1 million loan from his father, Fred Trump, to start his business career.",
    "In 1989, he sponsored a high-profile advertising campaign calling for the death penalty in the Central Park Five case.",
    "Trump's administration expanded oil and gas drilling on federal lands and approved the Keystone XL pipeline.",
    "He signed an executive order to ban certain immigration practices, including travel from several Muslim-majority countries.",
    "Trump has been nominated for the Nobel Peace Prize multiple times for his foreign policy initiatives.",
    "He was one of the oldest presidents ever elected, taking office at the age of 70.",
    "Trump's tax returns were a contentious issue during and after his presidency."
]


quotes = [
    "Sometimes by losing a battle you find a new way to win the war. - Donald Trump",
    "What separates the winners from the losers is how a person reacts to each new twist of fate. - Donald Trump",
    "If you're going to think, think big. - Donald Trump",
    "I like thinking big. If you’re going to be thinking anything, you might as well think big. - Donald Trump",
    "Without passion, you don’t have energy. Without energy, you have nothing. - Donald Trump",
    "In the end, you’re measured not by how much you undertake but by what you finally accomplish. - Donald Trump",
    "Sometimes your best investments are the ones you don’t make. - Donald Trump",
    "As long as you’re going to be thinking anyway, think big. - Donald Trump",
    "Courage is not the absence of fear. Courage is conquering fear. - Donald Trump",
    "What separates the winners from the losers is how a person reacts to each new twist of fate. - Donald Trump",
    "You have to think anyway, so why not think big? - Donald Trump",
    "Anyone who thinks my story is anywhere near over is sadly mistaken. - Donald Trump",
    "Show me someone without an ego, and I’ll show you a loser. - Donald Trump",
    "Sometimes it takes a little courage to step up and show people what you’re made of. - Donald Trump",
    "You have to have confidence in yourself. You have to believe in your ability, and be tough enough to follow through. - Donald Trump",
    "Watch, listen, and learn. You can’t know it all yourself. Anyone who thinks they do is destined for mediocrity. - Donald Trump",
    "Sometimes losing a battle helps you find a new way to win the war. - Donald Trump",
    "Experience taught me a few things. One is to listen to your gut, no matter how good something sounds on paper. - Donald Trump",
    "I try to learn from the past, but I plan for the future by focusing exclusively on the present. - Donald Trump",
    "Remember, there’s no such thing as an unrealistic goal—just unrealistic timeframes. - Donald Trump",
    "People love me. And you know what, I have been very successful. Everybody loves me. - Donald Trump",
    "Keep going, and never stop. Keep moving forward. - Donald Trump",
    "Think big and live large. - Donald Trump",
    "Money was never a big motivation for me, except as a way to keep score. The real excitement is playing the game. - Donald Trump",
    "Sometimes it pays to be a little wild. - Donald Trump",
    "Leverage is the most important word in any business. - Donald Trump",
    "Nothing great in the world has been accomplished without passion. - Donald Trump",
    "I have an attention span that’s as long as it has to be. - Donald Trump",
    "Success comes from failure, not from memorizing the right answers. - Donald Trump",
    "A lot of people don’t know how to win. They are afraid of success. - Donald Trump",
    "When somebody challenges you, fight back. Be brutal, be tough. - Donald Trump",
    "When people treat me badly or unfairly or try to take advantage of me, my thoughts are: I get even with them. - Donald Trump",
    "Winning is great, but it's not enough. It's everything. - Donald Trump",
    "Always have passion. Passion will drive you to success. - Donald Trump",
    "Deals are my art form. Other people paint beautifully on canvas or write wonderful poetry. I like making deals, preferably big deals. That’s how I get my kicks. - Donald Trump",
    "I don't do it for the money. I've got enough, much more than I'll ever need. I do it to do it. Deals are my art form. - Donald Trump",
    "Sometimes you have to go through hell to get to heaven. - Donald Trump",
    "It’s always good to be underestimated. - Donald Trump",
    "Success requires passion, drive, and resilience. - Donald Trump"
]

billionaires = [
    {"name": "George Washington", "title": "1st President of the United States", "net_worth": "$525M (inflation-adjusted)", "quote": "It is better to be alone than in bad company."},
    {"name": "Thomas Jefferson", "title": "3rd President of the United States", "net_worth": "$212M (inflation-adjusted)", "quote": "Honesty is the first chapter in the book of wisdom."},
    {"name": "Theodore Roosevelt", "title": "26th President of the United States", "net_worth": "$125M (inflation-adjusted)", "quote": "Believe you can and you're halfway there."},
    {"name": "John F. Kennedy", "title": "35th President of the United States", "net_worth": "$1B (family wealth, inflation-adjusted)", "quote": "Ask not what your country can do for you – ask what you can do for your country."},
    {"name": "Abraham Lincoln", "title": "16th President of the United States", "net_worth": "Modest", "quote": "Whatever you are, be a good one."},
    {"name": "Franklin D. Roosevelt", "title": "32nd President of the United States", "net_worth": "$66M (inflation-adjusted)", "quote": "The only thing we have to fear is fear itself."},
    {"name": "Barack Obama", "title": "44th President of the United States", "net_worth": "$70M", "quote": "The arc of the moral universe is long, but it bends towards justice."},
    {"name": "Donald Trump", "title": "45th President of the United States", "net_worth": "$2.5B", "quote": "Sometimes by losing a battle you find a new way to win the war."},
    {"name": "Joe Biden", "title": "46th President of the United States", "net_worth": "$9M", "quote": "Don’t tell me what you value. Show me your budget, and I’ll tell you what you value."},
    {"name": "Bill Clinton", "title": "42nd President of the United States", "net_worth": "$80M", "quote": "There is nothing wrong with America that cannot be cured by what is right with America."},
    {"name": "Ronald Reagan", "title": "40th President of the United States", "net_worth": "$14M (inflation-adjusted)", "quote": "The greatest leader is not necessarily the one who does the greatest things."},
    {"name": "Andrew Jackson", "title": "7th President of the United States", "net_worth": "$132M (inflation-adjusted)", "quote": "Take time to deliberate; but when the time for action arrives, stop thinking and go in."},
    {"name": "Harry S. Truman", "title": "33rd President of the United States", "net_worth": "Modest", "quote": "The buck stops here."},
    {"name": "Woodrow Wilson", "title": "28th President of the United States", "net_worth": "Modest", "quote": "You are here to enrich the world and you impoverish yourself if you forget the errand."},
    {"name": "Dwight D. Eisenhower", "title": "34th President of the United States", "net_worth": "$9M (inflation-adjusted)", "quote": "Leadership is the art of getting someone else to do something you want done because he wants to do it."},
    {"name": "Jimmy Carter", "title": "39th President of the United States", "net_worth": "$10M", "quote": "We should live our lives as though Christ were coming this afternoon."},
    {"name": "James Madison", "title": "4th President of the United States", "net_worth": "$113M (inflation-adjusted)", "quote": "Knowledge will forever govern ignorance; and a people who mean to be their own governors must arm themselves with the power which knowledge gives."},
    {"name": "John Adams", "title": "2nd President of the United States", "net_worth": "$21M (inflation-adjusted)", "quote": "Liberty cannot be preserved without a general knowledge among the people."},
    {"name": "Ulysses S. Grant", "title": "18th President of the United States", "net_worth": "Modest", "quote": "In every battle, there comes a time when both sides consider themselves beaten. Then he who continues the attack wins."},
    {"name": "James Monroe", "title": "5th President of the United States", "net_worth": "$27M (inflation-adjusted)", "quote": "National honor is the national property of the highest value."}
]

@router.message(Command(commands=["trumphelp"]))
async def send_welcome(message: Message):
    """Handle /start and /help commands."""
    await message.reply("Chat with me using /trump <your text>, or type /president to get inspired. Huge opportunities ahead, trust me.")


@router.message(Command(commands=["president"]))
async def elite_command(message: Message):
    """Handle the /elite command (without any input) to send quotes, facts, or billionaire insights."""
    # Choose the type of response (fact, quote, billionaire)
    response_type = random.choice(["fact", "quote", "billionaire"])

    if response_type == "fact":
        fact = random.choice(facts)
        await message.reply(fact)
    
    elif response_type == "quote":
        quote = random.choice(quotes)
        await message.reply(quote)
    
    elif response_type == "billionaire":
        billionaire = random.choice(billionaires)
        billionaire_info = (f"{billionaire['name']}, {billionaire['title']} | Net Worth: {billionaire['net_worth']}\n"
                            f"Quote: {billionaire['quote']}")
        await message.reply(billionaire_info)


@router.message(Command(commands=["trump"]))
async def chat_with_gpt(message: Message):
    """Handle the /aiagent <text> command to chat with ChatGPT."""
    # Remove the "/aiagent" command and get the user's message
    user_message = message.text[9:].strip()  # Remove "/aiagent " from the message

    if user_message:
        try:
            # Send the user's message to OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a 47th president of USA. Show people how they can win. Please make short but catchy and sharp answers and without hashtags. Act like Donald Trump and chat with user like Donald Trump."},
                    {"role": "user", "content": user_message},
                ]
            )
            # Extract the response text
            gpt_response = response["choices"][0]["message"]["content"]

            # Send the response back to the user
            await message.reply(gpt_response)
        except Exception as e:
            logging.error(f"Error: {e}")
            await message.reply("Sorry, something went wrong. Please try again later.")


@router.chat_member()
async def on_user_joined(member_update: ChatMemberUpdated):
    """Handle when a new member joins the group."""
    if member_update.new_chat_member.status == "member":
        new_member = member_update.new_chat_member.user
        welcome_message = (
            f"Welcome to the future, folks—the best of the best, {new_member.first_name}! 🇺🇸\n"
            "Chat with me using /trump <your text>, or type /president to get inspired. Huge opportunities ahead, trust me. Need help? Just hit /trumphelp—it's going to be tremendous!"
        )
        await bot.send_message(member_update.chat.id, welcome_message)

@router.my_chat_member()
async def track_bot_addition(update: types.ChatMemberUpdated):
    """Track when the bot is added to a group."""
    global group_chat_id
    if update.new_chat_member.status in ["member", "administrator"]:
        group_chat_id = update.chat.id
        logging.info(f"Bot added to group: {group_chat_id}")
        await bot.send_message(
            group_chat_id,
            "Hello, folks! I'm here to bring tremendous opportunities. Use /trump <your text> or /trumphelp to start. It's going to be great!"
        )

async def send_periodic_messages():
    """Send periodic messages to the group."""
    while True:
        if group_chat_id:
            message = random.choice(periodic_messages)
            await bot.send_message(group_chat_id, message)
        await asyncio.sleep(2600)  # Send a message every hour


async def main():
    # Register the router with the dispatcher
    dp.include_router(router)

    # Start the periodic messages task
    asyncio.create_task(send_periodic_messages())

    # Start polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
