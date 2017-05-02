# Authors: Haukur Pall Jonsson, Silvan Hungerbuhler, Max Rapp
# Date: 29th April 2017
import copy
import random
import unittest
import itertools

random.seed(673567)  # we set the seed for debugging


class Preference:
    """
    :param list_of_preferences: orderer list of integers, in which integer is a unique candidate, first candidate is 0
    """

    def __init__(self, preference_order):
        self.preference_order = preference_order
        self.number_of_candidates = len(preference_order)

    def __eq__(self, other):
        return self.preference_order == other.preference_order

    def __getitem__(self, index):
        return self.preference_order[index]

    """
    Generates a random preference order over a uniform distribution.
    """
    @staticmethod
    def generate_random_preference_order(m):
        preference_set = set([x for x in range(0, m)])
        preference_list = random.sample(preference_set, m)
        return Preference(preference_list)

    """
    Returns True if x is more preferred than y
    """
    def is_x_more_preferred_than_y(self, x, y):
        return self.preference_order.index(x) < self.preference_order.index(y)

    """
    Returns a new preference order in which x has been placed first
    """
    def place_x_first(self, x):
        old_order = copy.deepcopy(self.preference_order)
        old_order.remove(x)
        return Preference([x] + old_order)

    """
    Returns a new preference order in which x has been placed last
    """
    def place_x_last(self, x):
        old_order = copy.deepcopy(self.preference_order)
        old_order.remove(x)
        return Preference(old_order + [x])

    """
    Returns a new preference order in which the list of preference order has been placed last
    """
    def place_preferences_last(self, list_of_preferences):
        old_order = copy.deepcopy(self.preference_order)
        for preference in list_of_preferences:
            old_order.remove(preference)
        return Preference(old_order + list_of_preferences)

    def get_copy(self):
        order = copy.deepcopy(self.preference_order)
        return Preference(order)

    def get_first_candidate(self):
        return self.preference_order[0]

    def get_number_of_candidates(self):
        return self.number_of_candidates

    def __str__(self):
        return str(self.preference_order)


class Profile:
    def __init__(self, list_of_preferences):
        self.list_of_preferences = list_of_preferences
        self.number_of_voters = len(list_of_preferences)

    def __str__(self):
        profile = ""
        for preference_order_index, preference_order in enumerate(self.list_of_preferences):
            profile += str(preference_order) + "\n"
        return profile

    def __getitem__(self, index):
        return self.list_of_preferences[index]

    """
    Generate a random profile with n voters and m alternatives
    """
    @staticmethod
    def generate_random_profile(n, m):
        list_of_preferences = []
        for voter in range(0, n):
            list_of_preferences.append(Preference.generate_random_preference_order(m))
        return Profile(list_of_preferences)

    def get_number_of_candidates(self):
        return self.list_of_preferences[0].get_number_of_candidates()

    """
    Returns True if profile is manipulable with given voting rule
    """
    def is_manipulable(self, voting_rule):
        scores = voting_rule.calculate_scores(self)

        winners = voting_rule.get_winners(scores)
        possible_winners = voting_rule.get_possible_winners(scores, self.get_number_of_candidates())
        winner, tie_losers = voting_rule.break_ties(winners)
        # the other winners can be made to win
        possible_winners.extend(tie_losers)
        if len(possible_winners) == 0:
            return False
        for preference_order_index, preference_order in enumerate(self.list_of_preferences):
            for should_be_winner in possible_winners:
                # if this voter wants this candidate to win
                if preference_order.is_x_more_preferred_than_y(should_be_winner, winner):
                    possible_winners_excluding_current_one = copy.deepcopy(possible_winners)
                    possible_winners_excluding_current_one.remove(should_be_winner)
                    # can the voting rule manipulate this preference order s.t. the should_be_winner wins?
                    new_preference_order, success = voting_rule.manipulate_order(preference_order,
                                                                                 preference_order_index,
                                                                                 winner,
                                                                                 should_be_winner,
                                                                                 possible_winners_excluding_current_one,
                                                                                 self)
                    # if we were not successful in manipulation we continue
                    if not success:
                        continue
                    # we verify that the winner is no longer a winner
                    new_profile = self.manipulate_preference_order(preference_order_index, new_preference_order)
                    new_scores = voting_rule.calculate_scores(new_profile)
                    new_winners = voting_rule.get_winners(new_scores)
                    # Sanity check
                    if should_be_winner not in new_winners:
                        print(str(should_be_winner) + " should have won, but did not")
                        print("Old profile:")
                        print(self)
                        print("Old scores:")
                        print(scores)
                        print("New profile")
                        print(new_profile)
                        print("New scores:")
                        print(new_scores)
                        raise Exception("Should be winner not in new winners!")
                    return True

    """
    Return new profile in which we have swapped out preference order of voter i with a new_preference_order
    """
    def manipulate_preference_order(self, i, new_preference_order):
        new_list = copy.deepcopy(self.list_of_preferences)
        new_list[i] = new_preference_order
        return Profile(new_list)


class VotingRule:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def get_number(self):
        pass

    """
    Return a list of scores for the candidates
    """
    def calculate_scores(self, profile):
        pass

    """
    Returns a list of possible winners, the candidates with scores in a 'striking distance' of the winners
    """
    def get_possible_winners(self, candidate_scores, m):
        pass

    """
    Returns True and a new preference order if we can manupulate the preference order s.t. our possible winner wins,
    False and the old preference order if it cannot
    """
    def manipulate_order(self, preference_order, order_index, winner, candidate_which_should_win, possible_winners, profile):
        pass

    """
    Returns a list of winners, the candidates which have the highest scores
    """
    @staticmethod
    def get_winners(candidate_scores):
        winners = []
        max_score = max(candidate_scores)
        for index, score in enumerate(candidate_scores):
            if score == max_score:
                winners.append(index)
        return winners

    """
    Returns a winner using a tiebreaker (lexicographically)
    """
    @staticmethod
    def break_ties(winners):
        first_winner = min(winners)
        tie_losers = copy.deepcopy(winners)
        tie_losers.remove(first_winner)
        return first_winner, tie_losers


class PluralityRule(VotingRule):
    def __init__(self):
        super().__init__("Plurality rule")

    def get_number(self):
        return 0

    def calculate_scores(self, profile):
        candidate_scores = [0 for x in range(0, profile.get_number_of_candidates())]
        for preference_order in profile:
            candidate = preference_order.get_first_candidate()
            candidate_scores[candidate] += 1

        return candidate_scores

    def get_possible_winners(self, candidate_scores, m):
        # This essentially calucaltes "marging of victory"
        possible_winners = []
        max_score = max(candidate_scores)
        possible_winner_score = max_score - 1
        for index, score in enumerate(candidate_scores):
            if score == possible_winner_score:
                possible_winners.append(index)
        return possible_winners

    def manipulate_order(self, preference_order, order_index, winner, candidate_which_should_win, possible_winners, profile):
        # if the candidate which we like the best is already at the top there is nothing we can do
        if preference_order.get_first_candidate() == candidate_which_should_win:
            return preference_order, False
        new_preference = preference_order.place_x_first(candidate_which_should_win).place_x_last(winner)
        if new_preference == preference_order:
            return preference_order, False
        else:
            return new_preference, True


class BordaRule(VotingRule):
    def __init__(self):
        super().__init__("Borda rule")

    def get_number(self):
        return 1

    def calculate_scores(self, profile):
        candidate_scores = [0 for x in range(0, profile.get_number_of_candidates())]
        for preference_order in profile:
            score = profile.get_number_of_candidates() - 1
            for candidate in preference_order:
                candidate_scores[candidate] += score
                score -= 1

        return candidate_scores

    def get_possible_winners(self, candidate_scores, m):
        possible_winners = []
        max_score = max(candidate_scores)
        possible_winner_score = max_score - (m - 2)
        for index, score in enumerate(candidate_scores):
            if score >= possible_winner_score and score != max_score:
                possible_winners.append(index)
        return possible_winners

    def manipulate_order(self, preference_order, order_index, winner, candidate_which_should_win, possible_winners, profile):
        # we put candidates which have no chance winning at the top to begin with
        new_preference = preference_order.get_copy()
        for candidate in new_preference:
            if candidate not in possible_winners and candidate != winner:
                new_preference = new_preference.place_x_first(candidate)

        new_preference = new_preference.place_x_first(candidate_which_should_win)
        # now we need to check if our possible winner wins. We go through each permutation of possible winners at the bottom
        for permutation in list(itertools.permutations(possible_winners)):
            new_preference = new_preference.place_preferences_last(list(permutation))
            new_profile = profile.manipulate_preference_order(order_index, new_preference)
            scores = self.calculate_scores(new_profile)
            winners = self.get_winners(scores)
            # if we have successfully made our candidate win
            if candidate_which_should_win in winners:
                return new_preference, True
        return preference_order, False


class CopelandRule(VotingRule):
    def __init__(self):
        super().__init__("Copeland Rule")

    def get_number(self):
        return 2

    def calculate_scores(self, profile):
        candidate_scores = [0 for x in range(0, profile.get_number_of_candidates())]
        for preference_order in profile:
            score = profile.get_number_of_candidates() - 1
            for candidate in preference_order:
                candidate_scores[candidate] += score
                score -= 2

        return candidate_scores

    def get_possible_winners(self, candidate_scores, m):
        possible_winners = []
        max_score = max(candidate_scores)
        possible_winner_score = max_score - 2*(m - 2)
        for index, score in enumerate(candidate_scores):
            if score >= possible_winner_score and score != max_score:
                possible_winners.append(index)
        return possible_winners

    def manipulate_order(self, preference_order, order_index, winner, candidate_which_should_win, possible_winners, profile):
        # we put candidates which have no chance winning at the top to begin with
        new_preference = preference_order.get_copy()
        for candidate in new_preference:
            if candidate not in possible_winners and candidate != winner:
                new_preference = new_preference.place_x_first(candidate)

        new_preference = new_preference.place_x_first(candidate_which_should_win)
        # now we need to check if our possible winner wins for each permutation of possible winners at the bottom
        for permutation in list(itertools.permutations(possible_winners)):
            new_preference = new_preference.place_preferences_last(list(permutation))
            new_profile = profile.manipulate_preference_order(order_index, new_preference)
            scores = self.calculate_scores(new_profile)
            winners = self.get_winners(scores)
            # if we have successfully made the winner lose and our candidate win
            if candidate_which_should_win in winners:
                return new_preference, True
        return preference_order, False


class Tests(unittest.TestCase):

    def test_2x2(self):
        profile = Profile([
            Preference([1, 0]),
            Preference([0, 1])])
        plurality_rule = PluralityRule()
        borda_rule = BordaRule()
        copeland_rule = CopelandRule()
        self.assertFalse(profile.is_manipulable(plurality_rule))
        self.assertFalse(profile.is_manipulable(borda_rule))
        self.assertFalse(profile.is_manipulable(copeland_rule))

    def test_3x3(self):
        profile = Profile([
            Preference([2, 1, 0]),
            Preference([0, 2, 1]),
            Preference([1, 0, 2])])
        plurality_rule = PluralityRule()
        borda_rule = BordaRule()
        copeland_rule = CopelandRule()
        self.assertTrue(profile.is_manipulable(plurality_rule))
        self.assertTrue(profile.is_manipulable(borda_rule))
        self.assertTrue(profile.is_manipulable(copeland_rule))


def generate_profiles(number_of_voters=10, number_of_candidates=3, number_of_profiles=10):
    profiles = []
    for profile in range(0, number_of_profiles):
        profiles.append(Profile.generate_random_profile(number_of_voters, number_of_candidates))
    return profiles


def main():
    number_of_candidates = 6
    number_of_profiles = 100
    number_of_voters = 10
    plurality_rule = PluralityRule()
    borda_rule = BordaRule()
    copeland_rule = CopelandRule()
    with open("data.txt", "a") as file:
        file.write("rule, voters, candidates, manipulable\n")
        while number_of_voters <= 1000:
            profiles = generate_profiles(number_of_voters, number_of_candidates, number_of_profiles)
            for profile in profiles:
                if profile.is_manipulable(plurality_rule):
                    file.write(str(plurality_rule) + " " + str(number_of_voters) + " " + str(number_of_candidates) + " " + "1")
                else:
                    file.write(str(plurality_rule) + " " + str(number_of_voters) + " " + str(number_of_candidates) + " " + "0")
                file.write("\n")
                if profile.is_manipulable(borda_rule):
                    file.write(str(borda_rule) + " " + str(number_of_voters) + " " + str(number_of_candidates) + " " + "1")
                else:
                    file.write(str(borda_rule) + " " + str(number_of_voters) + " " + str(number_of_candidates) + " " + "0")
                file.write("\n")
                if profile.is_manipulable(copeland_rule):
                    file.write(str(copeland_rule) + " " + str(number_of_voters) + " " + str(number_of_candidates) + " " + "1")
                else:
                    file.write(str(copeland_rule) + " " + str(number_of_voters) + " " + str(number_of_candidates) + " " + "0")
                file.write("\n")
            number_of_voters += 10

if __name__ == "__main__":
    unittest.main()
    main()