import math
import re
from collections import OrderedDict


def get_right_side_of_negation(sentence, index):
    #used to apply De Morgan laws
    right = ''
    open_bracket_count = 0

    for x in range(index, len(sentence)):
        right += sentence[x]
        if sentence[x] == ')':
            open_bracket_count -= 1
            if open_bracket_count == 0:
                break

        elif sentence[x] == '(':
            open_bracket_count += 1

    return right


def get_side_of_sign(sentence, index, end_index, first_condition, second_condition, operator=1):
    side = sentence[index]
    index_counter = -1 if operator == -1 else 1

    for x in range(index + index_counter, end_index, operator):
        """
        get everything that belongs to the side of given sign
        if there is ')' next to the sign then we are searching until we reach '((' or till we get out of scope
        otherwise just get everything until first '('
        similarly if there is '(' next to sign
        """
        try:
            if side[0] == first_condition and sentence[x] == second_condition and sentence[
                x + operator] == second_condition:
                side += sentence[x]
                break

            elif side[0] != first_condition and sentence[x] == second_condition:
                break

            else:
                side += sentence[x]

        except IndexError:
            side += sentence[x]
            break

    return side


def no_bracket_needed(sentence):
    if sentence[0] == '(':
        i = 1

        for x in range(1, len(sentence)):
            if x == len(sentence) - 1:
                return True
            if sentence[x] == ')' and sentence[x + 1] != '|':
                i -= 1
            elif sentence[x] == '(':
                i += 1
            if i == 0:
                return False

    return False


def bracket_needed(sentence):
    bracket = False

    for char in sentence:
        if char.isalpha() and not bracket:
            return True
        elif char == '(':
            bracket = True
        elif char == ')':
            bracket = False

    return False


def delete_additional_brackets(sentence):
    patterns = ["~~\([a-z\|]+\)\|", "\|~~\([a-z\|]+\)", "\&~~\([a-z\&]+\)", "~~\([a-z\&]+\)\&"]

    for pattern in patterns:
        sentence_with_pattern = re.search(pattern, sentence)

        if sentence_with_pattern:
            new_sentence = sentence_with_pattern.group().replace('~~(', '')
            new_sentence = new_sentence.replace(')', '')
            sentence = sentence.replace(sentence_with_pattern.group(), new_sentence)

    return sentence


def biconditional_elimination(sentence):
    while sentence.find('<>') != -1:
        index = sentence.find('<>')
        left = get_side_of_sign(sentence, index - 1, -1, ')', '(', -1)[::-1]

        right = get_side_of_sign(sentence, index + 2, len(sentence), '(', ')')
        new_left = left
        new_right = right

        if f'({left}<>{right})' in sentence and not (
                f'|({left}<>{right})' in sentence or f'({left}<>{right})|' in sentence):
            left = '(' + left
            right += ')'

        sentence = sentence.replace(
            f'{left}<>{right}',
            f'({new_left}>>{new_right})&({new_right}>>{new_left})',
            1
        )

    return sentence


def implication_elimination(sentence):
    while sentence.find('>>') != -1:
        index = sentence.find('>>')
        left = get_side_of_sign(sentence, index - 1, -1, ')', '(', -1)[::-1]

        right = get_side_of_sign(sentence, index + 2, len(sentence), '(', ')')

        new_right = right
        new_left = left

        if '&' in right:
            if no_bracket_needed(new_right):
                pass
            else:
                new_right = f'({new_right})'

        if '&' in left or '|' in left:
            if no_bracket_needed(new_left):
                pass
            else:
                new_left = f'({new_left})'

        if f'|({left}>>{right})' in sentence or f'({left}>>{right})|' in sentence:
            left = '(' + left
            right += ')'

        sentence = sentence.replace(
            f'{left}>>{right}',
            f'~{new_left}|{new_right}',
            1
        )

    return sentence


def de_morgan_laws(sentence):
    sentence = sentence.replace('~~', '')

    while sentence.find('~(') != -1:
        right = get_right_side_of_negation(sentence, sentence.find('~('))
        new_right = list('(')
        i = 2

        while i != len(right):
            if right[i].isalpha():
                new_right.append(f'~{right[i]}')

            elif right[i] == '|':
                new_right.append('&')

            elif right[i] == '&':
                new_right.append('|')

            elif right[i] == '(':
                right_bracket = get_right_side_of_negation(right, i)

                new_right.append(f'~{right_bracket}')
                i += len(right_bracket)

                continue

            else:
                new_right.append(right[i])

            i += 1

        if right.count('(') > 1 and bracket_needed(right[2:]):
            pass
        elif '&' in right and (f'|{right}' in sentence or f'{right}|' in sentence):
            del new_right[0]
            del new_right[-1]

        new_right = delete_additional_brackets("".join(new_right))

        sentence = sentence.replace(
            f'{right}',
            new_right,
            1
        )

        sentence = sentence.replace('~~', '')

    return sentence


def nnf_to_dnf_transition(sentence):
    i = 0
    while i != len(sentence):
        try:
            if sentence[i] == '&' and (sentence[i + 1] == '(' or sentence[i - 1] == ')'):
                left = get_side_of_sign(sentence, i - 1, -1, ')', '(', -1)[::-1]
                right = get_side_of_sign(sentence, i + 1, len(sentence), '(', ')')
                new_right = nnf_to_dnf_transition(right)

                new_part = []

                if sentence[i + 1] == '(':
                    if len(new_right) == 1:
                        new_side = new_right
                    else:
                        new_side = new_right[1:len(new_right)].split('|')
                    side = 'right'
                else:
                    new_side, side = left[1:len(left) - 1].split('|'), 'left'

                for symbol in new_side:
                    new_part.append(f'({left}&{symbol})' if side == 'right' else f'({right}&{symbol})')

                new_part = '|'.join(new_part)

                if f'|({left}&{right}' in sentence or f'{left}&{right})|' in sentence:
                    new_part = new_part[1:len(new_part) - 1]

                sentence = sentence.replace(f'{left}&{right}', new_part, 1)

                i = 0
        except:
            pass
        i += 1

    while sentence.find('((') != -1 or sentence.find('))') != -1:
        sentence = sentence.replace('((', '(')
        sentence = sentence.replace('))', ')')

    return delete_duplicates(sentence, True)


def delete_duplicates(sentence, dnf=False):
    def create_new_part(part_to_be_checked, sentence, sign):
        new_part = OrderedDict.fromkeys(part_to_be_checked[1:len(part_to_be_checked) - 1].split(f'{sign}'))

        if len(new_part) == 1:
            new_part = ''.join(new_part)
            if '&' in new_part and (f'{part_to_be_checked}&' in sentence or f'&{part_to_be_checked}' in sentence):
                new_part = new_part[1:len(new_part) - 1]
            elif '|' in new_part and (f'{part_to_be_checked}|' in sentence or f'|{part_to_be_checked}' in sentence):
                new_part = new_part[1:len(new_part) - 1]
            return new_part

        else:
            return '(' + f'{sign}'.join(new_part) + ')'

    def get_main_brackets(sentence, index, x=0):
        bracket = []
        while x < index:
            if sentence[x] == '~':
                bracket.append(f'{sentence[x]}{sentence[x + 1]}')
                x += 2
            else:
                bracket.append(sentence[x])
                x += 1

        return bracket

    def delete_dnf_duplicates(sentence):
        sentence = [element for element in sentence.split('|')]
        new_sentence = [[] for element in sentence]

        k = 0
        for element in sentence:
            index = 0
            while index < len(element):
                if element[index] == '~':
                    new_sentence[k].append(element[index] + element[index + 1])
                    index += 2
                else:
                    new_sentence[k].append(element[index])
                    index += 1
            k += 1

        new_sentence = [sorted(element) for element in new_sentence]
        duplicate_index = []

        index = 0
        while index < len(new_sentence) - 1:
            j = index + 1
            while j < len(new_sentence):
                if new_sentence[index] == new_sentence[j]:
                    duplicate_index.append(j)
                j += 1
            index += 1

        index = 0
        new_sentence = []
        while index < len(sentence):
            if index not in duplicate_index:
                new_sentence.append(sentence[index])
            index += 1

        return '|'.join(new_sentence)

    i = 0

    while i < len(sentence):
        if sentence[i] == '(':
            part_to_be_checked = get_right_side_of_negation(sentence, i)
            if ')|(' in part_to_be_checked:
                new_part = create_new_part(part_to_be_checked, sentence, '|')
            elif ')&(' in part_to_be_checked:
                new_part = create_new_part(part_to_be_checked, sentence, '&')
            elif '|' in part_to_be_checked:
                new_part = create_new_part(part_to_be_checked, sentence, '|')
            elif '&' in part_to_be_checked:
                new_part = create_new_part(part_to_be_checked, sentence, '&')

            sentence = sentence.replace(part_to_be_checked, new_part, 1)

        i += 1

    i = math.floor(len(sentence) / 2)

    if sentence[i] == '&' and sentence[i - 1] == ')' and sentence[i + 1] == '(':
        left, right = get_main_brackets(sentence, i), get_main_brackets(sentence, len(sentence), i + 1)

        if sorted(left) == sorted(right):
            sentence = sentence[1:i - 1]

    return sentence if dnf == False else delete_dnf_duplicates(sentence)


def check_satisfiability(sentence):
    sentence = [variable[1:-1].split('&') for variable in sentence.split('|')]
    counter = 0

    for conjunction in sentence:
        for variable in conjunction:
            if f'~{variable}' in conjunction:
                counter += 1
                break

    if counter == len(sentence):
        return True
    else:
        return False


def main():
    while True:
        sentence = input()
        if sentence.lower() == 'stop':
            break
        sentence = biconditional_elimination(sentence)
        sentence = implication_elimination(sentence)
        sentence = de_morgan_laws(sentence)
        sentence = delete_duplicates(sentence)
        sentence = nnf_to_dnf_transition(sentence)
        print('Disjunctive normal form: ' + sentence)
        if check_satisfiability(sentence):
            print('Given formula is not satisfiable, because all its elementary component contain a pair of opposite '
                  'literals')
        else:
            print('Given formula is satisfiable')


if __name__ == '__main__':
    main()
