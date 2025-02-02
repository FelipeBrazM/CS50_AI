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
    """
    num_pages = len(corpus)
    probabilities = {}
    
    if corpus[page]:
        # Pages linked from the current page
        linked_pages = corpus[page]
        num_links = len(linked_pages)
        
        for p in corpus:
            probabilities[p] = (1 - damping_factor) / num_pages
            if p in linked_pages:
                probabilities[p] += damping_factor / num_links
    else:
        # If no outgoing links, distribute equally among all pages
        for p in corpus:
            probabilities[p] = 1 / num_pages

    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.
    """
    page_rank = {page: 0 for page in corpus}
    pages = list(corpus.keys())
    
    # Start with a random page
    current_page = random.choice(pages)
    page_rank[current_page] += 1

    for _ in range(n - 1):
        probabilities = transition_model(corpus, current_page, damping_factor)
        next_page = random.choices(pages, weights=probabilities.values(), k=1)[0]
        page_rank[next_page] += 1
        current_page = next_page

    # Normalize to ensure the sum of PageRanks is 1
    total_samples = sum(page_rank.values())
    for page in page_rank:
        page_rank[page] /= total_samples

    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.
    """
    num_pages = len(corpus)
    page_rank = {page: 1 / num_pages for page in corpus}
    new_rank = page_rank.copy()
    
    while True:
        for page in corpus:
            rank_sum = 0
            for possible_page in corpus:
                # Consider all pages linking to the current page
                if page in corpus[possible_page]:
                    rank_sum += page_rank[possible_page] / len(corpus[possible_page])
                elif not corpus[possible_page]:  # Handle pages with no outgoing links
                    rank_sum += page_rank[possible_page] / num_pages
            
            new_rank[page] = (1 - damping_factor) / num_pages + damping_factor * rank_sum
        
        # Check for convergence
        if all(abs(new_rank[page] - page_rank[page]) < 0.001 for page in page_rank):
            break
        
        page_rank = new_rank.copy()

    # Normalize to ensure the sum of PageRanks is 1
    total_rank = sum(new_rank.values())
    for page in new_rank:
        new_rank[page] /= total_rank

    return new_rank


if __name__ == "__main__":
    main()
