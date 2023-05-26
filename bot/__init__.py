from functools import cached_property
from db import User, State
from sqlalchemy import select
from sqlalchemy.orm import Session

from bot.exceptions import EndConversationException
from fa_dependencies import get_db

CONVERSATION_STEPS = {
    'first_step': {
        'positive':
            {
                'step': 'STEP_1',
                'question': 'Привет. Я помогу отличить кота от хлеба. Объект перед тобой квадратный?'
            }
        },
    'second_step': {
        'positive': {
            'step': 'STEP_2',
            'question': 'У него есть уши?'
        }
    }
}

ANSWERS = {
    'ага': True,
    'пожалуй': True,
    'конечно': True,
    'да': True,
    'нет, конечно': False,
    'ноуп': False,
    'найн': False,
    'нет': False
}

RE_ASK_QUESTION = 'Уточните свой вопрос'


class Bot:

    def __init__(self, user_id: int, db: Session):
        self.db = db
        self.user = self.db.query(User).filter(User.id == user_id).first() or self.create_user(user_id)

    @cached_property
    def last_state(self):
        a = self.db.execute(select(self.user).join(self.user.states))
        b = self.user.states
        b = 1
        # return self.user.states.first()

    def create_user(self, user_id):
        user = User(id=user_id)
        self.db.add(user)
        state = State(
            step=1,
            question=CONVERSATION_STEPS['first_step']['positive']['question'],
        )
        user.states.append(state)
        self.db.commit()
        self.db.refresh(user)
        return user

    def start_dialogue(self):
        return self.last_state.question

    def process_answer(self, answer: str):
        answer = ANSWERS.get(answer.lower())
        if not answer:
            return RE_ASK_QUESTION
        self.set_conversation_step()
        self.last_state.update(answer=answer)

    def set_conversation_step(self, step: str = 1):
        current_step = self.last_state.step
        if current_step == 3:
            raise EndConversationException
        self.last_state.update(step=current_step + 1)


    # def ask_question(self):
    #     return self.questions.get(self.state.step)
    #
    # @property
    # def bot_answer(self):
    #     return self.state.answer
    #
    # def start_dialogue(self):
    #     self.set_conversation_step('STEP_1')
    #     return 'Привет. Я помогу отличить кота от хлеба. Объект перед тобой квадратный?'
    #
    # def continue_dialogue(self, step):
    #     pass
    #
    #

