#Need in PDA:

#-Must be Nondetermenistic
#-Show stack
#-Show trasitions

class State:
    def __init__(self):
        self.f = False  # initially not a final state
        self.gamma = ['Z']  # stack with Z as the only element
        self.sigma = []  # array of symbols (optional)
        self.next = {}  # dictionary to store transitions

    def delta(self, symbol):
        next_states = []
        if symbol in self.next:
            for transition in self.next[symbol]:
                next_states.append(transition)
        return next_states

    def setTransition(self, input_symbol, pop_symbol, next_state, push_symbols):
        if input_symbol not in self.next:
            self.next[input_symbol] = []
        self.next[input_symbol].append({
            'pop': pop_symbol,
            'state': next_state,
            'push': push_symbols
        })

    def setFinal(self):
        self.f = True

    def getStackSymbol(self):
        return self.gamma[-1]

    def showStack(self, transition_symbol=None, popped_symbol=None, pushed_symbols=None):
        print("Stack:", end=" ")

        # Display stack content
        for symbol in reversed(self.gamma):
            print(symbol, end="")

        # Display additional information about the transition
        if transition_symbol is not None:
            print(f"  Transition: {transition_symbol}", end="")
            if popped_symbol is not None:
                print(f" (Popped: {popped_symbol})", end="")
            if pushed_symbols is not None:
                print(f" (Pushed: {''.join(reversed(pushed_symbols))})", end="")

        print(" (top)")

class PDA:
    def __init__(self):
        self.q = []  # array of Class State
        self.f = set()  # set of final Class State (optional)
        self.gamma = ['Z']  # a stack with Z as the only element

    def delta(self, input_string):
        try:
            if not self.q:
                raise ValueError("No start state defined.")
            
            current_state = self.q[0]  # Assuming there's a start state

            for symbol in input_string:
                next_states = current_state.delta(symbol)

                if not next_states:
                    return False  # No transition defined for the current symbol

                chosen_transition = next_states[0]
                next_state = chosen_transition['state']

                # Identifies if stack symbol
                epsilon_symbol = 'ε' if 'E' in chosen_transition['push'] else ''
                stack_symbol = '0' if current_state.getStackSymbol() == 'Z' else '1'

                # Prints the Transitions in the terminal
                transition_str = f"d(q{self.q.index(current_state)}, {symbol}, {stack_symbol}) "
                transition_str += f"= (q{self.q.index(next_state)}, {', '.join(chosen_transition['push'])}{epsilon_symbol})"
                print(transition_str)

                current_state.gamma.pop()  # Pop the top symbol
                current_state.gamma.extend(reversed(chosen_transition['push']))

                current_state.showStack(
                    transition_symbol=symbol,
                    popped_symbol=stack_symbol,
                    pushed_symbols=chosen_transition['push']
                )
                # Prints the stack
                print()
                current_state = next_state

            return current_state in self.f
            
        except ValueError as e:
            print(f"Error: {e}")
            return False

    def main(self, choice):
        pda = PDA()
        
        if choice == 1:
            Q0 = State()
            Q1 = State()
            Q2 = State()
            Q3 = State()

            Q0.setTransition('0', 'Z', Q1, ['X', 'Z'])
            Q1.setTransition('0', 'X', Q1, ['X', 'X'])
            Q1.setTransition('1', 'X', Q2, ['ε'])  # No push, just pop X
            Q2.setTransition('1', 'X', Q3, ['ε'])  # No push, just pop X

            Q3.setFinal()
            self.q = [Q0, Q1, Q2, Q3]
            for state in self.q:
                if state.f:
                    self.f.add(state)  # add final states to the set of final states
        
        elif choice == 2:
            Q0 = State()
            Q1 = State()
            Q2 = State()
            Q3 = State()

            # Define transitions
            Q0.setTransition('0', 'Z', Q1, ['X', 'Z'])
            Q1.setTransition('0', 'X', Q1, ['X', 'X'])
            Q1.setTransition('1', 'X', Q2, ['ε'])  # Transition to Q2 when '1' is encountered
            Q2.setTransition('1', 'X', Q2, ['ε'])
            Q2.setTransition('0', 'Z', Q3, ['ε'])  # Transition to Q4 when '0' is encountered

            Q3.setFinal()  # Set Q4 as a final state

            # Update PDA states and final states
            self.q = [Q0, Q1, Q2, Q3]
            self.f = {Q3}

        elif choice == 3:
            Q0 = State()
            Q1 = State()
            Q2 = State()

            Q0.setTransition('0', 'Z', Q0, ['0', 'Z'])
            Q0.setTransition('1', 'Z', Q0, ['1', 'Z'])
            Q0.setTransition('0', '1', Q0, ['0', '1'])
            Q0.setTransition('1', '0', Q0, ['1', '0'])
            Q0.setTransition('0', '0', Q1, ['ε'])
            Q0.setTransition('1', '1', Q1, ['ε'])
            Q1.setTransition('0', '0', Q1, ['ε'])
            Q1.setTransition('1', '1', Q1, ['ε'])
            Q1.setTransition('ε', 'Z', Q2, ['Z'])

            Q2.setFinal()   
            self.q = [Q0, Q1, Q2]
            for state in self.q:
                if state.f:
                    self.f.add(state) 
        else:
            print("What you inputted is not what we asked...")
            choice = int(input("Enter Choice Here: "))
            pda.main(choice)

    
# Example usage:
pda = PDA()

# Ask the user for input_string
print('''
  ____  ____    _    
 |  _ \|  _ \  / \   
 | |_) | | | |/ _ \  
 |  __/| |_| / ___ \ 
 |_|   |____/_/   \_\          
      ''')

choice = int(input('''
Please select which transitions your string wants to accept:
1.) 0^n 11
2.) 0^n 1^m 0
                   
where in: (n, m > 0)

Enter Choice Here: '''))

pda.main(choice)
input_string = input("Please enter the input string: ")
result = pda.delta(input_string)
print("String accepted:", result)
