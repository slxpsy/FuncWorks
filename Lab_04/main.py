
from algorithms import (
    Node,
    bfs_level_order,
    fib,
    inorder,
    lcs_cache_info,
    lcs_length,
    postorder,
    preorder,
    quicksort,
)


def main() -> None:
    tree = Node(4, Node(2, Node(1), Node(3)), Node(6, None, Node(7)))
    print(f"Quicksort: {quicksort([7, 2, 5, 2, -1])}")
    print(f"Preorder: {list(preorder(tree))}")
    print(f"Inorder: {list(inorder(tree))}")
    print(f"Postorder: {list(postorder(tree))}")
    print(f"BFS: {bfs_level_order(tree)}")
    print(f"fib(30): {fib(30)}; cache: {fib.cache_info()}")
    print(f"LCS('рекурсія', 'курсор'): {lcs_length('рекурсія', 'курсор')}")
    print(f"LCS cache: {lcs_cache_info()}")


if __name__ == "__main__":
    main()
