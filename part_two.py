import math
from collections import defaultdict, Counter

def e_prob(file):
    frequencies = defaultdict(Counter)

    with open(file, "r") as f:
        for line in f:
            correct, typed = line.strip().lower().split(":")
            for correct_letter, typed_letter in zip(correct, typed):
                frequencies[correct_letter][typed_letter] += 1

    e_probs = {}
    for correct_letter, counter in frequencies.items():
        total = sum(counter.values())
        e_probs[correct_letter] = {
            typed_letter: count / total for typed_letter, count in counter.items()
        }

    return e_probs


def t_probs(file):
    frequencies = defaultdict(Counter)

    with open(file, "r") as f:
        for line in f:
            correct_word, throw = line.strip().lower().split(":")
            letters = ["start"] + list(correct_word) + ["end"]
            for i in range(len(letters) - 1):
                frequencies[letters[i]][letters[i+1]] += 1

    t_probs = {}
    for prev_letter, counter in frequencies.items():
        total = sum(counter.values())
        t_probs[prev_letter] = {
            next_letter: count / total for next_letter, count in counter.items()
        }

    return t_probs


def viterbi_correction(user_input, e_probs, t_probs):
    states = list(e_probs.keys())
    V = [{}]
    backpointer = [{}]

    for s in states:
        V[0][s] = math.log(t_probs.get('start', {}).get(s, 1e-10)) \
                   + math.log(e_probs.get(s, {}).get(user_input[0], 1e-10))
        backpointer[0][s] = None

    # Recursion
    for t in range(1, len(user_input)):
        V.append({})
        backpointer.append({})
        for s in states:
            max_prob, prev_state = max(
                (
                    V[t-1][s_prev] +
                    math.log(t_probs.get(s_prev, {}).get(s, 1e-10)) +
                    math.log(e_probs.get(s, {}).get(user_input[t], 1e-10)),
                    s_prev
                )
                for s_prev in states
            )
            V[t][s] = max_prob
            backpointer[t][s] = prev_state

    final_state, final_prob = max(
        (
            s,
            V[-1][s] + math.log(t_probs.get(s, {}).get('end', 1e-10))
        )
        for s in states
    )

    best_path = [final_state]
    for t in range(len(user_input)-1, 0, -1):
        best_path.insert(0, backpointer[t][best_path[0]])

    return ''.join(best_path)



if __name__ == "__main__":
    emission_probs = e_prob("aspell.txt")
    transition_probs = t_probs("aspell.txt")

    text = input("Enter text: ").strip().lower()
    words = text.split()

    for word in words:
        corrected = viterbi_correction(word, emission_probs, transition_probs)
        print(corrected, end=" ")
