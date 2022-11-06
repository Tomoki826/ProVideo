from flask import Blueprint, render_template, request
from random import randint

janken_module = Blueprint("janken", __name__)

@janken_module.route('/gameresult', methods=['POST'])
def game_result():
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
    print(f'じゃんけん開始: enemy_hand: {enemy_hand}, player_hand: {player_hand}, judgement: {judgement}')
    return f'相手： {enemy_hand_ja}, あなた: {player_hand_ja}, 判定：{janken_mapping[judgement]}'
