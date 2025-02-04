import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # Probabilities of going to the next page
    page_probabilities = {}

    # Checking if a page has outgoing links
    if corpus[page]:

        # Calculating probability for next pages
        next_page_probability = damping_factor/len(corpus[page])
        all_possible_pages_probability = (1 - damping_factor)/len(corpus)
        probability = next_page_probability + all_possible_pages_probability

        # Adding page and respective probability to dictionary
        page_probabilities[page] = all_possible_pages_probability
        for next_page in corpus[page]:
            page_probabilities[next_page] = probability

    else:

        # Calculating probability for next pages
        next_page_probability = 1/len(corpus)

        # Adding page and respective probability to dictionary
        for next_page in corpus:
            page_probabilities[next_page] = next_page_probability

    return page_probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Generating first sample page randomly and calculate it's transition model
    random_page = next(iter(random.sample(list(corpus), 1)))
    next_page_model = transition_model(corpus, random_page, damping_factor)

    # Randomly selects the next page to add to the samples, based on the transition model of the previous page
    samples = [random_page]
    page_ranks = {
        random_page: 1 / n
    }
    while len(samples) < n:
        next_page = random.choices(list(next_page_model.keys()), weights=next_page_model.values(), k=1)[0]
        samples.append(next_page)
        next_page_model = transition_model(corpus, next_page, damping_factor)

        # Updating the page's respective PageRank
        if next_page in page_ranks:
            page_ranks[next_page] += 1 / n
        else:
            page_ranks[next_page] = 1 / n

    return page_ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Initialy setting every page's PageRank to 1 / n
    n = len(corpus)
    page_ranks, previous_page_ranks = {}, {}
    for page in corpus:
        page_ranks[page], previous_page_ranks[page] = 1 / n, 1 / n

    # Constantly iterating until the previouse and current PageRanks differ by less than 0.001 or converge
    first_iteration = True
    while any(abs(previous_page_ranks[page] - page_ranks[page]) > 0.001 for page in previous_page_ranks) or first_iteration:
        first_iteration = False
        previous_page_ranks = page_ranks.copy()

        # Using the PageRank formula to calculate PageRank for every page in the corpus
        for page in page_ranks:
            next_links = []
            for link in corpus:
                if page in corpus[link] or len(corpus[link]) == 0:
                    next_links.append(link)

            iteration_sum = 0
            for link in next_links:
                numlinks = n
                if len(corpus[link]) != 0:
                    numlinks = len(corpus[link])

                iteration_sum += previous_page_ranks[link] / numlinks

            page_ranks[page] = ((1 - damping_factor) / n) + (damping_factor * iteration_sum)


    return page_ranks

if __name__ == "__main__":
    main()
