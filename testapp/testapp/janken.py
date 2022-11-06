from flask import Blueprint, render_template, request
from random import randint

# じゃんけんモジュールを作成
janken_module = Blueprint("janken", __name__)

# じゃんけん選択画面
@janken_module.get('/sampleform')
def sample_form():
    return render_template('sampleform.html')

# じゃんけん表示画面
@janken_module.post('/sampleform')
def janken_result():
    # ジャンケンの手を文字列の数字0~2で受け取る
    hands = {
        '0': 'グー',
        '1': 'チョキ',
        '2': 'パー',
    }
    janken_mapping = {
        'draw': '引き分け',
        'win': '勝ち',
        'lose': '負け',
    }

    player_hand_ja = hands[request.form['janken']]  # 日本語表示用
    player_hand = int(request.form['janken'])  # str型→数値に変換必要
    enemy_hand = randint(0, 2)  # 相手は0~2の乱数
    enemy_hand_ja = hands[str(enemy_hand)]  # 日本語表示用
    if player_hand == enemy_hand:
        judgement = 'draw'
    elif (player_hand == 0 and enemy_hand == 1) or (player_hand == 1 and enemy_hand == 2) or (player_hand == 2 and enemy_hand == 0):
        judgement = 'win'
    else:
        judgement = 'lose'
    result = {
            'enemy_hand_ja': enemy_hand_ja,
            'player_hand_ja': player_hand_ja,
            'judgement': janken_mapping[judgement],
    }
    return render_template('janken_result.html', result=result)
