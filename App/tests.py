import unittest
import login
import list_players
import team_editor
import vars
import player_search
import request_try
import sell
import buy
import market_checker
from unittest import mock
unittest.TestLoader.sortTestMethodsUsing = None


@mock.patch("display.print_warning")
@mock.patch("display.print_info")
class CredentialsTests(unittest.TestCase):
    def test_login_wrong_all(self, mock_info, mock_warning):
        wrong_all = login.authenticate("asdf", "asdf")
        self.assertEqual(wrong_all, False)

    def test_login_wrong_username(self, mock_info, mock_warning):
        wrong_username = login.authenticate("asdf", "test")
        self.assertEqual(wrong_username, False)

    def test_login_wrong_password(self, mock_info, mock_warning):
        wrong_password = login.authenticate("TestUser", "asdf")
        self.assertEqual(wrong_password, False)

    def test_login_succeeded(self, mock_info, mock_warning):
        authenticate_succeeded = login.authenticate("TestUser", "test")
        self.assertEqual(authenticate_succeeded, True)
        self.assertEqual(vars.user_id, 4)
        self.assertEqual(vars.users_id_url, "http://localhost:3000/Users/4")


@mock.patch("display.print_warning")
@mock.patch("display.print_info")
@mock.patch("display.print_info_green")
@mock.patch("display.print_info_cyan")
class ListPlayerTests(unittest.TestCase):
    def setUp(self) -> None:
        vars.user_id = 4
        vars.users_id_url = "http://localhost:3000/Users/4"
        self.owned_players = list_players.get_users_players_id('owned_players')
        self.starting_11 = list_players.get_users_players_id('starting_11')
        self.starting_11_ids = list(self.starting_11.values())

    def test_list_owned_players(self, mock_cyan, mock_green, mock_info, mock_warning):
        self.assertEqual(len(self.owned_players), 1)
        self.assertListEqual(self.owned_players, [1])

    def test_list_starting_11(self, mock_cyan, mock_green, mock_info, mock_warning):
        self.assertEqual(len(self.starting_11), 11)
        self.assertDictEqual(self.starting_11,
                             {"GK": 834, "RB": 2308, "RCB": 8167, "LCB": 1378, "LB": 5336, "RM": 90, "RCM": 13249,
                              "LCM": 4836, "LM": 9119, "RST": 26052, "LST": 24775})

    def test_matched_owned(self, mock_cyan, mock_green, mock_info, mock_warning):
        matched_owned = list_players.select_matching(self.owned_players, "owned_players")
        owned = matched_owned.ids
        at_owned = matched_owned.at_ind
        owned_found = matched_owned.found_counter
        self.assertEqual(len(owned), 1)
        self.assertListEqual(owned, [1])
        self.assertEqual(len(at_owned), 1)
        self.assertDictEqual(at_owned, {0: 1})
        self.assertEqual(owned_found, 1)

    def test_matched_starting(self, mock_cyan, mock_green, mock_info, mock_warning):
        matched_starting = list_players.select_matching(self.starting_11_ids, "starting_11")
        starting = matched_starting.ids
        at_starting = matched_starting.at_ind
        starting_found = matched_starting.found_counter
        self.assertEqual(len(starting), 11)
        self.assertDictEqual(starting, {"GK": 834, "RB": 2308, "RCB": 8167, "LCB": 1378, "LB": 5336, "RM": 90,
                                        "RCM": 13249, "LCM": 4836, "LM": 9119, "RST": 26052, "LST": 24775})
        self.assertEqual(len(at_starting), 11)
        self.assertDictEqual(at_starting, {"GK": 834, "RB": 2308, "RCB": 8167, "LCB": 1378, "LB": 5336, "RM": 90,
                                           "RCM": 13249, "LCM": 4836, "LM": 9119, "RST": 26052, "LST": 24775})
        self.assertEqual(starting_found, 11)


@mock.patch("display.print_warning")
@mock.patch("display.print_info")
@mock.patch("display.print_info_green")
@mock.patch("display.print_info_cyan")
class TeamEditorTests(unittest.TestCase):
    def setUp(self) -> None:
        vars.user_id = 4
        vars.users_id_url = "http://localhost:3000/Users/4"

    def test_changing_with_wrong_id(self, mock_cyan, mock_green, mock_info, mock_warning):
        changing_with_wrong_id = team_editor.changing([1, 2])
        changing_with_wrong_ids = team_editor.changing([3, 2])
        self.assertEqual(changing_with_wrong_id, False)
        self.assertEqual(changing_with_wrong_ids, False)

    def test_changing_in_reserve(self, mock_cyan, mock_green, mock_info, mock_warning):
        changing_in_reserve = team_editor.changing([1, 1])
        self.assertEqual(changing_in_reserve, False)

    def test_changing_with_itself(self, mock_cyan, mock_green, mock_info, mock_warning):
        changing_with_itself = team_editor.changing([90, 90])
        self.assertEqual(changing_with_itself, False)

    def test_changing_good(self, mock_cyan, mock_green, mock_info, mock_warning):
        changing_with_good_ids_reserve_to_starting = team_editor.changing([1, 90])
        changing_with_good_ids_starting_to_reserve = team_editor.changing([90, 1])
        changing_with_good_ids_starting_to_starting = team_editor.changing([90, 834])
        changing_with_good_ids_starting_to_starting_2 = team_editor.changing([834, 90])
        self.assertEqual(changing_with_good_ids_reserve_to_starting, True)
        self.assertEqual(changing_with_good_ids_starting_to_reserve, True)
        self.assertEqual(changing_with_good_ids_starting_to_starting, True)
        self.assertEqual(changing_with_good_ids_starting_to_starting_2, True)


@mock.patch("display.print_warning")
@mock.patch("display.print_info")
@mock.patch("display.print_info_green")
@mock.patch("display.print_info_cyan")
class PlayerSearchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.buy_purpose = True

    def test_empty_input(self, mock_cyan, mock_green, mock_info, mock_warning):
        empty_aspect_input = player_search.is_valid_input([])
        empty_aspect_input_buy = player_search.is_valid_input([], self.buy_purpose)
        self.assertEqual(empty_aspect_input, False)
        self.assertEqual(empty_aspect_input_buy, False)

    def test_aspect_num_too_high(self, mock_cyan, mock_green, mock_info, mock_warning):
        aspect_num_too_high = player_search.is_valid_input(['9'])
        aspect_num_too_high_buy = player_search.is_valid_input(['11'], self.buy_purpose)
        self.assertEqual(aspect_num_too_high, False)
        self.assertEqual(aspect_num_too_high_buy, False)

    def test_aspect_num_too_low(self, mock_cyan, mock_green, mock_info, mock_warning):
        aspect_num_too_low = player_search.is_valid_input(['0'])
        aspect_num_too_low_buy = player_search.is_valid_input(['0'], self.buy_purpose)
        self.assertEqual(aspect_num_too_low, False)
        self.assertEqual(aspect_num_too_low_buy, False)

    def test_aspect_not_num(self, mock_cyan, mock_green, mock_info, mock_warning):
        aspect_not_num = player_search.is_valid_input(['asd'])
        aspect_not_num_buy = player_search.is_valid_input(['asd'], self.buy_purpose)
        self.assertEqual(aspect_not_num, False)
        self.assertEqual(aspect_not_num_buy, False)

    def test_aspect_list_with_empty(self, mock_cyan, mock_green, mock_info, mock_warning):
        aspect_list_with_empty = player_search.is_valid_input(['1', '2', ' ', '3'])
        aspect_list_with_empty_buy = player_search.is_valid_input(['1', '2', ' ', '3'], self.buy_purpose)
        self.assertEqual(aspect_list_with_empty, False)
        self.assertEqual(aspect_list_with_empty_buy, False)

    def test_aspect_list_with_too_high(self, mock_cyan, mock_green, mock_info, mock_warning):
        aspect_list_with_too_high = player_search.is_valid_input(['1', '2', '9'])
        aspect_list_with_too_high_buy = player_search.is_valid_input(['1', '2', '11'], self.buy_purpose)
        self.assertEqual(aspect_list_with_too_high, False)
        self.assertEqual(aspect_list_with_too_high_buy, False)

    def test_aspect_list_with_too_low(self, mock_cyan, mock_green, mock_info, mock_warning):
        aspect_list_with_too_low = player_search.is_valid_input(['1', '2', '0'])
        aspect_list_with_too_low_buy = player_search.is_valid_input(['1', '2', '0'], self.buy_purpose)
        self.assertEqual(aspect_list_with_too_low, False)
        self.assertEqual(aspect_list_with_too_low_buy, False)

    def test_aspect_list_with_not_num(self, mock_cyan, mock_green, mock_info, mock_warning):
        aspect_list_with_not_num = player_search.is_valid_input(['1', '2', 'asd'])
        aspect_list_with_not_num_buy = player_search.is_valid_input(['1', '2', 'asd'], self.buy_purpose)
        self.assertEqual(aspect_list_with_not_num, False)
        self.assertEqual(aspect_list_with_not_num_buy, False)

    def test_aspect_input_list_full_valid(self, mock_cyan, mock_green, mock_info, mock_warning):
        aspect_input_full_list_valid = player_search.is_valid_input(['1', '2', '3', '4', '5', '6', '7', '8'])
        aspect_input_valid_full_list_buy = player_search.is_valid_input(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], self.buy_purpose)
        self.assertEqual(aspect_input_full_list_valid, True)
        self.assertEqual(aspect_input_valid_full_list_buy, True)

    def test_aspect_input_list_valid(self, mock_cyan, mock_green, mock_info, mock_warning):
        aspect_input_list_valid = player_search.is_valid_input(['1', '5', '8'])
        aspect_input_list_valid_buy = player_search.is_valid_input(['1', '6', '10'], self.buy_purpose)
        self.assertEqual(aspect_input_list_valid, True)
        self.assertEqual(aspect_input_list_valid_buy, True)

    def test_back_as_input(self, mock_cyan, mock_green, mock_info, mock_warning):
        back_as_input = player_search.stay_check(['back'])
        self.assertEqual(back_as_input, False)

    def test_back_in_input(self, mock_cyan, mock_green, mock_info, mock_warning):
        back_in_input = player_search.stay_check(['1', 'back', '2'])
        self.assertEqual(back_in_input, False)

    def test_can_stay_at_menupoint(self, mock_cyan, mock_green, mock_info, mock_warning):
        no_back_in_input = player_search.stay_check(['1', '2', ' ', '3'])
        no_back_in_input_1 = player_search.stay_check(['1', '2', '9'])
        no_back_in_input_2 = player_search.stay_check(['1', '2', '0'])
        no_back_in_input_3 = player_search.stay_check(['1', '2', 'asd'])
        self.assertEqual(no_back_in_input, True)
        self.assertEqual(no_back_in_input_1, True)
        self.assertEqual(no_back_in_input_2, True)
        self.assertEqual(no_back_in_input_3, True)


@mock.patch("display.print_warning")
@mock.patch("display.print_info")
@mock.patch("display.print_info_green")
@mock.patch("display.print_info_cyan")
class SellPlayerTests(unittest.TestCase):
    def setUp(self) -> None:
        vars.user_id = 4
        vars.users_id_url = "http://localhost:3000/Users/4"
        user_before_sell = request_try.try_request_get(vars.users_URL, {'id': vars.user_id})
        self.user_owned_players_before_sell = user_before_sell[0]['owned_players']
        self.user_history_before_sell = user_before_sell[0]['history']

    def my_test1_selling_owned_player_named_alan_shearer(self):
        all_alan_shearer = request_try.try_request_get(vars.players_URL, {'player_extended_name': "Alan Shearer"})
        shearers_ids = sell.futbin_ids_with_resource_ids(all_alan_shearer)
        self.shearer_futbin_ids = list(shearers_ids.keys())
        self.assertEqual(len(all_alan_shearer), 3)
        self.assertListEqual(all_alan_shearer, [
            {'futbin_id': '1', 'player_name': 'Shearer', 'player_extended_name': 'Alan Shearer',
             'quality': 'Gold - Rare', 'revision': 'Icon', 'origin': 'Prime', 'overall': '91', 'club': 'FUT 21 ICONS',
             'league': 'Icons', 'nationality': 'England', 'position': 'ST', 'age': '50', 'date_of_birth': '1970.08.13',
             'height': '182', 'weight': '78', 'intl_rep': '5', 'added_date': '2020.09.10', 'pace': '81',
             'pace_acceleration': '82', 'pace_sprint_speed': '80', 'dribbling': '78', 'drib_agility': '71',
             'drib_balance': '71', 'drib_reactions': '87', 'drib_ball_control': '82', 'drib_dribbling': '76',
             'drib_composure': '88', 'shooting': '93', 'shoot_positioning': '92', 'shoot_finishing': '95',
             'shoot_shot_power': '94', 'shoot_long_shots': '86', 'shoot_volleys': '93', 'shoot_penalties': '94',
             'passing': '77', 'pass_vision': '76', 'pass_crossing': '77', 'pass_free_kick': '86', 'pass_short': '82',
             'pass_long': '63', 'pass_curve': '81', 'defending': '52', 'def_interceptions': '44', 'def_heading': '94',
             'def_marking': '28', 'def_stand_tackle': '65', 'def_slid_tackle': '55', 'physicality': '85',
             'phys_jumping': '88', 'phys_stamina': '84', 'phys_strength': '88', 'phys_aggression': '80',
             'gk_diving': '', 'gk_reflexes': '', 'gk_handling': '', 'gk_speed': '', 'gk_kicking': '',
             'gk_positoning': '', 'pref_foot': 'Right', 'att_workrate': 'High', 'def_workrate': 'Med', 'weak_foot': '3',
             'skill_moves': '2', 'cb': '66', 'rb': '68', 'lb': '68', 'rwb': '69', 'lwb': '69', 'cdm': '67', 'cm': '77',
             'rm': '81', 'lm': '81', 'cam': '82', 'cf': '85', 'rf': '85', 'lf': '85', 'rw': '82', 'lw': '82',
             'st': '89', 'traits': 'Power Header Long Shot Taker (CPU AI Only) Power Free-Kick', 'specialities': '',
             'base_id': '51', 'resource_id': '51', 'ps4_last': '', 'ps4_min': '', 'ps4_max': '', 'ps4_prp': '0',
             'xbox_last': '', 'xbox_min': '', 'xbox_max': '', 'xbox_prp': '0', 'pc_last': '', 'pc_min': '',
             'pc_max': '', 'pc_prp': '0'},
            {'futbin_id': '189', 'player_name': 'Shearer', 'player_extended_name': 'Alan Shearer',
             'quality': 'Gold - Rare', 'revision': 'Icon', 'origin': 'Medium', 'overall': '89', 'club': 'FUT 21 ICONS',
             'league': 'Icons', 'nationality': 'England', 'position': 'ST', 'age': '50', 'date_of_birth': '1970.08.13',
             'height': '182', 'weight': '76', 'intl_rep': '4', 'added_date': '2020.09.10', 'pace': '84',
             'pace_acceleration': '85', 'pace_sprint_speed': '83', 'dribbling': '78', 'drib_agility': '74',
             'drib_balance': '71', 'drib_reactions': '83', 'drib_ball_control': '81', 'drib_dribbling': '77',
             'drib_composure': '85', 'shooting': '90', 'shoot_positioning': '89', 'shoot_finishing': '92',
             'shoot_shot_power': '90', 'shoot_long_shots': '85', 'shoot_volleys': '90', 'shoot_penalties': '91',
             'passing': '75', 'pass_vision': '73', 'pass_crossing': '77', 'pass_free_kick': '83', 'pass_short': '80',
             'pass_long': '62', 'pass_curve': '80', 'defending': '48', 'def_interceptions': '40', 'def_heading': '91',
             'def_marking': '26', 'def_stand_tackle': '60', 'def_slid_tackle': '51', 'physicality': '84',
             'phys_jumping': '89', 'phys_stamina': '87', 'phys_strength': '85', 'phys_aggression': '77',
             'gk_diving': '', 'gk_reflexes': '', 'gk_handling': '', 'gk_speed': '', 'gk_kicking': '',
             'gk_positoning': '', 'pref_foot': 'Right', 'att_workrate': 'High', 'def_workrate': 'Med', 'weak_foot': '3',
             'skill_moves': '2', 'cb': '63', 'rb': '66', 'lb': '66', 'rwb': '68', 'lwb': '68', 'cdm': '64', 'cm': '75',
             'rm': '81', 'lm': '81', 'cam': '80', 'cf': '83', 'rf': '83', 'lf': '83', 'rw': '82', 'lw': '82',
             'st': '87', 'traits': 'Power Header Long Shot Taker (CPU AI)', 'specialities': '', 'base_id': '239598',
             'resource_id': '239598', 'ps4_last': '412000', 'ps4_min': '67000', 'ps4_max': '600000', 'ps4_prp': '64',
             'xbox_last': '446000', 'xbox_min': '67000', 'xbox_max': '750000', 'xbox_prp': '55', 'pc_last': '525000',
             'pc_min': '67000', 'pc_max': '900000', 'pc_prp': '54'},
            {'futbin_id': '190', 'player_name': 'Shearer', 'player_extended_name': 'Alan Shearer',
             'quality': 'Gold - Rare', 'revision': 'Icon', 'origin': 'Base', 'overall': '87', 'club': 'FUT 21 ICONS',
             'league': 'Icons', 'nationality': 'England', 'position': 'ST', 'age': '50', 'date_of_birth': '1970.08.13',
             'height': '182', 'weight': '78', 'intl_rep': '5', 'added_date': '2020.09.10', 'pace': '76',
             'pace_acceleration': '78', 'pace_sprint_speed': '75', 'dribbling': '76', 'drib_agility': '69',
             'drib_balance': '69', 'drib_reactions': '88', 'drib_ball_control': '80', 'drib_dribbling': '72',
             'drib_composure': '89', 'shooting': '88', 'shoot_positioning': '91', 'shoot_finishing': '90',
             'shoot_shot_power': '88', 'shoot_long_shots': '83', 'shoot_volleys': '87', 'shoot_penalties': '93',
             'passing': '76', 'pass_vision': '76', 'pass_crossing': '75', 'pass_free_kick': '86', 'pass_short': '80',
             'pass_long': '61', 'pass_curve': '79', 'defending': '53', 'def_interceptions': '44', 'def_heading': '91',
             'def_marking': '30', 'def_stand_tackle': '68', 'def_slid_tackle': '56', 'physicality': '84',
             'phys_jumping': '86', 'phys_stamina': '81', 'phys_strength': '87', 'phys_aggression': '82',
             'gk_diving': '', 'gk_reflexes': '', 'gk_handling': '', 'gk_speed': '', 'gk_kicking': '',
             'gk_positoning': '', 'pref_foot': 'Right', 'att_workrate': 'Med', 'def_workrate': 'Med', 'weak_foot': '3',
             'skill_moves': '2', 'cb': '66', 'rb': '67', 'lb': '67', 'rwb': '68', 'lwb': '68', 'cdm': '67', 'cm': '76',
             'rm': '79', 'lm': '79', 'cam': '79', 'cf': '82', 'rf': '82', 'lf': '82', 'rw': '80', 'lw': '80',
             'st': '85', 'traits': 'Power Header Long Shot Taker (CPU AI) Power Free-Kick', 'specialities': '',
             'base_id': '239599', 'resource_id': '239599', 'ps4_last': '250000', 'ps4_min': '65500',
             'ps4_max': '440000', 'ps4_prp': '49', 'xbox_last': '300000', 'xbox_min': '65500', 'xbox_max': '480000',
             'xbox_prp': '56', 'pc_last': '340000', 'pc_min': '65500', 'pc_max': '700000', 'pc_prp': '43'}])
        self.assertEqual(len(shearers_ids), 3)
        self.assertDictEqual(shearers_ids, {1: 51, 189: 239598, 190: 239599})

    def my_test2_user_props(self):
        self.assertEqual(len(self.user_owned_players_before_sell), 1)
        self.assertListEqual(self.user_owned_players_before_sell, [1])
        self.assertEqual(len(self.user_history_before_sell), 0)
        self.assertListEqual(self.user_history_before_sell, [])

    def my_test3_matched_shearer(self):
        shearer_matched = list_players.select_matching(self.shearer_futbin_ids, "owned_players")
        self.owned_shearer_id = sell.get_player_to_sell_id(shearer_matched)
        self.owned_players_without_shearer = sell.remove_from_owned(shearer_matched)
        self.assertEqual(shearer_matched.found_counter, 1)
        self.assertEqual(len(shearer_matched.at_ind), 1)
        self.assertDictEqual(shearer_matched.at_ind, {0: 1})
        self.assertEqual(self.owned_shearer_id, 1)
        self.assertEqual(len(self.owned_players_without_shearer), 0)
        self.assertListEqual(self.owned_players_without_shearer, [])

    def my_test4_http_methods_of_sell(self):
        patched_owned_players = sell.patch_owned(self.owned_players_without_shearer)
        advertised = sell.put_player_to_market(self.owned_shearer_id, 50000)
        self.assertEqual(patched_owned_players, True)
        self.assertEqual(advertised, True)

    def my_test5_shearer_on_market(self):
        shearer_is_on_market = request_try.try_request_get(vars.market_URL, {'seller_id': vars.user_id})
        self.assertEqual(shearer_is_on_market[0]['futbin_id'], '1')
        self.assertEqual(shearer_is_on_market[0]['id'], 1)
        self.assertEqual(shearer_is_on_market[0]['price'], 50000)
        self.assertEqual(shearer_is_on_market[0]['available'], "True")
        self.assertEqual(shearer_is_on_market[0]['seller_id'], 4)

    def my_test6_user_props_after_selling(self):
        user_after_sell = request_try.try_request_get(vars.users_URL, {'id': vars.user_id})
        user_owned_players_after_sell = user_after_sell[0]['owned_players']
        user_history_after_sell = user_after_sell[0]['history']
        self.assertEqual(len(user_owned_players_after_sell), 0)
        self.assertListEqual(user_owned_players_after_sell, [])
        self.assertEqual(len(user_history_after_sell), 0)
        self.assertListEqual(user_history_after_sell, [])

    def my_test7_try_selling_with_empty_reserved_team(self):
        selling_with_empty_reserve_team = sell.sell_player()
        self.assertEqual(selling_with_empty_reserve_team, False)

    def _steps(self):
        for name in dir(self):
            if name.startswith("my_test"):
                yield name, getattr(self, name)

    def test_steps(self, mock_cyan, mock_green, mock_info, mock_warning):
        for name, step in self._steps():
            try:
                step()
            except Exception as e:
                self.fail("{} failed ({}: {})".format(step, type(e), e))


@mock.patch("display.print_warning")
@mock.patch("display.print_info")
@mock.patch("display.print_info_green")
@mock.patch("display.print_info_cyan")
class BuyTestCases(unittest.TestCase):
    @mock.patch("request_try.try_request_get")
    def setUp(self, request_get) -> None:
        request_get.return_value = [{'futbin_id': '1', 'player_name': 'Shearer', 'player_extended_name': 'Alan Shearer',
                                     'quality': 'Gold - Rare', 'revision': 'Icon', 'origin': 'Prime', 'overall': '91',
                                     'club': 'FUT 21 ICONS', 'league': 'Icons', 'nationality': 'England',
                                     'position': 'ST', 'age': '50', 'date_of_birth': '1970.08.13', 'height': '182',
                                     'weight': '78', 'intl_rep': '5', 'added_date': '2020.09.10', 'pace': '81',
                                     'pace_acceleration': '82', 'pace_sprint_speed': '80', 'dribbling': '78',
                                     'drib_agility': '71', 'drib_balance': '71', 'drib_reactions': '87',
                                     'drib_ball_control': '82', 'drib_dribbling': '76', 'drib_composure': '88',
                                     'shooting': '93', 'shoot_positioning': '92', 'shoot_finishing': '95',
                                     'shoot_shot_power': '94', 'shoot_long_shots': '86', 'shoot_volleys': '93',
                                     'shoot_penalties': '94', 'passing': '77', 'pass_vision': '76',
                                     'pass_crossing': '77', 'pass_free_kick': '86', 'pass_short': '82',
                                     'pass_long': '63', 'pass_curve': '81', 'defending': '52',
                                     'def_interceptions': '44', 'def_heading': '94', 'def_marking': '28',
                                     'def_stand_tackle': '65', 'def_slid_tackle': '55', 'physicality': '85',
                                     'phys_jumping': '88', 'phys_stamina': '84', 'phys_strength': '88',
                                     'phys_aggression': '80', 'gk_diving': '', 'gk_reflexes': '',
                                     'gk_handling': '', 'gk_speed': '', 'gk_kicking': '',
                                     'gk_positoning': '', 'pref_foot': 'Right', 'att_workrate': 'High',
                                     'def_workrate': 'Med', 'weak_foot': '3', 'skill_moves': '2',
                                     'cb': '66', 'rb': '68', 'lb': '68', 'rwb': '69', 'lwb': '69', 'cdm': '67',
                                     'cm': '77', 'rm': '81', 'lm': '81', 'cam': '82', 'cf': '85', 'rf': '85',
                                     'lf': '85', 'rw': '82', 'lw': '82', 'st': '89',
                                     'traits': 'Power Header Long Shot Taker (CPU AI Only) Power Free-Kick',
                                     'specialities': '', 'base_id': '51', 'resource_id': '51', 'ps4_last': '',
                                     'ps4_min': '', 'ps4_max': '', 'ps4_prp': '0', 'xbox_last': '', 'xbox_min': '',
                                     'xbox_max': '', 'xbox_prp': '0', 'pc_last': '', 'pc_min': '', 'pc_max': '',
                                     'pc_prp': '0', 'price': 50000, 'seller_id': 4, 'expire': '02/05/2022 17:03:41',
                                     'available': 'True', 'id': 1}]
        self.market_players_buyer_pov = request_try.try_request_get(vars.market_URL, {})

    def my_test10_seller_props_before_sell(self):
        vars.user_id = 4
        seller = request_try.try_request_get(vars.users_URL, {'id': vars.user_id})
        seller_coins = seller[0]['coins']
        seller_history = seller[0]['history']
        seller_owned_players = seller[0]['owned_players']
        self.assertEqual(vars.user_id, 4)
        self.assertEqual(seller_coins, 100000)
        self.assertEqual(len(seller_history), 0)
        self.assertListEqual(seller_history, [])
        self.assertEqual(len(seller_owned_players), 0)
        self.assertListEqual(seller_owned_players, [])

    def my_test11_market_from_seller_pov(self):
        market_for_seller = request_try.try_request_get(vars.market_URL, {})
        market_hits = buy.buy_player({}, None, '10000')
        market_players_seller_pov = request_try.try_request_get(vars.market_URL, {})
        seller_selectable_ids = buy.filter_market_players(market_players_seller_pov, None, '100000')
        self.assertEqual(len(market_for_seller), 1)
        self.assertEqual(market_hits, False)
        self.assertEqual(len(seller_selectable_ids), 0)
        self.assertListEqual(seller_selectable_ids, [])

    def my_test12_buyer_props_before_buy(self):
        vars.user_id = 5
        buyer = request_try.try_request_get(vars.users_URL, {'id': vars.user_id})
        buyer_coins = buyer[0]['coins']
        buyer_history = buyer[0]['history']
        buyer_owned_players = buyer[0]['owned_players']
        self.assertEqual(vars.user_id, 5)
        self.assertEqual(buyer_coins, 100000)
        self.assertEqual(len(buyer_history), 0)
        self.assertListEqual(buyer_history, [])
        self.assertEqual(len(buyer_owned_players), 0)
        self.assertListEqual(buyer_owned_players, [])

    def my_test13_market_from_buyer_pov_before_buy(self):
        market_for_buyer = request_try.try_request_get(vars.market_URL, {})
        market_players_buyer_pov_real = request_try.try_request_get(vars.market_URL, {})
        buyer_filtered_market_players = buy.filter_market_players(market_players_buyer_pov_real, None, '100000')
        buyer_selectable_ids = buy.create_selectable_market_ids(buyer_filtered_market_players)
        self.assertEqual(len(market_for_buyer), 1)
        self.assertEqual(len(buyer_filtered_market_players), 1)
        self.assertEqual(len(buyer_selectable_ids), 1)
        self.assertListEqual(buyer_selectable_ids, [1])

    def my_test14_buy_buyer_pov_with_max_price_too_low(self):
        market_players_buyer_pov = request_try.try_request_get(vars.market_URL, {})
        # buyer_selectable_ids_with_max_price_too_low = buy.create_selectable_ids(self.market_players_buyer_pov, None, '10000')
        buyer_filtered_market_players_with_max_price_too_low = buy.filter_market_players(market_players_buyer_pov, None, '10000')
        buyer_selectable_ids_with_max_price_too_low = buy.create_selectable_market_ids(buyer_filtered_market_players_with_max_price_too_low)
        self.assertEqual(len(buyer_filtered_market_players_with_max_price_too_low), 0)
        self.assertEqual(buyer_filtered_market_players_with_max_price_too_low, [])
        self.assertEqual(len(buyer_selectable_ids_with_max_price_too_low), 0)
        self.assertListEqual(buyer_selectable_ids_with_max_price_too_low, [])

    def my_test15_buy_buyer_pov_with_max_price_high_enough(self):
        market_players_buyer_pov = request_try.try_request_get(vars.market_URL, {})
        # buyer_selectable_ids_with_max_price_high_enough = buy.create_selectable_ids(self.market_players_buyer_pov, None, '50000')
        buyer_filtered_market_players_with_max_price_high_enough = buy.filter_market_players(market_players_buyer_pov, None, '50000')
        buyer_selectable_ids_with_max_price_high_enough = buy.create_selectable_market_ids(buyer_filtered_market_players_with_max_price_high_enough)
        self.assertEqual(len(buyer_filtered_market_players_with_max_price_high_enough), 1)
        self.assertEqual(buyer_filtered_market_players_with_max_price_high_enough[0]['id'], 1)
        self.assertEqual(len(buyer_selectable_ids_with_max_price_high_enough), 1)
        self.assertListEqual(buyer_selectable_ids_with_max_price_high_enough, [1])

    def my_test16_buy_buyer_pov_with_min_price_too_high(self):
        market_players_buyer_pov = request_try.try_request_get(vars.market_URL, {})
        # buyer_selectable_ids_with_min_price_too_high = buy.create_selectable_ids(self.market_players_buyer_pov, '70000', None)
        buyer_filtered_market_players_with_min_price_too_high = buy.filter_market_players(market_players_buyer_pov, '70000', None)
        buyer_selectable_ids_with_min_price_too_high = buy.create_selectable_market_ids(buyer_filtered_market_players_with_min_price_too_high)
        self.assertEqual(len(buyer_filtered_market_players_with_min_price_too_high), 0)
        self.assertEqual(buyer_filtered_market_players_with_min_price_too_high, [])
        self.assertEqual(len(buyer_selectable_ids_with_min_price_too_high), 0)
        self.assertListEqual(buyer_selectable_ids_with_min_price_too_high, [])

    def my_test17_buy_buyer_pov_with_min_price_low_enough(self):
        market_players_buyer_pov = request_try.try_request_get(vars.market_URL, {})
        # buyer_selectable_ids_with_min_price_low_enough = buy.create_selectable_ids(self.market_players_buyer_pov, '20000', None)
        buyer_filtered_market_players_with_min_price_low_enough = buy.filter_market_players(market_players_buyer_pov, '20000', None)
        buyer_selectable_ids_with_in_price_low_enough = buy.create_selectable_market_ids(buyer_filtered_market_players_with_min_price_low_enough)
        self.assertEqual(len(buyer_filtered_market_players_with_min_price_low_enough), 1)
        self.assertEqual(buyer_filtered_market_players_with_min_price_low_enough[0]['id'], 1)
        self.assertEqual(len(buyer_selectable_ids_with_in_price_low_enough), 1)
        self.assertListEqual(buyer_selectable_ids_with_in_price_low_enough, [1])

    def my_test18_buy_buyer_pov_with_min_and_max_wrong(self):
        market_players_buyer_pov = request_try.try_request_get(vars.market_URL, {})
        # buyer_selectable_ids_with_min_and_max_wrong = buy.create_selectable_ids(self.market_players_buyer_pov, '70000', '100000')
        buyer_filtered_market_players_with_min_and_max_wrong = buy.filter_market_players(market_players_buyer_pov, '70000', '100000')
        buyer_selectable_ids_with_min_and_max_wrong = buy.create_selectable_market_ids(buyer_filtered_market_players_with_min_and_max_wrong)
        self.assertEqual(len(buyer_filtered_market_players_with_min_and_max_wrong), 0)
        self.assertEqual(buyer_filtered_market_players_with_min_and_max_wrong, [])
        self.assertEqual(len(buyer_selectable_ids_with_min_and_max_wrong), 0)
        self.assertListEqual(buyer_selectable_ids_with_min_and_max_wrong, [])

    def my_test19_buy_buyer_pov_with_min_and_max_good(self):
        market_players_buyer_pov = request_try.try_request_get(vars.market_URL, {})
        # buyer_selectable_ids_with_min_and_max_good = buy.create_selectable_ids(self.market_players_buyer_pov, '30000', '60000')
        buyer_filtered_market_players_with_min_and_max_good = buy.filter_market_players(market_players_buyer_pov, '30000', '60000')
        buyer_selectable_ids_with_min_and_max_good = buy.create_selectable_market_ids(buyer_filtered_market_players_with_min_and_max_good)
        self.assertEqual(len(buyer_filtered_market_players_with_min_and_max_good), 1)
        self.assertEqual(buyer_filtered_market_players_with_min_and_max_good[0]['id'], 1)
        self.assertEqual(len(buyer_selectable_ids_with_min_and_max_good), 1)
        self.assertListEqual(buyer_selectable_ids_with_min_and_max_good, [1])

    def my_test20_buying_player_with_market_id_1(self):
        vars.user_id = 5
        vars.users_id_url = "http://localhost:3000/Users/5"
        player_bought_with_buyable_check = buy.buyable_check('1')
        self.assertEqual(player_bought_with_buyable_check, True)

    def my_test21_buyer_props_after_buying_player(self):
        vars.user_id = 5
        buyer = request_try.try_request_get(vars.users_URL, {'id': vars.user_id})
        buyer_coins = buyer[0]['coins']
        buyer_history = buyer[0]['history']
        buyer_owned_players = buyer[0]['owned_players']
        self.assertEqual(vars.user_id, 5)
        self.assertEqual(buyer_coins, 50000)
        self.assertEqual(len(buyer_history), 1)
        self.assertListEqual(buyer_history, [1])
        self.assertEqual(len(buyer_owned_players), 1)
        self.assertListEqual(buyer_owned_players, [1])

    def my_test22_market_from_buyer_pov_after_buy(self):
        market_for_buyer = request_try.try_request_get(vars.market_URL, {})
        market_players_buyer_pov_real = request_try.try_request_get(vars.market_URL, {})
        buyer_filtered_market_players = buy.filter_market_players(market_players_buyer_pov_real, None, '100000')
        buyer_selectable_ids = buy.create_selectable_market_ids(buyer_filtered_market_players)
        self.assertEqual(len(market_for_buyer), 1)
        self.assertEqual(len(buyer_filtered_market_players), 0)
        self.assertEqual(len(buyer_selectable_ids), 0)
        self.assertListEqual(buyer_selectable_ids, [])

    def my_test23_seller_props_after_sell(self):
        vars.user_id = 4
        seller = request_try.try_request_get(vars.users_URL, {'id': vars.user_id})
        seller_coins = seller[0]['coins']
        seller_history = seller[0]['history']
        seller_owned_players = seller[0]['owned_players']
        self.assertEqual(vars.user_id, 4)
        self.assertEqual(seller_coins, 150000)
        self.assertEqual(len(seller_history), 0)
        self.assertListEqual(seller_history, [])
        self.assertEqual(len(seller_owned_players), 0)
        self.assertListEqual(seller_owned_players, [])


    def _steps(self):
        for name in dir(self):
            if name.startswith("my_test"):
                yield name, getattr(self, name)

    def test_steps(self, mock_cyan, mock_green, mock_info, mock_warning):
        for name, step in self._steps():
            try:
                step()
            except Exception as e:
                self.fail("{} failed ({}: {})".format(step, type(e), e))


@mock.patch("display.print_warning")
@mock.patch("display.print_info")
@mock.patch("display.print_info_green")
@mock.patch("display.print_info_cyan")
@mock.patch("display.show_history")
class HistoryTestCases(unittest.TestCase):
    def test_get_buyer_history(self, show_history, mock_cyan, mock_green, mock_info, mock_warning):
        vars.user_id = 5
        vars.users_id_url = "http://localhost:3000/Users/5"
        buyer_got_history = market_checker.market_check()
        self.assertEqual(buyer_got_history, True)

    def test_get_seller_history(self, show_history, mock_cyan, mock_green, mock_info, mock_warning):
        vars.user_id = 4
        vars.users_id_url = "http://localhost:3000/Users/4"
        seller_got_history = market_checker.market_check()
        self.assertEqual(seller_got_history, True)

    def test_outsider_history(self, show_history, mock_cyan, mock_green, mock_info, mock_warning):
        vars.user_id = 1
        vars.users_id_url = "http://localhost:3000/Users/1"
        outsider_got_history = market_checker.market_check()
        self.assertEqual(outsider_got_history, False)

if __name__ == '__main__':
    unittest.main()
