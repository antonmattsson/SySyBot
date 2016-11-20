from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)
import functions
import apikey
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

NAME, TEAM, SPORT, DURATION = range(4)

ev = {}

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def start(bot, update):

    update.message.reply_text('Hi! I am the official SySyBot! \n Please use /submit to sumbit a new excercise!\n'
                              'Or use /scores to see how great your team is doing!')

def submit(bot,update):
    ev[update.message.from_user.id] = {}
    update.message.reply_text('Please tell me your name')
    return NAME

def name(bot,update):
    ev[update.message.from_user.id]['player'] = functions.dumbass(update.message.text)
    update.message.reply_text('What is your team called?')
    return TEAM
    
def team(bot,update):
    ev[update.message.from_user.id]['team'] = functions.dumbass(update.message.text)
    update.message.reply_text('Which sport did you do this time?')
    
    return SPORT
    
def sport(bot,update):
    ev[update.message.from_user.id]['sport'] = functions.dumbass(update.message.text)
    update.message.reply_text('What was the duration of your exercise in hours? (with . as decimal mark)')
    
    return DURATION
    
def duration(bot,update):
    if isfloat(update.message.text):
        ev[update.message.from_user.id]['duration'] = float(update.message.text)
        functions.insert_event(ev[update.message.from_user.id])
        functions.update_teams()
        update.message.reply_text('Impressive! I have registered your exercise')
        
        return ConversationHandler.END
    else:
        update.message.reply_text('Please enter a bare decimal number with point as decimal mark'
                                  'like 2 or 1.8')
        return DURATION
    

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.')

    return ConversationHandler.END

def scores(bot,update):
    update.message.reply_text(functions.get_scores())
    return

def sports(bot,update):
    ev[update.message.from_user.id] = {}
    update.message.reply_text('Please tell me your name')
    return NAME_SPORTS

def name_sports(bot,update):
    ev[update.message.from_user.id]['player'] = functions.dumbass(update.message.text)
    update.message.reply_text('What is your team called?')
    return TEAM_SPORTS

def team_sports(bot,update):
    ev[update.message.from_user.id]['team'] = functions.dumbass(update.message.text)
    update.message.reply_text(functions.get_sports)
    return ConversationHandler.END


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token=apikey.bot_key)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('submit', submit)],

        states={
            NAME: [MessageHandler([Filters.text], name)],

            TEAM: [MessageHandler([Filters.text], team)],

            SPORT: [MessageHandler([Filters.text], sport)],

            DURATION: [MessageHandler([Filters.text], duration)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    conv_handler_sports = ConversationHandler(
        entry_points=[CommandHandler('sports', sports)],

        states={
            NAME_SPORTS: [MessageHandler([Filters.text], name_sports)],

            TEAM_SPORTS: [MessageHandler([Filters.text], team_sports)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    scores_handler = CommandHandler('scores',scores)

    dp.add_handler(conv_handler)
    
    dp.add_handler(scores_handler)

    dp.add_handler(conv_handler_sports)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
