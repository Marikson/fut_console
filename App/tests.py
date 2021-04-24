import unittest
import login
import list_players
import team_editor
import vars


class CredentialsTests(unittest.TestCase):
    def test_login(self):
        wrong_username = login.authenticate("asdf", "test")
        wrong_password = login.authenticate("TestUser", "asdf")
        authenticate_succeeded = login.authenticate("TestUser", "test")
        self.assertEqual(wrong_username, False)
        self.assertEqual(wrong_password, False)
        self.assertEqual(authenticate_succeeded, True)
        self.assertEqual(vars.user_id, 4)
        self.assertEqual(vars.users_id_url, "http://localhost:3000/Users/4")

    def test_list_player(self):
        vars.user_id = 4
        vars.users_id_url = "http://localhost:3000/Users/4"
        owned_players = list_players.get_users_players_id('owned_players')
        starting_11 = list_players.get_users_players_id('starting_11')
        starting_11_ids = list(starting_11.values())
        matched_starting = list_players.select_matching(starting_11_ids, "starting_11")
        starting = matched_starting.ids
        at_starting = matched_starting.at_ind
        starting_found = matched_starting.found_counter
        matched_owned = list_players.select_matching(owned_players, "owned_players")
        owned = matched_owned.ids
        at_owned = matched_owned.at_ind
        owned_found = matched_owned.found_counter
        self.assertEqual(len(owned_players), 1)
        self.assertEqual(len(starting_11), 11)
        self.assertDictEqual(starting_11, {"GK": 834, "RB": 2308, "RCB": 8167, "LCB": 1378, "LB": 5336, "RM": 90, "RCM": 13249, "LCM": 4836, "LM": 9119, "RST": 26052, "LST": 24775})
        self.assertListEqual(owned_players, [1])
        self.assertEqual(len(starting), 11)
        self.assertEqual(starting, {"GK": 834, "RB": 2308, "RCB": 8167, "LCB": 1378, "LB": 5336, "RM": 90, "RCM": 13249, "LCM": 4836, "LM": 9119, "RST": 26052, "LST": 24775})
        self.assertEqual(starting_found, 11)
        self.assertEqual(len(at_starting), 11)
        self.assertEqual(at_starting, {"GK": 834, "RB": 2308, "RCB": 8167, "LCB": 1378, "LB": 5336, "RM": 90, "RCM": 13249, "LCM": 4836, "LM": 9119, "RST": 26052, "LST": 24775})
        self.assertEqual(len(owned), 1)
        self.assertListEqual(owned_players, [1])
        self.assertEqual(owned_found, 1)
        self.assertEqual(len(at_owned), 1)
        self.assertDictEqual(at_owned, {0: 1})

    def test_team_editor(self):
        vars.user_id = 4
        vars.users_id_url = "http://localhost:3000/Users/4"
        changing_with_wrong_id = team_editor.changing([1, 2])
        changing_with_wrong_ids = team_editor.changing([3, 2])
        changing_in_reserve = team_editor.changing([1, 1])
        changing_with_itself = team_editor.changing([90, 90])
        changing_with_good_ids_reserve_to_starting = team_editor.changing([1, 90])
        changing_with_good_ids_starting_to_reserve = team_editor.changing([90, 1])
        changing_with_good_ids_starting_to_starting = team_editor.changing([90, 834])
        changing_with_good_ids_starting_to_starting_2 = team_editor.changing([834, 90])
        self.assertEqual(changing_with_wrong_id, False)
        self.assertEqual(changing_with_wrong_ids, False)
        self.assertEqual(changing_in_reserve, False)
        self.assertEqual(changing_with_itself, False)
        self.assertEqual(changing_with_good_ids_reserve_to_starting, True)
        self.assertEqual(changing_with_good_ids_starting_to_reserve, True)
        self.assertEqual(changing_with_good_ids_starting_to_starting, True)
        self.assertEqual(changing_with_good_ids_starting_to_starting_2, True)


if __name__ == '__main__':
    unittest.main()
