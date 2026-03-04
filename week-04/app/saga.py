
# Реализуйте здесь простую машину состояний (State Machine).
# Функция должна принимать текущее состояние и событие,
# и возвращать следующее состояние.

def next_state(state: str, event: str) -> str:
    if state == 'NEW' and event == 'PAY_OK':
        return 'PAID'
    if state == 'NEW' and event == 'PAY_FAIL':
        return 'CANCELLED'
    return state