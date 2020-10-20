import unittest
from main import biconditional_elimination, implication_elimination, de_morgan_laws, delete_duplicates, \
    nnf_to_dnf_transition, check_satisfiability


class TestBiconditionalElimination(unittest.TestCase):

    def test_first_case(self):
        self.assertEqual(biconditional_elimination('p<>q'), '(p>>q)&(q>>p)')

    def test_second_case(self):
        self.assertEqual(biconditional_elimination('p&q<>p&r'), '(p&q>>p&r)&(p&r>>p&q)')

    def test_third_case(self):
        self.assertEqual(biconditional_elimination('(p<>q)>>p&q'), '(p>>q)&(q>>p)>>p&q')

    def test_fourth_case(self):
        self.assertEqual(biconditional_elimination('(p>>q)<>p&~q'), '((p>>q)>>p&~q)&(p&~q>>(p>>q))')

    def test_fifth_case(self):
        self.assertEqual(
            biconditional_elimination(
                '(p>>q&r)<>(p>>q)&(p>>r)'
            ),
            '((p>>q&r)>>(p>>q)&(p>>r))&((p>>q)&(p>>r)>>(p>>q&r))'
        )

    def test_sixth_case(self):
        self.assertEqual(
            biconditional_elimination(
                '(p|q>>r)<>(p>>r)&(q>>r)'
            ),
            '((p|q>>r)>>(p>>r)&(q>>r))&((p>>r)&(q>>r)>>(p|q>>r))'
        )

    def test_seventh_case(self):
        self.assertEqual(
            biconditional_elimination(
                '(p&q>>r)<>(p>>r)|(q>>r)'
            ),
            '((p&q>>r)>>(p>>r)|(q>>r))&((p>>r)|(q>>r)>>(p&q>>r))'
        )

    def test_eight_case(self):
        self.assertEqual(
            biconditional_elimination(
                '(p<>q)<>r'
            ),
            '((p>>q)&(q>>p)>>r)&(r>>(p>>q)&(q>>p))'
        )

    def test_ninth_case(self):
        self.assertEqual(
            biconditional_elimination(
                'p<>(r<>q)'
            ),
            '(p>>(r>>q)&(q>>r))&((r>>q)&(q>>r)>>p)'
        )


class TestImplicationElimination(unittest.TestCase):

    def test_first_case(self):
        self.assertEqual(implication_elimination('(p>>q)&(q>>p)'), '(~p|q)&(~q|p)')

    def test_second_case(self):
        self.assertEqual(implication_elimination('(p&q>>p&r)&(p&r>>p&q)'), '(~(p&q)|(p&r))&(~(p&r)|(p&q))')

    def test_third_case(self):
        self.assertEqual(implication_elimination('(p>>q)&(q>>p)>>p&q'), '~((~p|q)&(~q|p))|(p&q)')

    def test_fourth_case(self):
        self.assertEqual(
            implication_elimination(
                '((p>>q)>>p&~q)&(p&~q>>(p>>q))'
            ),
            '(~(~p|q)|(p&~q))&(~(p&~q)|~p|q)'
        )

    def test_fifth_case(self):
        self.assertEqual(
            implication_elimination(
                '((p>>q&r)>>(p>>q)&(p>>r))&((p>>q)&(p>>r)>>(p>>q&r))'
            ),
            '(~(~p|(q&r))|((~p|q)&(~p|r)))&(~((~p|q)&(~p|r))|~p|(q&r))'
        )

    def test_sixth_case(self):
        self.assertEqual(
            implication_elimination(
                '((p|q>>r)>>(p>>r)&(q>>r))&((p>>r)&(q>>r)>>(p|q>>r))'
            ),
            '(~(~(p|q)|r)|((~p|r)&(~q|r)))&(~((~p|r)&(~q|r))|~(p|q)|r)'
        )

    def test_seventh_case(self):
        self.assertEqual(
            implication_elimination(
                '((p&q>>r)>>(p>>r)|(q>>r))&((p>>r)|(q>>r)>>(p&q>>r))'
            ),
            '(~(~(p&q)|r)|~p|r|~q|r)&(~(~p|r|~q|r)|~(p&q)|r)'
        )

    def test_eight_case(self):
        self.assertEqual(
            implication_elimination(
                '((p>>q)&(q>>p)>>r)&(r>>(p>>q)&(q>>p))'
            ),
            '(~((~p|q)&(~q|p))|r)&(~r|((~p|q)&(~q|p)))'
        )

    def test_ninth_case(self):
        self.assertEqual(
            implication_elimination(
                '(p>>(r>>q)&(q>>r))&((r>>q)&(q>>r)>>p)'
            ),
            '(~p|((~r|q)&(~q|r)))&(~((~r|q)&(~q|r))|p)'
        )


class DeMorganLawsTest(unittest.TestCase):

    def test_first_case(self):
        self.assertEqual(de_morgan_laws('(~p|q)&(~q|p)'), '(~p|q)&(~q|p)')

    def test_second_case(self):
        self.assertEqual(de_morgan_laws('(~(p&q)|(p&r))&(~(p&r)|(p&q))'), '(~p|~q|(p&r))&(~p|~r|(p&q))')

    def test_third_case(self):
        self.assertEqual(de_morgan_laws('~((~p|q)&(~q|p))|(p&q)'), '(p&~q)|(q&~p)|(p&q)')

    def test_fourth_case(self):
        self.assertEqual(
            de_morgan_laws(
                '(~(~p|q)|(p&~q))&(~(p&~q)|~p|q)'
            ),
            '((p&~q)|(p&~q))&(~p|q|~p|q)'
        )

    def test_fifth_case(self):
        self.assertEqual(
            de_morgan_laws(
                '(~(~p|(q&r))|((~p|q)&(~p|r)))&(~((~p|q)&(~p|r))|~p|(q&r))'
            ),
            '((p&(~q|~r))|((~p|q)&(~p|r)))&((p&~q)|(p&~r)|~p|(q&r))'
        )

    def test_sixth_case(self):
        self.assertEqual(
            de_morgan_laws(
                '(~(~(p|q)|r)|((~p|r)&(~q|r)))&(~((~p|r)&(~q|r))|~(p|q)|r)'
            ),
            '(((p|q)&~r)|((~p|r)&(~q|r)))&((p&~r)|(q&~r)|(~p&~q)|r)'
        )

    def test_seventh_case(self):
        self.assertEqual(
            de_morgan_laws(
                '(~(~(p&q)|r)|~p|r|~q|r)&(~(~p|r|~q|r)|~(p&q)|r)'
            ),
            '((p&q&~r)|~p|r|~q|r)&((p&~r&q&~r)|~p|~q|r)'
        )

    def test_eight_case(self):
        self.assertEqual(
            de_morgan_laws(
                '(~((~p|q)&(~q|p))|r)&(~r|((~p|q)&(~q|p)))'
            ),
            '((p&~q)|(q&~p)|r)&(~r|((~p|q)&(~q|p)))'
        )

    def test_ninth_case(self):
        self.assertEqual(
            de_morgan_laws(
                '(~p|((~r|q)&(~q|r)))&(~((~r|q)&(~q|r))|p)'
            ),
            '(~p|((~r|q)&(~q|r)))&((r&~q)|(q&~r)|p)'
        )


class DeleteDuplicatesTest(unittest.TestCase):

    def test_first_case(self):
        self.assertEqual(delete_duplicates('(~p|q)&(~q|p)'), '(~p|q)&(~q|p)')

    def test_second_case(self):
        self.assertEqual(delete_duplicates('(~p|~q|(p&r))&(~p|~r|(p&q))'), '(~p|~q|(p&r))&(~p|~r|(p&q))')

    def test_third_case(self):
        self.assertEqual(delete_duplicates('(p&~q)|(q&~p)|(p&q)'), '(p&~q)|(q&~p)|(p&q)')

    def test_fourth_case(self):
        self.assertEqual(
            delete_duplicates(
                '((p&~q)|(p&~q))&(~p|q|~p|q)'
            ),
            'p&~q&(~p|q)'
        )

    def test_fifth_case(self):
        self.assertEqual(
            delete_duplicates(
                '((p&(~q|~r))|((~p|q)&(~p|r)))&((p&~q)|(p&~r)|~p|(q&r))'
            ),
            '((p&(~q|~r))|((~p|q)&(~p|r)))&((p&~q)|(p&~r)|~p|(q&r))'
        )

    def test_sixth_case(self):
        self.assertEqual(
            delete_duplicates(
                '(((p|q)&~r)|((~p|r)&(~q|r)))&((p&~r)|(q&~r)|(~p&~q)|r)'
            ),
            '(((p|q)&~r)|((~p|r)&(~q|r)))&((p&~r)|(q&~r)|(~p&~q)|r)'
        )

    def test_seventh_case(self):
        self.assertEqual(
            delete_duplicates(
                '((p&q&~r)|~p|r|~q|r)&((p&~r&q&~r)|~p|~q|r)'
            ),
            '(p&q&~r)|~p|r|~q'
        )

    def test_eight_case(self):
        self.assertEqual(
            delete_duplicates(
                '((p&~q)|(q&~p)|r)&(~r|((~p|q)&(~q|p)))'
            ),
            '((p&~q)|(q&~p)|r)&(~r|((~p|q)&(~q|p)))'
        )

    def test_ninth_case(self):
        self.assertEqual(
            delete_duplicates(
                '(~p|((~r|q)&(~q|r)))&((r&~q)|(q&~r)|p)'
            ),
            '(~p|((~r|q)&(~q|r)))&((r&~q)|(q&~r)|p)'
        )


class NpnToApnTest(unittest.TestCase):

    def test_first_case(self):
        self.assertEqual(nnf_to_dnf_transition('(~p|q)&(~q|p)'), '(~q&~p)|(~q&q)|(p&~p)|(p&q)')

    def test_second_case(self):
        self.assertEqual(
            nnf_to_dnf_transition(
                '(~p|~q|(p&r))&(~p|~r|(p&q))'
            ),
            '~p|(~p&~q)|(~p&p&r)|(~r&~p)|(~r&~q)|(~r&p&r)|(p&q&~p)|(p&q&~q)|(p&q&r)'
        )

    def test_third_case(self):
        self.assertEqual(nnf_to_dnf_transition('(p&~q)|(q&~p)|(p&q)'), '(p&~q)|(q&~p)|(p&q)')

    def test_fourth_case(self):
        self.assertEqual(
            nnf_to_dnf_transition(
                'p&~q&(~p|q)'
            ),
            '(p&~q&~p)|(p&~q&q)'
        )

    def test_fifth_case(self):
        self.assertEqual(
            nnf_to_dnf_transition(
                '((p&(~q|~r))|((~p|q)&(~p|r)))&((p&~q)|(p&~r)|~p|(q&r))'
            ),
            '(p&~q)|(p&~q&~r)|(p&~q&~p&q)|(p&~q&r&~p)|(p&~q&r&q)|(p&~r)|(p&~r&~p&q)|(p&~r&r&~p)|(p&~r&r&q)|('
            '~p&p&~q)|(~p&p&~r)|(~p&p)|(~p&q)|(~p&r)|(~p&r&q)|(q&r&p)|(q&r)'
        )

    def test_sixth_case(self):
        self.assertEqual(
            nnf_to_dnf_transition(
                '(((p|q)&~r)|((~p|r)&(~q|r)))&((p&~r)|(q&~r)|(~p&~q)|r)'
            ),
            '(p&~r)|(p&~r&q)|(p&~r&~q&~p)|(p&~r&~q&r)|(p&~r&r&~p)|(p&~r&r)|(q&~r)|(q&~r&~q&~p)|(q&~r&~q&r)|('
            'q&~r&r&~p)|(q&~r&r)|(~p&~q)|(~p&~q&r)|(r&~q)|(r&~p)|r'
        )

    def test_seventh_case(self):
        self.assertEqual(
            nnf_to_dnf_transition(
                '(p&q&~r)|~p|r|~q'
            ),
            '(p&q&~r)|~p|r|~q'
        )

    def test_eight_case(self):
        self.assertEqual(
            nnf_to_dnf_transition(
                '((p&~q)|(q&~p)|r)&(~r|((~p|q)&(~q|p)))'
            ),
            '(~r&p&~q)|(~r&q&~p)|(~r&r)|(~q&~p&p)|(~q&~p&q)|(~q&~p&r)|(~q&q&p)|(~q&q&r)|(p&~p&q)|(p&~p&r)|(p&q&r)'
        )

    def test_ninth_case(self):
        self.assertEqual(
            nnf_to_dnf_transition(
                '(~p|((~r|q)&(~q|r)))&((r&~q)|(q&~r)|p)'
            ),
            '(r&~q&~p)|(r&~q&~r)|(r&~q&q)|(q&~r&~p)|(q&~r&~q)|(q&~r&r)|(p&~p)|(p&~q&~r)|(p&~q&q)|(p&r&~r)|(p&r&q)'
        )


class CheckFalsifiabilityTest(unittest.TestCase):

    def test_first_case(self):
        self.assertEqual(check_satisfiability('(~q&~p)|(~q&q)|(p&~p)|(p&q))'), False)

    def test_second_case(self):
        self.assertEqual(
            check_satisfiability(
                '~p|(~p&~q)|(~p&p&r)|(~r&~p)|(~r&~q)|(~r&p&r)|(p&q&~p)|(p&q&~q)|(p&q&r)'
            ),
            False
        )

    def test_third_case(self):
        self.assertEqual(check_satisfiability('(p&~q)|(q&~p)|(p&q)'), False)

    def test_fourth_case(self):
        self.assertEqual(
            check_satisfiability(
                '(p&~q&~p)|(p&~q&q)'
            ),
            True
        )

    def test_fifth_case(self):
        self.assertEqual(
            check_satisfiability(
                '(p&~q)|(p&~q&~r)|(p&~q&~p&q)|(p&~q&r&~p)|(p&~q&r&q)|(p&~r)|(p&~r&~p&q)|(p&~r&r&~p)|(p&~r&r&q)|('
                '~p&p&~q)|(~p&p&~r)|(~p&p)|(~p&q)|(~p&r)|(~p&r&q)|(q&r&p)|(q&r)'
            ),
            False
        )

    def test_sixth_case(self):
        self.assertEqual(
            check_satisfiability(
                '(p&~r)|(p&~r&q)|(p&~r&~q&~p)|(p&~r&~q&r)|(p&~r&r&~p)|(q&~r)|(q&~r&~q&~p)|(q&~r&~q&r)|(q&~r&r&~p)|('
                '~p&~q)|(~p&~q&r)|(r&~r&p)|(r&~r&q)|(r&~q)|(r&~p)'
            ),
            False
        )

    def test_seventh_case(self):
        self.assertEqual(
            check_satisfiability(
                '(p&q&~r)|~p|r|~q'
            ),
            False
        )

    def test_eight_case(self):
        self.assertEqual(
            check_satisfiability(
                '(~r&p&~q)|(~r&q&~p)|(~r&r)|(~q&~p&p)|(~q&~p&q)|(~q&~p&r)|(~q&q&p)|(~q&q&r)|(p&~p&q)|(p&~p&r)|(p&q&r)'
            ),
            False
        )

    def test_ninth_case(self):
        self.assertEqual(
            check_satisfiability(
                '(r&~q&~p)|(r&~q&~r)|(r&~q&q)|(q&~r&~p)|(q&~r&~q)|(q&~r&r)|(p&~p)|(p&~q&~r)|(p&~q&q)|(p&r&~r)|(p&r&q)'
            ),
            False
        )


if __name__ == '__main__':
    unittest.main()
