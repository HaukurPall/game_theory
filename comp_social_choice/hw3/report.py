from comp_social_choice.hw3.manipulability import Preference, Profile, BordaRule, PluralityRule
import matplotlib.pyplot as plt

def plot_line_graph(x, y, y_name, x_name):
    """
    Helper function
    """
    plt.plot(x, y)
    plt.ylabel(y_name)
    plt.xlabel(x_name)
    #plt.xscale('log')
    plt.savefig(x_name + y_name + '.png')
    plt.clf()

def generate_profiles(number_of_voters=10, number_of_candidates=3, number_of_profiles=10):
    profiles = []
    for profile in range(0, number_of_profiles):
        profiles.append(Profile.generate_random_profile(number_of_voters, number_of_candidates))
    return profiles

def main():
    profiles = generate_profiles()
    plurality_rule = PluralityRule()
    borda_rule = BordaRule()
    for profile in profiles:
        if profile.is_manipulable(plurality_rule):
            print("Can manipulate")
            print(profile)
        if profile.is_manipulable(borda_rule):
            print("Can manipulate")
            print(profile)

if __name__ == "__main__":
    main()
