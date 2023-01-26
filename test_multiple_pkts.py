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

    def test_boundary_across_pkts(self):
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


if __name__ == '__main__':
    main()
