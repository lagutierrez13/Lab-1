import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw

reddit = praw.Reddit(client_id='fRSSC1MxeUllpQ',
                     client_secret='l0P3flPXhhlZhDyAALdRjoBbu5Q',
                     user_agent='Luisgtzh'
                     )

nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()


def get_text_negative_prob(text):
    return sid.polarity_scores(text)['neg']


def get_text_neutral_prob(text):
    return sid.polarity_scores(text)['neu']


def get_text_positive_prob(text):
    return sid.polarity_scores(text)['pos']


def get_submission_comments(url):
    submission = reddit.submission(url=url)
    submission.comments.replace_more()

    return submission.comments


# method of getting all comments without recursion
def process_comments(comments, neg, pos, neu):
    for comment in comments:  # for loop to traverse comments within the same level
        if len(comment.replies) > 0:  # if comment has a reply
            process_comments(comment.replies, neg, pos, neu)  # recursive call on the comment's reply
        if get_text_negative_prob(comment.body) > 0.5:  # if comment is over 50% negative add to negatives list
            neg.append(comment.body)
        elif get_text_positive_prob(comment.body) > 0.5:  # if comment is over 50% negative add to negatives list
            pos.append(comment.body)
        elif get_text_neutral_prob(comment.body) > 0.5:  # if comment is over 50% negative add to negatives list
            neu.append(comment.body)
    return


# method that prints the lists containing the negative, positive, and neutral comments
def print_lists_with_comments(neg, pos, neu):
    print("-----------------------------NEW SUBMISSION POST-----------------------------")
    print("-----------------List of over 50% probable negative comments-----------------")
    print(neg, "\n")
    print("-----------------List of over 50% probable positive comments-----------------")
    print(pos, "\n")
    print("-----------------List of over 50% probable neutral comments------------------")
    print(neu, "\n")


def main():
    # first reddit post submission
    reply = get_submission_comments(
        'https://www.reddit.com/r/gifs/comments/9f0ik8/i_added_effects_to_thor_and_spidermans_brutal/')

    # create lists that will be populated with corresponding comments
    pos_list = []
    neg_list = []
    neu_list = []

    # populate the negative, positive, and neutral lists with corresponding comments
    process_comments(reply, neg_list, pos_list, neu_list)

    # print negative, positive, and neutral lists
    print_lists_with_comments(neg_list, pos_list, neu_list)

    # -------------------------------------------------------------------------------------
    # different submission for testing purposes
    reply_2 = get_submission_comments(
        'https://www.reddit.com/r/funny/comments/9fnsix/my_friend_is_apparently_allergic_to_hair_dye/')

    # create lists that will be populated with corresponding comments
    pos_list_2 = []
    neg_list_2 = []
    neu_list_2 = []

    # populate the negative, positive, and neutral lists with corresponding comments
    process_comments(reply_2, neg_list_2, pos_list_2, neu_list_2)

    # print negative, positive, and neutral lists
    print_lists_with_comments(neg_list_2, pos_list_2, neu_list_2)

    # -------------------------------------------------------------------------------------
    # different submission for testing purposes (2 comments on post)
    reply_3 = get_submission_comments(
        'https://www.reddit.com/r/CrossStitch/comments/9fn5vd/fo_quick_cross_stitch_i_did_for_a_coworkers_going/')

    # create lists that will be populated with corresponding comments
    pos_list_3 = []
    neg_list_3 = []
    neu_list_3 = []

    # populate the negative, positive, and neutral lists with corresponding comments
    process_comments(reply_3, neg_list_3, pos_list_3, neu_list_3)

    # print negative, positive, and neutral lists
    print_lists_with_comments(neg_list_3, pos_list_3, neu_list_3)


main()
