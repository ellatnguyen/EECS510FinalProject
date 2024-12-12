import re

class Automaton:
    def __init__(self, states, input_symbols, start_state, accept_states, transitions):
        self.states = states
        self.input_symbols = input_symbols
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions

    def accept(self, w):
        current_state = self.start_state
        path = []

        for symbol in w:
            if symbol not in self.input_symbols:
                return "reject"  # Invalid symbol

            transition_found = False
            for (src, input_symbol, dest) in self.transitions:
                if src == current_state and input_symbol == symbol:
                    path.append((current_state, symbol, dest))
                    current_state = dest
                    transition_found = True
                    break

            if not transition_found:
                return f"reject'"  # No valid transition

        if current_state in self.accept_states:
            return "accept", path
        else:
            return "reject"


def read_automaton(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    states = lines[0].strip().split()
    input_symbols = lines[1].strip().split()
    start_state = lines[2].strip()
    accept_states = lines[3].strip().split()

    transitions = []
    for line in lines[4:]:
        parts = line.strip().split()
        transitions.append((parts[0], parts[1], parts[2]))

    return Automaton(states, input_symbols, start_state, accept_states, transitions)


def validate_pokemon_battle_string(w):
    # Updated regex for matching substrings
    battle_regex = re.compile(r'(P[A-Za-z]+(M[A-Za-z]+P[A-Za-z]+|Switch+P[A-Za-z]+|Item+D[A-Za-z]+))')
    matches = battle_regex.findall(w)

    if not matches or len(matches) > 3:
        return "reject"

    return "accept", [match[0] for match in matches]


def preprocess_test_string(valid_substrings):
    symbols = []
    for substring in valid_substrings:
        battle_regex = re.compile(r'(P[A-Za-z]+)(M[A-Za-z]+P[A-Za-z]+|Switch+P[A-Za-z]+|Item+D[A-Za-z]+)')
        match = battle_regex.match(substring)
        if match:
            symbols.append('P')
            action_target = match.group(2)
            if action_target.startswith('M'):
                symbols.append('M')
                symbols.append('P')
            elif action_target.startswith('S'):
                symbols.append('S')
                symbols.append('P')
            elif action_target.startswith('I'):
                symbols.append('I')
                symbols.append('D')
    return symbols


def test_automaton(file_path, test_string):
    automaton = read_automaton(file_path)

    # Validate substrings from the input
    validation_result = validate_pokemon_battle_string(test_string)
    if validation_result[0].startswith("reject"):
        print(validation_result[0])
        return

    valid_substrings = validation_result[1]

    # Preprocess valid substrings into symbols
    all_symbols = preprocess_test_string(valid_substrings)

    # Test symbols against the automaton
    result = automaton.accept(all_symbols)
    if isinstance(result, str) and result.startswith("reject"):
        print(result)
    else:
        print("accept")
        for step in result[1]:
            print(step[0], step[1], step[2])


# Test Cases (please view testcases.txt for further examples/explanation)
print("=== ACCEPTED TEST CASES ===")
test_automaton("automaton.txt", "PPikachuSwitchPCharizard") # Switching Pokemon
print()
test_automaton("automaton.txt", "PSquirtleMBubblePPikachu") # Pokemon Move
print()
test_automaton("automaton.txt", "PBulbasaurItemDPotion") # Using Items
print()
test_automaton("automaton.txt", "PPikachuSwitchPCharizard PSquirtleMBubblePPikachu") # Double Battle
print()
test_automaton("automaton.txt", "PPikachuSwitchPCharizard PSquirtleMBubblePPikachu PBulbasaurItemDPotion") # Triple Battle

print("=== REJECTED TEST CASES ===")
test_automaton("automaton.txt", "SquirtleBubblePikachu") # No Notation
print()
test_automaton("automaton.txt", "MThunderboltPSquirtle") # No Acting Pokemon
print()
test_automaton("automaton.txt", "PPikachuMThunderbolt") # No Target Pokemon
print()
test_automaton("automaton.txt", "") # No Input
print()
test_automaton("automaton.txt", "PPikachuSwitchPCharizard PSquirtleMBubblePPikachu, PBulbasaurItemDPotion PCharizardSwitchPidgeot") # Not Single/Double/Triple Battle
