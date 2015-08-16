import itertools
import sys


EMPTY = ''


def print_board(board):
    """
    Pretty-prints the board.

    Example output:

         1     [b]   [b]   [b]   [b]    Red: 12
         5  [b]   [b]   [b]   [b]       Black: 12
         9     [b]   [b]   [b]   [b]
        13  [ ]   [ ]   [ ]   [ ]
        17     [ ]   [ ]   [ ]   [ ]
        21  [r]   [r]   [r]   [r]
        25     [r]   [r]   [r]   [r]
        29  [r]   [r]   [r]   [r]
    """
    blank = ' ' * 3
    odd_row = False
    r_score = red_score(board)
    b_score = black_score(board)
    for i, space in enumerate(board):
        if not i % 4:
            row_label = '{}  '.format(i + 1)
            if len(str(i + 1)) == 1:
                row_label = ' ' + row_label
            sys.stdout.write(row_label)
        space = '[{}]'.format(space or ' ')
        args = (space, blank) if odd_row else (blank, space)
        sys.stdout.write('{}{}'.format(*args))
        if (i + 1) % 4 == 0:
            odd_row = not odd_row
            if i < 4:  # write red score
                sys.stdout.write('    Red:   {}'.format(r_score))
            elif i < 8:  # write black score
                sys.stdout.write('    Black: {}'.format(b_score))
            sys.stdout.write('\n')


def red_score(board):
    return sum(1 for s in board if s == 'r')


def black_score(board):
    return sum(1 for s in board if s == 'b')


def all_black_moves():
    for i in xrange(1, 33):
        # Edges only have one move
        if i in (4, 5, 12, 13, 20, 21, 28):
            yield i, i + 4
        # Left-shifted squares move +4 and +5
        elif i in (1, 2, 3, 9, 10, 11, 17, 18, 19, 25, 26, 27):
            yield i, i + 4
            yield i, i + 5
        # Right-shifted squares move +3 and +4
        elif i in (6, 7, 8, 14, 15, 16, 22, 23, 24):
            yield i, i + 3
            yield i, i + 4


def all_red_moves():
    """
    Generates the reverse of all black moves
    """
    for i, j in all_black_moves():
        yield j, i


def all_king_moves():
    """
    A king can move in any direction.
    """
    for m in all_black_moves():
        yield m
    for m in all_red_moves():
        yield m


def possible_black_moves(board, position):
    """
    Given a board, generate possible black moves
    """
    if position:
        for i, j in black_captures_from_pos(board, position):
            yield i, j
    for i, j in all_black_moves():
        if board[i - 1] == 'b' and not board[j - 1]:
            yield i, j


def possible_red_moves(board, position):
    """
    Given a board, generate possible red moves
    """
    if position:
        for i, j in red_captures_from_pos(board, position):
            yield i, j
    for i, j in all_red_moves():
        if board[i - 1] == 'r' and not board[j - 1]:
            yield i, j


def is_red_move(from_, to):
    return (from_, to) in all_red_moves()


def is_black_move(from_, to):
    return (from_, to) in all_black_moves()


def red_captures_from_pos(board, pos):
    """
    Generates all valid jump moves from the given position of a red
    player.
    """
    idx = pos - 1
    if position_in_odd_row(pos):
        # -4 then -5
        if (board[idx - 4].lower() == 'b' and board[idx - 9] == EMPTY and
                is_red_move(pos - 4, pos - 9)):
            yield pos, pos - 9
        # -3 and -7
        if (board[idx - 3].lower() == 'b' and board[idx - 7] == EMPTY and
                is_red_move(pos - 3, pos - 7)):
            yield pos, pos - 7
    else:
        # -5 and -9
        if (board[idx - 5].lower() == 'b' and board[idx - 9] == EMPTY and
                is_red_move(pos - 5, pos - 9)):
            yield pos, pos - 9
        # -4 and -7
        if (board[idx - 4].lower() == 'b' and board[idx - 7] == EMPTY and
                is_red_move(pos - 4, pos - 7)):
            yield pos, pos - 7


def black_captures_from_pos(board, pos):
    """
    Generates all valid jump moves from the given position of a black
    player.
    """
    idx = pos - 1
    if position_in_odd_row(pos):
        # +4 then +7
        if (board[idx + 4].lower() == 'r' and board[idx + 7] == EMPTY and
                is_black_move(pos + 4, pos + 7)):
            yield pos, pos + 7
        # +5 then +9
        if (board[idx + 5].lower() == 'r' and board[idx + 9] == EMPTY and
                is_black_move(pos + 5, pos + 9)):
            yield pos, pos + 9
    else:
        # +3 then +7
        if (board[idx + 3].lower() == 'r' and board[idx + 7] == EMPTY and
                is_black_move(pos + 3, pos + 7)):
            yield pos, pos + 7
        # +4 then +9
        if (board[idx + 4].lower() == 'r' and board[idx + 9] == EMPTY and
                is_black_move(pos + 4, pos + 9)):
            yield pos, pos + 9


def position_in_odd_row(position):
    if position % 4 == 0:
        return bool((position // 4) % 2)

    return bool(((position + 4 - (position % 4)) // 4) % 2)


def turns():
    turn = 'r'
    while True:
        yield turn
        turn = 'b' if turn == 'r' else 'r'


def is_jump(move):
    return distance(move) > 5


def distance(move):
    from_, to = move
    return abs(to - from_)


def direction(move):
    """
    Returns -1 if moving backward or 1 if moving forward
    """
    from_, to = move
    return -1 if from_ > to else 1


def is_backward(move):
    return direction(move) == -1


def is_forward(move):
    return not is_backward(move)


def jumped_space_relative(move):
    assert is_jump(move)

    jump = distance(move) // 2
    odd_row = position_in_odd_row(move[0])
    even_row = not odd_row
    backward = is_backward(move)
    forward = not backward

    if odd_row and forward or even_row and backward:
        jump += 1

    return jump * direction(move)


def next_board(board, move):
    """
    Returns a new board from the old board with the given move applied
    to it
    """
    from_, to = move
    jump = None

    if is_jump(move):  # jump move
        assert distance(move) in (7, 9), 'How can jump distance not be 7 or 9?'
        jump = jumped_space_relative(move)

    nextb = board[:]
    nextb[to-1], nextb[from_-1] = nextb[from_-1], EMPTY

    if jump:
        set_to_empty = from_ - 1 + jump
        nextb[set_to_empty] = EMPTY

    return nextb


# TESTS

def test_red_captures():
    board = ['b', 'b', 'b', 'b',
             'b', 'b', 'b', 'b',
             EMPTY, EMPTY, 'b', EMPTY,
             EMPTY, EMPTY, EMPTY, EMPTY,
             'b', 'b', EMPTY, 'b',
             'r', 'r', 'r', 'r',
             'r', 'r', 'r', 'r',
             'r', 'r', 'r', 'r']

    assert len(board) == 32, "Board isn't the right size"
    assert set(red_captures_from_pos(board, 21)) == set([(21, 14)])
    assert set(red_captures_from_pos(board, 22)) == set([(22, 13), (22, 15)])
    assert set(red_captures_from_pos(board, 24)) == set()


def test_red_capture_21_14():
    board = ['b', 'b', 'b', 'b',
             'b', 'b', EMPTY, 'b',
             EMPTY, 'b', 'b', 'b',
             'b', EMPTY, EMPTY, EMPTY,
             'b', EMPTY, EMPTY, EMPTY,
             'r', 'r', 'r', 'r',
             EMPTY, 'r', 'r', 'r',
             'r', 'r', 'r', 'r']
    expected = ['b', 'b', 'b', 'b',
                'b', 'b', EMPTY, 'b',
                EMPTY, 'b', 'b', 'b',
                'b', 'r', EMPTY, EMPTY,
                EMPTY, EMPTY, EMPTY, EMPTY,
                EMPTY, 'r', 'r', 'r',
                EMPTY, 'r', 'r', 'r',
                'r', 'r', 'r', 'r']
    move = (21, 14)
    actual = next_board(board, move)

    assert len(board) == 32, "Board isn't the right size"
    assert len(expected) == 32, "Board isn't the right size"
    assert expected == actual


def test_black_captures():
    board = ['b', 'b', 'b', 'b',
             'b', 'b', 'b', 'b',
             'b', 'b', EMPTY, 'b',
             'r', EMPTY, 'b', 'r',
             EMPTY, 'r', EMPTY, EMPTY,
             EMPTY, EMPTY, EMPTY, 'r',
             'r', 'r', 'r', 'r',
             'r', 'r', 'r', 'r']

    assert len(board) == 32, "Board isn't the right size"
    assert set(black_captures_from_pos(board, 9)) == set()
    assert set(black_captures_from_pos(board, 15)) == set([(15, 22)]), \
        str(set(black_captures_from_pos(board, 15)))
    assert set(black_captures_from_pos(board, 12)) == set([(12, 19)]), \
        str(set(black_captures_from_pos(board, 12)))


def test_odd_row_detector():
    assert position_in_odd_row(12) is True
    assert position_in_odd_row(15) is False
    assert position_in_odd_row(18) is True


def test_turn_generator():
    t = turns()
    first_five_turns = [t.next(), t.next(), t.next(), t.next(), t.next()]
    assert first_five_turns == ['r', 'b', 'r', 'b', 'r']


def test_possible_move_generators():
    board = ['b'] * 12 + [EMPTY] * 8 + ['r'] * 12
    assert len(board) == 32, "Board isn't the right size"

    assert set(possible_black_moves(board, None)) == set(
        [(9, 13), (9, 14), (10, 14), (10, 15), (11, 15), (11, 16), (12, 16)])

    assert set(possible_red_moves(board, None)) == set(
        [(21, 17), (22, 17), (22, 18), (23, 18), (23, 19), (24, 19), (24, 20)])


def test_all_king_moves():
    assert list(all_king_moves()) == [
        (1, 5), (1, 6), (2, 6), (2, 7), (3, 7), (3, 8), (4, 8), (5, 9), (6, 9),
        (6, 10), (7, 10), (7, 11), (8, 11), (8, 12), (9, 13), (9, 14),
        (10, 14), (10, 15), (11, 15), (11, 16), (12, 16), (13, 17), (14, 17),
        (14, 18), (15, 18), (15, 19), (16, 19), (16, 20), (17, 21), (17, 22),
        (18, 22), (18, 23), (19, 23), (19, 24), (20, 24), (21, 25), (22, 25),
        (22, 26), (23, 26), (23, 27), (24, 27), (24, 28), (25, 29), (25, 30),
        (26, 30), (26, 31), (27, 31), (27, 32), (28, 32), (5, 1), (6, 1),
        (6, 2), (7, 2), (7, 3), (8, 3), (8, 4), (9, 5), (9, 6), (10, 6),
        (10, 7), (11, 7), (11, 8), (12, 8), (13, 9), (14, 9), (14, 10),
        (15, 10), (15, 11), (16, 11), (16, 12), (17, 13), (17, 14), (18, 14),
        (18, 15), (19, 15), (19, 16), (20, 16), (21, 17), (22, 17), (22, 18),
        (23, 18), (23, 19), (24, 19), (24, 20), (25, 21), (25, 22), (26, 22),
        (26, 23), (27, 23), (27, 24), (28, 24), (29, 25), (30, 25), (30, 26),
        (31, 26), (31, 27), (32, 27), (32, 28)]


def test_all_red_moves():
    assert list(all_red_moves()) == [
        (5, 1), (6, 1), (6, 2), (7, 2), (7, 3), (8, 3), (8, 4), (9, 5), (9, 6),
        (10, 6), (10, 7), (11, 7), (11, 8), (12, 8), (13, 9), (14, 9),
        (14, 10), (15, 10), (15, 11), (16, 11), (16, 12), (17, 13), (17, 14),
        (18, 14), (18, 15), (19, 15), (19, 16), (20, 16), (21, 17), (22, 17),
        (22, 18), (23, 18), (23, 19), (24, 19), (24, 20), (25, 21), (25, 22),
        (26, 22), (26, 23), (27, 23), (27, 24), (28, 24), (29, 25), (30, 25),
        (30, 26), (31, 26), (31, 27), (32, 27), (32, 28)]


def test_all_black_moves():
    assert list(all_black_moves()) == [
        (1, 5), (1, 6), (2, 6), (2, 7), (3, 7), (3, 8), (4, 8), (5, 9), (6, 9),
        (6, 10), (7, 10), (7, 11), (8, 11), (8, 12), (9, 13), (9, 14),
        (10, 14), (10, 15), (11, 15), (11, 16), (12, 16), (13, 17), (14, 17),
        (14, 18), (15, 18), (15, 19), (16, 19), (16, 20), (17, 21), (17, 22),
        (18, 22), (18, 23), (19, 23), (19, 24), (20, 24), (21, 25), (22, 25),
        (22, 26), (23, 26), (23, 27), (24, 27), (24, 28), (25, 29), (25, 30),
        (26, 30), (26, 31), (27, 31), (27, 32), (28, 32)]


def test_next_board_A():
    board = ['b', 'b', 'b', 'b',
             'b', 'b', 'b', 'b',
             EMPTY, 'b', 'b', 'b',
             EMPTY, 'b', EMPTY, EMPTY,
             EMPTY, 'r', EMPTY, EMPTY,
             'r', 'r', EMPTY, 'r',
             'r', 'r', 'r', 'r',
             'r', 'r', 'r', 'r']
    expected = ['b', 'b', 'b', 'b',
                'b', 'b', 'b', 'b',
                'r', 'b', 'b', 'b',
                EMPTY, EMPTY, EMPTY, EMPTY,
                EMPTY, EMPTY, EMPTY, EMPTY,
                'r', 'r', EMPTY, 'r',
                'r', 'r', 'r', 'r',
                'r', 'r', 'r', 'r']
    result = next_board(board, (18, 9))
    for i, (a, b) in enumerate(itertools.izip(expected, result)):
        if a != b:
            print("failure at position {}: expected {}, got {}"
                  .format(i, repr(a), repr(b)))
    assert result == expected, "Next board isn't what we expected"


def test_next_board_B():
    board = ['b', 'b', 'b', 'b',
             'b', 'b', 'b', 'b',
             EMPTY, 'b', 'b', 'b',
             EMPTY, 'b', EMPTY, EMPTY,
             EMPTY, 'r', EMPTY, EMPTY,
             'r', 'r', EMPTY, 'r',
             'r', 'r', 'r', 'r',
             'r', 'r', 'r', 'r']
    expected = ['b', 'b', 'b', 'b',
                'b', 'b', 'b', 'b',
                EMPTY, 'b', 'b', 'b',
                EMPTY, EMPTY, EMPTY, EMPTY,
                EMPTY, EMPTY, EMPTY, EMPTY,
                'r', 'r', 'b', 'r',
                'r', 'r', 'r', 'r',
                'r', 'r', 'r', 'r']
    result = next_board(board, (14, 23))
    for i, (a, b) in enumerate(itertools.izip(expected, result)):
        if a != b:
            print("failure at position {}: expected {}, got {}"
                  .format(i, repr(a), repr(b)))
    assert result == expected, "Next board isn't what we expected"


def test():
    test_all_black_moves()
    test_all_red_moves()
    test_all_king_moves()
    test_possible_move_generators()
    test_turn_generator()
    test_odd_row_detector()
    test_red_captures()
    test_red_capture_21_14()
    test_black_captures()
    test_next_board_A()
    test_next_board_B()


def get_turn_fns(turn):
    if turn == 'r':
        return possible_red_moves, all_red_moves
    elif turn == 'b':
        return possible_black_moves, all_black_moves
    else:
        raise Exception('What kind of turn is this? {}'.format(repr(turn)))


def get_prompt(turn):
    if turn == 'r':
        return 'Red move: '
    elif turn == 'b':
        return 'Black move: '
    else:
        raise Exception('What kind of turn is this? {}'.format(repr(turn)))


def main():
    board = ['b'] * 12 + [EMPTY] * 8 + ['r'] * 12
    try:
        for t in turns():
            while True:
                print_board(board)
                print('')
                prompt = get_prompt(t)
                move_str = raw_input(prompt)
                move_split = move_str.split('-')
                if len(move_split) != 2:
                    print('Invalid move format (format = FROM-TO)')
                    print('')
                    continue

                possible_moves, all_moves_ = get_turn_fns(t)
                from_, to = int(move_split[0]), int(move_split[1])
                if (from_, to) in possible_moves(board, from_):
                    board = next_board(board, (from_, to))
                    break
                else:
                    print('{} is an illegal move :('.format(move_str))

            print('')
    except KeyboardInterrupt:
        print("\nBye!\n")
        sys.exit(0)


if __name__ == '__main__':
    test()
    main()
