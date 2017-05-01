from comp_social_choice.hw3.manipulability import Preference, Profile, BordaRule, PluralityRule, CopelandRule
import matplotlib.pyplot as plt


def plot_line_graph(x, y, y_name, x_name):
    """
    Helper function
    """
    plt.plot(x, y)
    plt.ylabel(y_name)
    plt.xlabel(x_name)
    # plt.xscale('log')
    plt.savefig(x_name + y_name + '.png')
    plt.clf()


def generate_profiles(number_of_voters=10, number_of_candidates=3, number_of_profiles=10):
    profiles = []
    for profile in range(0, number_of_profiles):
        profiles.append(Profile.generate_random_profile(number_of_voters, number_of_candidates))
    return profiles


def main():
    profiles = generate_profiles(1000, 6, 100)
    plurality_rule = PluralityRule()
    borda_rule = BordaRule()
    copeland_rule = CopelandRule()
    counter = [0,0,0]
    for profile in profiles:
        if profile.is_manipulable(plurality_rule):
            counter[0] += 1
        if profile.is_manipulable(borda_rule):
            counter[1] += 1
        if profile.is_manipulable(copeland_rule):
            counter[2] += 1
    print(counter)


if __name__ == "__main__":
    main()
