from prisma import Prisma

def init_connection() -> Prisma:
    db = Prisma()
    db.connect()
    return db

db = init_connection()

def save_open_ai_key(key):
    user = db.user.find_first()
    if (user == None):
        db.user.create({
            'openAiKey': key
        })
    else:
        db.user.update(
            where={'id': user.id},
            data={'openAiKey': key}
        )

def get_user_ai_key():
    user = db.user.find_first()
    try:
        return user.openAiKey   
    except:
        return None