import argparse
import sys
from string_algorithms.trie import Trie
from collections import deque, Counter
import re
from itertools import islice
from typing import List


def build_trie(words: List[str]) -> Trie:
    trie = Trie()

    for word in words:
        trie.add(word)

    return trie


def load_dictionary(dict_fname: str) -> List[str]:
    with open(dict_fname) as f:
        return list(map(lambda word: word.strip().lower(), f.readlines()))


def filter_dictionary(
    words: List[str], letters: str, wildcard=None, use_all_letters=True, prefix=None
) -> List[str]:
    letters = sorted(letters)
    letter_set = set(letters)
    num_wildcards = 0 if wildcard is None else letters.count(wildcard)

    def is_valid_word_without_prefix(word):
        if len(word) > len(letters):
            return False
        if use_all_letters and len(word) != len(letters):
            return False
        if len(set(word) - letter_set) > num_wildcards:
            return False
        if not wildcard and use_all_letters and sorted(word) != letters:
            return False
        return True

    def is_valid_word(word):
        if prefix:
            if not word.startswith(prefix):
                return False
            word = word[len(prefix) :]
        return is_valid_word_without_prefix(word)

    return list(filter(is_valid_word, words))


def find_permutations(
    word: str,
    trie: Trie,
    prefix=None,
    use_all_letters: bool = True,
    wildcard: str = None,
    limit: int = None,
) -> List[str]:
    root = trie.get_node(prefix) if prefix else trie.root
    letters = Counter(word)
    q = deque([(root, "", letters)])
    words = []

    while len(q):
        node, w, l = q.popleft()

        if wildcard is None or l[wildcard] == 0:
            subnodes = sorted(
                filter(lambda item: l[item[0]] > 0, node.children.items())
            )
        else:
            subnodes = sorted(node.children.items())
        for c, subnode in subnodes:
            if limit is None or limit > 0:
                new_w = w + c
                if (not use_all_letters or len(new_w) == len(word)) and subnode.is_word:
                    words.append(new_w)
                    if limit is not None:
                        limit -= 1
                new_l = l - Counter(c) if l[c] > 0 else l - Counter(wildcard)
                q.append((subnode, new_w, new_l))
    return [f"{prefix}{w}" for w in words] if prefix else words


def find_regex(regex: str, words: List[str], limit: int = None) -> List[str]:
    pattern = re.compile(regex)
    words = filter(lambda w: pattern.match(w), words)
    if limit:
        return list(islice(words, limit))
    return list(words)


def _print_list(words: List[str]):
    for word in words:
        print(word)


def answer(word: str, trie: Trie, words: List[str], args, is_filtered=False):
    word = word.lower()
    if args.regex:
        result = find_regex(word, words, limit=args.limit)
    else:
        if is_filtered and not args.allow_shorter and not args.wildcard:
            if not args.limit:
                result = words
            else:
                result = words[: args.limit]
        else:
            result = find_permutations(
                word,
                trie,
                prefix=args.prefix,
                use_all_letters=not args.allow_shorter,
                wildcard=args.wildcard,
                limit=args.limit,
            )
    _print_list(result)


def main():
    parser = argparse.ArgumentParser(description="Scrabbler")
    parser.add_argument("word", type=str, nargs="?", help="Input word")
    parser.add_argument(
        "-d", "--dictionary", type=str, required=True, help="Dictironary to search."
    )
    parser.add_argument(
        "-l", "--limit", type=int, help="Limit the number of words printed."
    )
    parser.add_argument(
        "--prefix",
        type=str,
        help="Only print words starting with the specified prefix.",
    )
    parser.add_argument(
        "--allow_shorter", action="store_true", help="Don't require using all letters."
    )
    parser.add_argument(
        "--wildcard",
        action="store",
        const="?",
        nargs="?",
        help="Set a wildcard for the permutation matching (default: '?')",
    )
    parser.add_argument(
        "-r", "--regex", action="store_true", help="Print words matching regex."
    )

    args = parser.parse_args()

    print("Loading dictionary...", file=sys.stderr)
    words = load_dictionary(args.dictionary)

    if args.word:
        if not args.regex:
            words = filter_dictionary(
                words,
                args.word,
                prefix=args.prefix,
                wildcard=args.wildcard,
                use_all_letters=not args.allow_shorter,
            )
            print("Filtering dictionary...", file=sys.stderr)
            trie = None
            if args.allow_shorter or args.wildcard:
                print("Building trie...", file=sys.stderr)
                trie = build_trie(words)
        print("Done.", file=sys.stderr)
        answer(args.word, trie, words, args, is_filtered=True)
    else:
        print("Building trie...", file=sys.stderr)
        trie = build_trie(words)
        print("Done.", file=sys.stderr)
        try:
            while word := input(">>> "):
                answer(word, trie, words, args)
        except EOFError:
            pass


if __name__ == "__main__":
    main()
