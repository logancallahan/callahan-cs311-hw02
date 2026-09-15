"""
Homework 2: The Playlist Shuffler -- starter.

Complete CircularPlaylist below. See HW2_The_Playlist_Shuffler.md,
Part B, for the full requirements.
"""

from typing import List, Optional


class _SongNode:
    __slots__ = ("name", "next")

    def __init__(self, name: str) -> None:
        self.name = name
        self.next: Optional["_SongNode"] = None


class CircularPlaylist:
    def __init__(self) -> None:
        self._current: Optional[_SongNode] = None  # the "currently playing" node
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def add_song(self, name: str) -> None:
        """Insert `name` at the end of the circle (its next wraps back to the head)."""
        node = _SongNode(name)
        if self._current is None:
            node.next = node
            self._current = node
        else:
            tail = self._current
            while tail.next is not self._current:
                tail = tail.next
            node.next = self._current
            tail.next = node
        self._size += 1

    def skip_next(self) -> str:
        """Advance the currently-playing pointer to the next song and return its name."""
        if self._current is None:
            raise IndexError("Cannot skip a song in an empty playlist")
        self._current = self._current.next
        return self._current.name

    def remove_current(self) -> str:
        """
        Remove the currently-playing song, rewire the circle around it,
        advance to the next song, and return the name of the removed song.
        """
        current = self._current
        if current is None:
            raise IndexError("Cannot remove a song from an empty playlist")
        if current.next is current:
            self._current = None
        else:
            previous = current
            while previous.next is not current:
                previous = previous.next
            previous.next = current.next
            self._current = current.next
        self._size -= 1
        return current.name

    def elimination_shuffle(self, k: int) -> List[str]:
        """
        Repeatedly skip k-1 songs and remove the k-th (the Josephus
        pattern from Part A, Question 3), until one song remains.
        Return the removed songs in removal order, with the survivor
        as the final element of the list.
        """
        if k < 1:
            raise ValueError("k must be positive")
        current = self._current
        if current is None:
            return []

        removed: List[str] = []
        previous = current
        while previous.next is not current:
            previous = previous.next

        while self._size > 1:
            for _ in range((k - 1) % self._size):
                previous = current
                current = current.next
            removed.append(current.name)
            previous.next = current.next
            current = current.next
            self._size -= 1

        self._current = current
        removed.append(current.name)
        return removed
