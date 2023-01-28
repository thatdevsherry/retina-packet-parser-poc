from typing import List


class NalParser:
    pieces: List[int]
    count: int

    def __init__(self):
        self.pieces = []
        self.count = 0

    def process_packet(self, pkt: List[int]):
        finalized_pkt = pkt
        bytes_read = 0

        while bytes_read < len(pkt):
            pkt_to_iterate = finalized_pkt[-1] if type(
                finalized_pkt[0]) == list else finalized_pkt

            for idx, byte in enumerate(pkt_to_iterate):
                bytes_read += 1
                if self.count > 0 and self.count < 3 and byte != 0:
                    # reset counter if we went across a few zeros ( < 3 ).
                    self.count = 0
                if self.count >= 3 and byte != 0:
                    # we have reached the first non-boundary byte after a valid
                    # boundary. It's time to remove the boundary.
                    finalized_pkt = self.remove_boundaries(finalized_pkt, idx)
                    break
                if byte == 0:
                    self.count += 1

        if type(finalized_pkt[0]) == list:
            self.pieces.extend(finalized_pkt)
        else:
            self.pieces.extend([finalized_pkt])

    def remove_boundaries(
            self,
            current_pkt: List[int],
            index_after_boundary: int
    ) -> List[int]:
        pkt_start_till_boundary = current_pkt[:index_after_boundary]

        pkt_start_till_before_boundary = self._remove_zeros(
            pkt_start_till_boundary)
        output = None
        if pkt_start_till_before_boundary is None:
            output = current_pkt[index_after_boundary:]
        else:
            output = [pkt_start_till_before_boundary]
            output.append(
                current_pkt[index_after_boundary:])
        return output

    def _remove_zeros(self, pkt: List[int]) -> List[int] | None:
        """
        Returns `None` if zeros were at the start of pkt, otherwise it'll
        return the pkt after removing zeros in the middle.
        """
        pkt = list(reversed(pkt))
        for idx, byte in enumerate(pkt):
            if byte == 0:
                self.count -= 1
            elif byte != 0 and self.count == 0:
                return list(reversed(pkt[idx:]))

        # if we reach here, it means self.count is not zero
        # now, decrement self.count to zero
        if self.count == 0:
            return None

        updated_pieces = self._remove_zeros_from_last_piece()
        self.pieces.extend(updated_pieces)
        return None

    def _remove_zeros_from_last_piece(self):
        popper = [self.pieces.pop()]
        updated_pieces = []

        while len(popper) > 0:
            piece = popper.pop()
            pkt_with_partial_boundary_removed = self._remove_zeros(piece)
            updated_pieces.append(pkt_with_partial_boundary_removed)

            if self.count > 0:
                popper.append(self.pieces.pop())

        return updated_pieces
