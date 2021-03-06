from DVFApy.state import State
from DVFApy.boolean_operator_construct import BooleanOperatorConstruct


class DVFA:
    """Class for holding a DVFA. """

    def __init__(self, starting_state: State = None):
        self._starting_state: State = starting_state
        self.var_set: set = set()
        self.const_set: set = set()
        self._map_properties()

    @property
    def starting_state(self) -> State:
        return self._starting_state

    # TODO: create a list of states and transitions, update copy and complement
    def _map_properties(self):
        # Our implementation of BFS,
        # in order to fill DVFA's variables set, and constants set.

        bfs_queue = [self._starting_state]
        visited_states = set(bfs_queue)

        for state in bfs_queue:
            for symbol, neighbor in state.transition_map.items():

                if isinstance(symbol, str):
                    if symbol != "y":
                        self.var_set.add(symbol)
                else:
                    self.const_set.add(symbol)
                if neighbor not in visited_states:
                    visited_states.add(neighbor)
                    bfs_queue.append(neighbor)

    def copy(self):
        """

        :return: this function returns a copy of the DVFA
        """
        # Run BFS to get a map of every state in A: new state in copy of A
        bfs_queue = [self._starting_state]
        visited_states = dict()
        visited_states[self.starting_state] = State(name=self.starting_state.name,
                                                    is_accepting=self.starting_state.is_accepting)

        for state in bfs_queue:
            for symbol, neighbor in state.transition_map.items():
                if neighbor not in visited_states.keys():
                    visited_states[neighbor] = State(name=neighbor.name,
                                                     is_accepting=neighbor.is_accepting)
                    bfs_queue.append(neighbor)
                visited_states[state].add_transition(symbol=symbol, state=visited_states[neighbor])
        return DVFA(starting_state=visited_states[self.starting_state])

    def complement(self):
        """

        :return: this function returns a complementing DVFA
        """
        # Run BFS to get a map of every state in A: new state in copy of A
        bfs_queue = [self._starting_state]
        visited_states = dict()
        visited_states[self.starting_state] = State(name=self.starting_state.name,
                                                    is_accepting=(not self.starting_state.is_accepting))

        for state in bfs_queue:
            for symbol, neighbor in state.transition_map.items():
                if neighbor not in visited_states.keys():
                    visited_states[neighbor] = State(name=neighbor.name,
                                                     is_accepting=(not neighbor.is_accepting))
                    bfs_queue.append(neighbor)
                visited_states[state].add_transition(symbol=symbol, state=visited_states[neighbor])
        return DVFA(starting_state=visited_states[self.starting_state])

    @staticmethod
    def unwind(A):
        """
        This function
        :param A: a DVFA
        :return: (unwinded_DVFA, map[key=state,value=[symbols]])
        """
        # Starting point, get first state, as
        u_states_dict = dict()
        u_result_dict = dict()
        u_state = DVFA._recursive_unwinding(A, current_tuple=None, u_states_dict=u_states_dict, is_first=True)
        for unwind_tuple, state in u_states_dict.items():
            u_result_dict[state] = unwind_tuple[1]
        return DVFA(u_state), u_result_dict

    @staticmethod
    def _recursive_unwinding(A, current_tuple: tuple, u_states_dict: dict, is_first: bool) -> State:
        """
        The first run of recursive unwinding will init current_tuple and tuple_set, this was done so that each call to
        _recursive_unwinding will create one state exactly
        :param A: The target DVFA
        :param current_tuple: The current tuple of <state, set> where set is a frozenset of the letters used to reach
        state
        :param u_states_dict: A dict containing all {tuple:state} state is from the new (unwinded) DVFA
        :param is_first: Set True for the first call, False for the rest, used to init params
        :return: State that is the first state of the DVFA
        """
        if is_first:
            # init some data structures, frozenset can be used as a key in dict, as its immutable
            starting_tuple = (A.starting_state, frozenset())
            current_tuple = starting_tuple

        # construct the result state
        # name for ex. "s1 (x1,y)"
        new_name = "{0} ({1})".format(current_tuple[0].name, ",".join(current_tuple[1]))
        # so that L(A) will be the same as L(U(A))
        is_accepting = current_tuple[0].is_accepting
        # create the state and put it in the dict, the dict has two purposes:
        # I) so that we can save newly generated states, this is done to prevent state duplication (and in some cases,
        # infinite loops)
        # II) return value to the user
        new_state = State(name=new_name, is_accepting=is_accepting)
        u_states_dict.update({current_tuple: new_state})

        # the newly minted state transition map
        transition_map = dict()

        # iterate on each {symbol,state} transition of this state.
        for symbol, next_state in current_tuple[0].transition_map.items():
            next_symbols = set()
            if symbol == "y":
                # optimization
                # if symbol is wildcard, don't pass on all the var_set.
                next_symbols = next_symbols.union(current_tuple[1])
                next_symbols.add("y")
                next_symbols = frozenset(next_symbols)
            elif symbol in A.var_set:
                # if symbol is known as a variable or a WILDCARD in this DVFA,
                # then add it to current tuple read variables set,
                # because its a variable that was read in order to get to this state.
                next_symbols = next_symbols.union(current_tuple[1])
                next_symbols.add(symbol)
                next_symbols = frozenset(next_symbols)
            else:
                # if the symbol is not in this DVFA variable set.
                next_symbols = frozenset(current_tuple[1])
            # if true - it means that the state we need already exists in u_states_dict, we can simply take an existing
            # state from the unwinded DVFA
            next_tuple = (next_state, next_symbols)
            if next_tuple in u_states_dict.keys():
                result_state = u_states_dict[(next_state, next_symbols)]
                transition_map[symbol] = result_state

            # else - we need to calculate the rest of the transitions
            else:
                result_state = DVFA._recursive_unwinding(A=A,
                                                         current_tuple=next_tuple,
                                                         u_states_dict=u_states_dict,
                                                         is_first=False)
                transition_map[symbol] = result_state

        # create the state's transition map
        for sym, state in transition_map.items():
            new_state.add_transition(sym, state)
        return new_state

    @staticmethod
    def intersect(A, B):
        """

        :param A: DVFA
        :param B: DVFA
        :return: intersected DVFA
        """
        U1, U1_dict = DVFA.unwind(A)
        U2, U2_dict = DVFA.unwind(B)

        op_construct = BooleanOperatorConstruct(u1=U1, u1_dict=U1_dict, u2=U2, u2_dict=U2_dict)
        const_matchings = op_construct.calculate_common_constants_matchings()
        new_rule = (U1.starting_state, U2.starting_state, const_matchings)
        new_starting_state = DVFA._recursive_intersect(current_rule=new_rule, op_construct=op_construct)

        return DVFA(starting_state=new_starting_state)

    @staticmethod
    def _recursive_intersect(current_rule: tuple, op_construct):
        existing_rule = op_construct.get_from_rules(current_rule)
        if existing_rule is not None:
            # We already traversed this state in Intersect(U1,U2), we should simply return it
            return existing_rule[3]
        else:
            # Create the new state
            state_1: State = current_rule[0]
            state_2: State = current_rule[1]
            current_matchings: frozenset = current_rule[2]
            new_state = BooleanOperatorConstruct.new_state(s1=state_1, s2=state_2)

            # Insert it to the helper
            existing_rule = (state_1, state_2, current_matchings, new_state)
            op_construct.new_rule(rule=existing_rule)

            u1 = op_construct.u1
            u2 = op_construct.u2

            # We need to determine the kind of new variable state_1 and state_2 introduce
            # in accordance with the theory:
            # I) If both introduce new bound variable - it will match as a new bound variable in the union construct
            # II) If only one introduce new bound variable - it will match with the "y" on the other DVFA as a
            # new bound variable
            # III) If none introduce new bound variable - both wildcards will match to create a new wildcard

            new_bound_variables_u1 = state_1.transition_map.keys()
            new_bound_variables_u1 = new_bound_variables_u1 - u1.const_set
            new_bound_variables_u1 = new_bound_variables_u1 - op_construct.u1_dict[state_1]

            new_bound_variables_u2 = state_2.transition_map.keys()
            new_bound_variables_u2 = new_bound_variables_u2 - u2.const_set
            new_bound_variables_u2 = new_bound_variables_u2 - op_construct.u2_dict[state_2]

            u1_new_vars = len(new_bound_variables_u1) == 1
            u2_new_vars = len(new_bound_variables_u2) == 1

            # By default, new variables are matched with wildcard so we will 'exploit' this property
            new_var1 = "y"
            new_var2 = "y"

            # state_1 introduced new variable
            if u1_new_vars:
                new_var1 = new_bound_variables_u1.pop()
            # state_2 introduced new variable
            if u2_new_vars:
                new_var2 = new_bound_variables_u2.pop()

            # create the next set of matchings
            new_matching = frozenset([(new_var1, new_var2)])
            next_matchings = current_matchings.union(new_matching)

            # create the next set of matchings
            next_rule = (state_1.transition(new_var1), state_2.transition(new_var2), next_matchings)

            # create the next transition in the intersection/union construct using recursive function
            next_state = DVFA._recursive_intersect(current_rule=next_rule, op_construct=op_construct)
            next_sym = op_construct.new_var_name(var1=new_var1, var2=new_var2)
            new_state.add_transition(symbol=next_sym, state=next_state)

            # Handling existing matchings
            for matching in current_matchings:
                # create the next set of rules
                next_rule = (state_1.transition(matching[0]), state_2.transition(matching[1]), current_matchings)

                # create the next transition in the intersection/union construct using recursive function
                next_state = DVFA._recursive_intersect(current_rule=next_rule, op_construct=op_construct)
                next_sym = op_construct.new_var_name(var1=matching[0], var2=matching[1])
                new_state.add_transition(symbol=next_sym, state=next_state)

            # Handling constants
            unmatched_consts1 = u1.const_set.copy()
            unmatched_consts2 = u2.const_set.copy()

            for matching in current_matchings:
                unmatched_consts1.discard(matching[0])
                unmatched_consts2.discard(matching[1])

            if u1_new_vars:
                for const in unmatched_consts2:
                    # create the next transition in the intersection/union construct using recursive function
                    # for new variables from u1 and consts from u2

                    # create the next set of matchings
                    new_matching = frozenset([(new_var1, const)])
                    next_matchings = current_matchings.union(new_matching)

                    # create the next set of matchings
                    next_rule = (state_1.transition(new_var1), state_2.transition(const), next_matchings)
                    next_state = DVFA._recursive_intersect(current_rule=next_rule, op_construct=op_construct)
                    next_sym = op_construct.new_var_name(var1=new_var1, var2=const)
                    new_state.add_transition(symbol=next_sym, state=next_state)

            if u2_new_vars:
                for const in unmatched_consts1:
                    # create the next transition in the intersection/union construct using recursive function
                    # for new variables from u1 and consts from u2

                    # create the next set of matchings
                    new_matching = frozenset([(const, new_var2)])
                    next_matchings = current_matchings.union(new_matching)

                    # create the next set of matchings
                    next_rule = (state_1.transition(const), state_2.transition(new_var2), next_matchings)
                    next_state = DVFA._recursive_intersect(current_rule=next_rule, op_construct=op_construct)
                    next_sym = op_construct.new_var_name(var1=const, var2=new_var2)
                    new_state.add_transition(symbol=next_sym, state=next_state)

        return new_state
