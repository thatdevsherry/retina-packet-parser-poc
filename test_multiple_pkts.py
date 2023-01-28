from unittest import TestCase, main

from remove_zeros import NalParser
from itertools import repeat


class TestZeroRemovalAcrossPackets(TestCase):
    def setUp(self):
        non_boundary_value_before_boundary = [4, 5, 6, 7]
        non_boundary_value_after_boundary = [8, 9, 10, 11]
        self.boundary_value = 0x00

        self.pkt_with_no_boundary = list(non_boundary_value_before_boundary)
        self.pkt_with_no_boundary.extend(non_boundary_value_after_boundary)

        current_pkt = []
        current_pkt.extend(repeat(self.boundary_value, 3))
        current_pkt.extend(non_boundary_value_before_boundary)
        current_pkt.extend(non_boundary_value_after_boundary)
        self.current_expected = []
        self.current_expected.extend(non_boundary_value_before_boundary)
        self.current_expected.extend(non_boundary_value_after_boundary)
        self.current_pkt = current_pkt
        pkt_with_boundary_at_start_and_in_middle = []
        pkt_with_boundary_at_start_and_in_middle.extend(
            repeat(self.boundary_value, 3))
        pkt_with_boundary_at_start_and_in_middle.extend(
            non_boundary_value_before_boundary)
        pkt_with_boundary_at_start_and_in_middle.extend(
            repeat(self.boundary_value, 3))
        pkt_with_boundary_at_start_and_in_middle.extend(
            non_boundary_value_after_boundary)
        self.pkt_with_boundary_at_start_and_in_middle = pkt_with_boundary_at_start_and_in_middle

        self.pkt_with_boundary_at_start_and_in_middle_expected = [
            self.pkt_with_no_boundary, list(
                reversed(
                    self.pkt_with_no_boundary
                )
            )
        ]
        self.pkt_with_boundary_at_start_and_in_middle_expected.append(
            non_boundary_value_before_boundary)
        self.pkt_with_boundary_at_start_and_in_middle_expected.append(
            non_boundary_value_after_boundary)

    def test_boundary_across_pkts(self):
        """
        Given packets in following format:
            [ [a], [b -  boundary], [boundary - c] ]

        Ensure output is:
               [ [a], [b], [c] ]

        Boundary is removed b/w packets
        """
        input = [self.pkt_with_no_boundary, list(reversed(
            self.pkt_with_no_boundary
        )) + [self.boundary_value] * 5, self.current_pkt]

        nal_parser = NalParser()

        for idx, i in enumerate(input):
            print(f'Input {idx+1}: {i}')
            nal_parser.process_packet(i)

        expected = [self.pkt_with_no_boundary, list(
            reversed(self.pkt_with_no_boundary)), self.current_expected]
        output = nal_parser.pieces
        print(f'Output: {output}')
        self.assertEqual(output, expected)

    def test_boundary_across_pkts_and_a_middle_boundary(self):
        """
        Given packets in following format:
            [ [a], [b -  boundary], [boundary - c - boundary - d] ]

        Ensure output is:
               [ [a], [b], [c], [d] ]

        Boundary is removed b/w packets as well as the middle boundary
        in the same packet.
        """
        input = [self.pkt_with_no_boundary, list(reversed(
            self.pkt_with_no_boundary
        )) + [self.boundary_value] * 5,
            self.pkt_with_boundary_at_start_and_in_middle]

        nal_parser = NalParser()

        for idx, i in enumerate(input):
            print(f'Input {idx+1}: {i}')
            nal_parser.process_packet(i)

        output = nal_parser.pieces
        expected = self.pkt_with_boundary_at_start_and_in_middle_expected
        print(f'Output: {output}')
        self.assertEqual(output, expected)


if __name__ == '__main__':
    main()
