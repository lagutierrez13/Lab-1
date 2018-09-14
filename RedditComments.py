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
    print("-----------------List of over 50% probable negative comments-----------------")
    print(neg, "\n")
    print("-----------------List of over 50% probable positive comments-----------------")
    print(pos, "\n")
    print("-----------------List of over 50% probable neutral comments------------------")
    print(neu, "\n")


def main():
    # create lists that will be populated with corresponding comments
    pos_list = []
    neg_list = []
    neu_list = []

    reply = get_submission_comments(
        'https://www.reddit.com/r/gifs/comments/9f0ik8/i_added_effects_to_thor_and_spidermans_brutal/')

    # populate the negative, positive, and neutral lists with corresponding comments
    process_comments(reply, neg_list, pos_list, neu_list)

    # print negative, positive, and neutral lists
    print_lists_with_comments(neg_list, pos_list, neu_list)


main()
