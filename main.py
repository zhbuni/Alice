from flask import Flask, request
import logging
import json
import random
import os

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}
dict_of_words = {'вра, ла': 'вра', 'кро, во, то, чить': 'чить',
                 'во, до, про, вод': 'вод', 'пар, тер': 'тер',
                 'а, э, ро, пор, ты': 'пор', 'бан, ты': 'бан',
                 'бо, ро, ду': 'бо', 'бух, гал, те, ров': 'гал',
                 'граж, дан, ство': 'дан', 'де, фис': 'фис',
                 'де, ше, виз, на': 'виз', 'дис, пан, сер': 'сер',
                 'до, го, во, рён, ность': 'рён', 'до, ку, мент': 'мент',
                 'до, суг': 'суг', 'е, ре, тик': 'тик',
                 'жа, лю, зи': 'зи', 'зна, чи, мость': 'зна',
                 'ик, сы': 'ик', 'ка, та, лог': 'ка',
                 'мо, но, лог': 'лог', 'квар, тал': 'тал',
                 'ки, ло, метр': 'метр', 'ко, ну, сы': 'ко',
                 'ко, рысть': 'ко', 'кра, ны': 'кра',
                 'кре, мень': 'мень', 'лек, то, ры': 'лек',
                 'лыж, ня': 'ня', 'мест, нос, тей': 'мест',
                 'му, со, ро, про, вод': 'вод', 'на, ме, ре, ни, е': 'мер',
                 'на, рост': 'рост', 'не, друг': 'не',
                 'не, дуг': 'не', 'не, кро, лог': 'лог',
                 'не, на, висть': 'не', 'от, ро, чес, тво': 'от',
                 'све, кла': 'све', 'сред, ства': 'сред',
                 'сто, ляр': 'ляр', 'до, яр': 'яр',
                 'тор, ты': 'тор', 'цент, нер': 'цент',
                 'це, поч, ка': 'поч', 'шар, фы': 'шар',
                 'экс, перт': 'перт', 'вер, на': 'на',
                 'зна, чи, мый': 'зна', 'кра, си, ве, е': 'си',
                 'кра, си, вей, ший': 'си', 'лов, ка': 'ка',
                 'бра, ла': 'ла', 'взя, ла': 'ла',
                 'вли, лась': 'лась', 'вор, вать, ся': 'вать',
                 'вос, при, ня, ла': 'ла', 'вос, соз, да, ла': 'ла',
                 'вру, чит': 'чит', 'гна, ла': 'ла',
                 'до, бра, ла': 'ла', 'до, жда, лась': 'лась',
                 'до, зво, нит, ся': 'нит', 'до, зи, ро, вать': 'зи',
                 'жи, лось': 'лос', 'за, ку, по, рить': 'ку',
                 'за, ня, ла': 'ла', 'за, пе, реть': 'реть',
                 'ис, чер, пать': 'чер', 'кла, ла': 'кла',
                 'кра, лась': 'кра', 'лга, ла': 'ла',
                 'ли, ла': 'ла', 'на, вра, ла': 'ла',
                 'на, де, лит': 'лит', 'на, дор, ва, лась': 'лась',
                 'на, зва, лась': 'лась', 'на, кре, нит, ся': 'нит',
                 'на, со, рит': 'рит', 'об, лег, чит': 'чит',
                 'об, ли, лась': 'лась', 'ма, за, ич, ный': 'ич',
                 'от, то, вый': 'то', 'про, зор, ли, ва': 'ли',
                 'сли, во, вый': 'сли', 'об, ня, лась': 'лась',
                 'о, бо, гна, ла': 'ла', 'о, бо, дра, ла': 'ла',
                 'о, бо, дрить': 'дрить', 'о, бо, стрить': 'стрить',
                 'о, дол, жит': 'жит', 'о, зло, бить': 'зло',
                 'о, кле, ить': 'кле', 'о, кру, жит': 'жит',
                 'о, плом, би, ро, вать': 'вать', 'о, по, шлить': 'по',
                 'о, све, до, ми, ться': 'све', 'от, быть': 'быть',
                 'от, ку, по, рить': 'ку', 'о, то, зва, ла': 'ла',
                 'пло, до, но, сить': 'сить', 'по, вто, рит': 'рит',
                 'по, ня, ла': 'ла', 'по, сла, ла': 'сла',
                 'при, ну, дить': 'ну', 'рва, ла': 'ла',
                 'свер, лить': 'лить', 'сня, ла': 'ла',
                 'соз, да, ла': 'ла', 'сор, ва, ла': 'ла',
                 'со, рит': 'рит', 'у, бы, стрить': 'стрить',
                 'у, глу, бить': 'бить', 'чер, пать': 'чер',
                 'ще, мить': 'мить', 'ба, ло, ван, ный': 'ло',
                 'за, гну, тый': 'за', 'за, ня, тый': 'за',
                 'за, ня, та': 'та', 'за, се, лен, ный': 'лен',
                 'за, се, ле, на': 'на', 'из, ба, ло, ван, ный': 'ло',
                 'кор, мя, щий': 'мя', 'кро, во, то, ча, щий': 'ча',
                 'мо, ля, щий': 'ля', 'на, няв, ший, ся': 'няв',
                 'на, чав, ший': 'чав', 'ба, лу, ясь': 'лу',
                 'за, ку, по, рив': 'ку', 'на, чав': 'чав',
                 'от, дав': 'дав', 'во, вре, мя': 'во',
                 'до, вер, ху': 'до', 'до, нель, зя': 'нель',
                 'до, ни, зу': 'до', 'до, су, ха': 'до',
                 'за, вид, но': 'вид', 'на, ча, тый': 'на',
                 'на, ча, та': 'та', 'по, няв, ший': 'няв',
                 'при, ня, тый': 'ня', 'про, жив, ший': 'жив',
                 'со, гну, тый': 'гну', 'по, няв': 'няв',
                 'при, быв': 'быв', 'соз, дав': 'дав',
                 'за, го, дя': 'за', 'за, свет, ло': 'за',
                 'на, дол, го': 'дол'}
list_of_words = list(dict_of_words.keys())
previous_word = ''
previous_value = ''

praise_words = ['молодец', 'Отлично', 'правильно', 'круто', 'замечательно']
dissaproval_words = ['Ошибочка', 'Неправильно', 'Неверно', 'Увы']


@app.route('/', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Response: %r', response)
    return json.dumps(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']
    if req['session']['new']:
        res['response']['text'] = 'Привет! Назови своё имя!'
        res['response']['tts'] = 'Привет!'
        sessionStorage[user_id] = {
            'first_name': None,
            'game_started': False
        }
        return

    if sessionStorage[user_id]['first_name'] is None:
        first_name = get_first_name(req)
        if first_name is None:
            res['response']['text'] = 'Не расслышала, повтори-ка!'
            res['response']['tts'] = 'Не расслышала, повтори-ка!'
        else:
            sessionStorage[user_id]['first_name'] = first_name
            sessionStorage[user_id]['guessed_words'] = []
            res['response']['text'] = f'Приятно познакомиться, {first_name.title()}. Я Алиса. Отгадаешь, куда падает ' \
                                      f'ударение?'
            res['response']['tts'] = f'Приятно познакомиться, {first_name.title()}. Я Алиса. Отгадаешь, куда падает ' \
                                     f'ударение?'
            res['response']['buttons'] = [
                {
                    'title': 'Да',
                    'hide': True
                },
                {
                    'title': 'Нет',
                    'hide': True
                }
            ]
            sessionStorage[user_id]['game_started'] = True
    else:
        if req['request']['command'] in ['Пока', 'хватит', 'стоп', 'удачи', 'до свидания']:
            res['response']['text'] = "До встречи!"
            res['response']['tts'] = "До встречи!"
            return
        if not sessionStorage[user_id]['game_started']:
            pass
        else:
            guess_word_stress(res, req)


def guess_word_stress(res, req):
    global list_of_words
    user_id = req['session']['user_id']
    word = random.choice(list_of_words)
    list_of_words.pop(list_of_words.index(word))

    value = req['request']['command']
    if value not in ['да', 'нет']:
        if value == dict_of_words[previous_word]:
            res['response']['text'] = '{}! А здесь? {}'.format(random.choice(praise_words),
                                                               ''.join(word.split(', ')))
            res['response']['tts'] = ' <speaker audio=\"alice-sounds-game-win-1.opus\"> {}! А здесь? {}'.format(random.choice(praise_words),
                                                               ''.join(word.split(', ')))
        else:
            res['response']['text'] = """{}, ударение падает
             на {}. Давай дальше. {}""".format(random.choice(dissaproval_words),
                                               dict_of_words[previous_word],
                                               ''.join(word.split(', ')))
            res['response']['tts'] = """{}, ударение падает
             на {}. Давай дальше. {}""".format(random.choice(dissaproval_words),
                                               dict_of_words[previous_word],
                                               ''.join(word.split(', ')))
    else:
        res['response']['text'] = ''.join(word.split(', '))
    res['response']['buttons'] = get_buttons(word, user_id)


def get_buttons(word, user_id):
    global previous_word
    session = sessionStorage[user_id]
    previous_word = word
    letters = [
        {'title': letter, 'hide': True}
        for letter in word.split(', ')
    ]

    session['suggests'] = letters
    sessionStorage[user_id] = session

    return letters


def get_first_name(req):
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.FIO':
            return entity['value'].get('first_name', None)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
