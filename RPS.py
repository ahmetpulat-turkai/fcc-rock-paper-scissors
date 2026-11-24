# Identifies which bot is playing by replaying each bot's logic on our own move history,
# keeps the model that predicts the opponent best, and plays what beats its predicted move.
BEATS = {'P': 'S', 'R': 'P', 'S': 'R'}  # BEATS[x] is the move that beats x


def _quincy(mine):
    return ["R", "R", "P", "P", "S"][(len(mine) + 1) % 5]


def _kris(mine):
    return BEATS[mine[-1] if mine else 'R']


def _mrugesh(mine):
    last_ten = ([''] + mine)[-10:]
    most_frequent = max(set(last_ten), key=last_ten.count)
    if most_frequent == '':
        most_frequent = 'S'
    return BEATS[most_frequent]


def _abbey(mine):
    hist = ['R'] + mine
    counts = {a + b: 0 for a in 'RPS' for b in 'RPS'}
    for i in range(len(hist) - 1):
        counts[hist[i] + hist[i + 1]] += 1
    sub = {k: counts[k] for k in (hist[-1] + 'R', hist[-1] + 'P', hist[-1] + 'S')}
    return BEATS[max(sub, key=sub.get)[-1:]]


MODELS = [_quincy, _kris, _mrugesh, _abbey]


def player(prev_play, state={}):
    if prev_play == '':
        state.clear()
        state.update(mine=[], scores=[0.0] * len(MODELS), preds=None)
    mine, scores = state['mine'], state['scores']
    if state['preds'] is not None:
        for i, p in enumerate(state['preds']):
            scores[i] = scores[i] * 0.9 + (1 if p == prev_play else 0)
    preds = [m(mine) for m in MODELS]
    state['preds'] = preds
    best = max(range(len(MODELS)), key=lambda i: scores[i])
    move = BEATS[preds[best]]
    mine.append(move)
    return move
