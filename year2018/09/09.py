class Node:
    """A node in a circular doubly-linked list."""

    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None


def part1(data):
    # Example values from your code:
    # 71657 for part 1, 71657 * 100 for part 2
    # In your code, you used 7165700 for part 2.
    marbles = 7165700
    players = 476

    # Initialize scores
    scores = [0] * players

    # Create the initial circular linked list of one node (value = 0)
    current = Node(0)
    current.next = current
    current.prev = current

    highest_score = 0
    player = 0

    for m in range(1, marbles + 1):
        # If marble is multiple of 23, do the "special" removal
        if m % 23 == 0:
            # Move 7 steps backward
            for _ in range(7):
                current = current.prev

            # Remove the node at 'current'
            removed_val = current.val

            # Link out the removed node
            left = current.prev
            right = current.next
            left.next = right
            right.prev = left

            # Add scores
            scores[player] += m + removed_val
            if scores[player] > highest_score:
                highest_score = scores[player]

            # Set the new current (the node after the removed one)
            current = right

        else:
            # Move 1 step forward
            current = current.next

            # Insert a new node (value = m) after current
            new_node = Node(m)
            right = current.next

            # Wire it in
            current.next = new_node
            new_node.prev = current
            new_node.next = right
            right.prev = new_node

            # The newly inserted node becomes 'current'
            current = new_node

        # Next player's turn
        player = (player + 1) % players

    return highest_score
