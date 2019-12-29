from DVFApy.state import State


class BooleanOperatorConstruct:
    """
    This class is aggregating several data structures that are required for intersect and union operations, it
    should not be exposed to the user.
    """

    def __init__(self, u1, u1_dict: dict, u2, u2_dict: dict, is_union = False):
        # rule is a 4-tuple (state1,state2,{(x1,x2)},state12)
        # states_dict and rules_dict are symmetrical, inserting should happen simultaneously
        self.rules_dict = dict()
        self.states_dict = dict()

        # vars dict keys are (x1,x2) and its values are x12
        self.vars_dict = dict()

        # u1 and u2 are the unwinded DVFAs
        self._u1 = u1
        self._u2 = u2

        # u1_dict and u2_dict are the unwind dicts - for each state which symbols were read to reach it
        self._u1_dict = u1_dict
        self._u2_dict = u2_dict

        # default mode is intersect, is_union is a flag which will change it to union mode
        self._is_union = is_union

    @property
    def u1(self):
        return self._u1

    @property
    def u2(self):
        return self._u2

    @property
    def u1_dict(self) -> dict:
        return self._u1_dict

    @property
    def u2_dict(self) -> dict:
        return self._u2_dict

    def new_rule(self, rule: tuple):
        """
        new_rule will insert a new rule to both rules_dict and states_dict
        :param rule: rule is a 4-tuple (state1,state2,{(x1,x2)},state12)
        :return: None
        """
        rule_key = (rule[0], rule[1], rule[2])
        state_key = rule[3]

        self.rules_dict[rule_key] = rule
        self.states_dict[state_key] = rule

    def get_from_rules(self, rule: tuple):
        return self.rules_dict.get(rule)

    def get_from_states(self, state: State):
        return self.states_dict.get(state)

    def calculate_common_constants_matchings(self):
        u1_consts: set = self.u1.const_set
        u2_consts: set = self.u2.const_set
        common_const_set = u1_consts.intersection(u2_consts)
        matchings = set()
        for const in common_const_set:
            matchings.add((const, const))
        return frozenset(matchings)

    @staticmethod
    def new_var_name(var1: str, var2: str):
        # Two wildcards produce wildcard
        if var1 == "y" and var2 == "y":
            return "y"
        # If either var1 or var2 are constants, they should "take over" the transition
        elif isinstance(var1, int):
            return var1
        elif isinstance(var2, int):
            return var2
        # Finally, if both are bound variables, unite them
        else:
            new_var = "{}_{}".format(var1, var2)
            return new_var

    def new_state_name(self, s1: State, s2: State):
        s1_name = s1.name
        s2_name = s2.name
        return "{}_{}".format(s1_name, s2_name)

    def new_state(self, s1: State, s2: State):
        if self._is_union:
            is_current_state_accepting = s1.is_accepting or s2.is_accepting
        else:
            is_current_state_accepting = s1.is_accepting and s2.is_accepting
        current_state_name = self.new_state_name(s1=s1, s2=s2)
        return State(name=current_state_name, is_accepting=is_current_state_accepting)
