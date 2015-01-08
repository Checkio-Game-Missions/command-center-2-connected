init_code = """
if not "Friends" in USER_GLOBAL:
    raise NotImplementedError("Where is 'Friends'?")

Friends = USER_GLOBAL['Friends']
"""

PASS_CODE = """
RET['code_result'] = True, "Ok"
"""


def prepare_test(middle_code, test_code, show_code, show_answer):
    if show_code is None:
        show_code = middle_code
    return {"test_code": {"python-3": init_code + middle_code + test_code,
                          "python-27": init_code + middle_code + test_code},
            "show": {"python-3": show_code,
                     "python-27": show_code},
            "answer": show_answer}


TESTS = {
    "1. Init": [
        prepare_test('Friends(({"a", "b"}, {"b", "c"}, {"c", "a"}, {"a", "c"}))\n',
                     PASS_CODE, None, None),
        prepare_test('Friends([{"1", "2"}, {"3", "1"}])\n', PASS_CODE, None, None),
    ],
    "2. Add": [
        prepare_test('f = Friends([{"1", "2"}, {"3", "1"}])\n'
                     'add_result = f.add({"2", "4"})\n',
                     "RET['code_result'] = add_result is True, str(add_result)",
                     'f = Friends([{"1", "2"}, {"3", "1"}])\n'
                     'f.add({"2", "4"})',
                     "True"
        ),
        prepare_test('f = Friends([{"And", "Or"}, {"For", "And"}])\n'
                     'add_result = f.add({"It", "Am"})\n',
                     "RET['code_result'] = add_result is True, str(add_result)",
                     'f = Friends([{"And", "Or"}, {"For", "And"}])\n'
                     'f.add({"It", "Am"})\n',
                     "True"),
        prepare_test('f = Friends([{"And", "Or"}, {"For", "And"}])\n'
                     'add_result = f.add({"Or", "And"})\n',
                     "RET['code_result'] = add_result is False, str(add_result)",
                     'f = Friends([{"And", "Or"}, {"For", "And"}])\n'
                     'f.add({"Or", "And"})\n',
                     "True")
    ],
    "3. Remove": [
        prepare_test('f = Friends([{"1", "2"}, {"3", "1"}])\n'
                     'remove_result = f.remove({"2", "4"})\n',
                     "RET['code_result'] = remove_result is False, str(remove_result)",
                     'f = Friends([{"1", "2"}, {"3", "1"}])\n'
                     'f.remove({"2", "4"})',
                     "False"),
        prepare_test('f = Friends([{"1", "2"}, {"3", "1"}])\n'
                     'remove_result = f.remove({"11", "12"})\n',
                     "RET['code_result'] = remove_result is False, str(remove_result)",
                     'f = Friends([{"1", "2"}, {"3", "1"}])\n'
                     'f.remove({"11", "12"})',
                     "False"),

        prepare_test('f = Friends([{"And", "Or"}, {"For", "And"}])\n'
                     'remove_result = f.remove({"And", "Or"})\n',
                     "RET['code_result'] = remove_result is True, str(remove_result)",
                     'f = Friends([{"And", "Or"}, {"For", "And"}])\n'
                     'f.remove({"And", "Or"})\n',
                     "True"),
    ],
    "4. Names": [
        prepare_test(
            'f = Friends(({"nikola", "sophia"}, {"stephen", "robot"}, {"sophia", "pilot"}))\n'
            'n = f.names()\n',
            'RET["code_result"] = (n == {"nikola", "sophia", "robot", "pilot", "stephen"}, str(n))',
            'f = Friends(({"nikola", "sophia"}, {"stephen", "robot"}, {"sophia", "pilot}))\n'
            'f.names()',
            '{"nikola", "sophia", "robot", "pilot", "stephen"}'),
        prepare_test(
            'f = Friends(({"nikola", "sophia"}, {"stephen", "robot"}, {"sophia", "pilot"}))\n'
            'f.remove({"stephen", "robot"})\n'
            'n = f.names()\n',
            'RET["code_result"] = (n == {"nikola", "sophia", "pilot"}, str(n))',
            'f = Friends(({"nikola", "sophia"}, {"stephen", "robot"}, {"sophia", "pilot}))\n'
            'f.remove({"stephen", "robot"})\n'
            'f.names()',
            '{"nikola", "sophia", "pilot"}'),

    ],
    "5. Connected": [
        prepare_test(
            'f = Friends(({"nikola", "sophia"}, {"stephen", "robot"}, {"sophia", "pilot"}))\n'
            'n = f.connected("nikola")\n',
            'RET["code_result"] = (n == {"sophia"}, str(n))',
            'f = Friends(({"nikola", "sophia"}, {"stephen", "robot"}, {"sophia", "pilot"}))\n'
            'f.connected("nikola")',
            '{"sophia"}'),
        prepare_test(
            'f = Friends(({"nikola", "sophia"}, {"stephen", "robot"}, {"sophia", "pilot"}))\n'
            'n = f.connected("sophia")\n',
            'RET["code_result"] = (n == {"nikola", "pilot"}, str(n))',
            'f = Friends(({"nikola", "sophia"}, {"stephen", "robot"}, {"sophia", "pilot"}))\n'
            'f.connected("sophia")',
            '{"nikola", "pilot"}'),
        prepare_test(
            'f = Friends(({"nikola", "sophia"}, {"stephen", "robot"}, {"sophia", "pilot"}))\n'
            'n = f.connected("DDD")\n',
            'RET["code_result"] = (n == set(), str(n))',
            'f = Friends(({"nikola", "sophia"}, {"stephen", "robot"}, {"sophia", "pilot"}))\n'
            'f.connected("DDD")',
            'set()'),
        prepare_test(
            'f = Friends(({"nikola", "sophia"}, {"stephen", "robot"}, {"sophia", "pilot"}))\n'
            'f.add({"sophia", "stephen"})\n'
            'f.remove({"sophia", "nikola"})\n'
            'n = f.connected("sophia")\n',
            'RET["code_result"] = (n == {"stephen", "pilot"}, str(n))',
            'f = Friends(({"nikola", "sophia"}, {"stephen", "robot"}, {"sophia", "pilot"}))\n'
            'f.add({"sophia", "stephen"})\n'
            'f.remove({"sophia", "nikola"})\n'
            'f.connected("sophia")\n',
            '{"stephen", "pilot"}'),


    ]




    #     prepare_test(test="str(Building(1, 1, 2, 2))",
    #                  answer="Building(1, 1, 2, 2, 10)", ),
    #     prepare_test(test="str(Building(0.2, 1, 2, 2.2, 3.5))",
    #                  answer="Building(0.2, 1, 2, 2.2, 3.5)", ),
    # ],
    # "3. Corners": [
    #     prepare_test(test="Building(1, 1, 2, 2).corners()",
    #                  answer={"south-west": [1, 1], "north-west": [3, 1], "north-east": [3, 3],
    #                          "south-east": [1, 3]}),
    #     prepare_test(test="Building(100.5, 0.5, 24.3, 12.2, 3).corners()",
    #                  answer={"north-east": [112.7, 24.8], "north-west": [112.7, 0.5],
    #                          "south-west": [100.5, 0.5], "south-east": [100.5, 24.8]}),
    # ],
    # "4. Area, Volume": [
    #     prepare_test(test="Building(1, 1, 2, 2, 100).area()",
    #                  answer=4),
    #     prepare_test(test="Building(100, 100, 135.5, 2000.1).area()",
    #                  answer=271013.55),
    #     prepare_test(test="Building(1, 1, 2, 2, 100).volume()",
    #                  answer=400),
    #     prepare_test(test="Building(100, 100, 135.5, 2000.1).volume()",
    #                  answer=2710135.5),
    # ]

}
