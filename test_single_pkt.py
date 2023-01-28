from unittest import TestCase, main

from remove_zeros import NalParser
from itertools import repeat


class TestZeroRemovalInSinglePacket(TestCase):
    def setUp(self):
        non_boundary_value_before_boundary = [4, 5, 6, 7]
        non_boundary_value_after_boundary = [8, 9, 10, 11]
        boundary_value = 0x00

        current_pkt = []
        current_pkt.extend(non_boundary_value_before_boundary)
        current_pkt.extend(repeat(boundary_value, 3))
        current_pkt.extend(non_boundary_value_after_boundary)

        self.current_pkt = current_pkt
        self.expected = []
        self.expected.append(non_boundary_value_before_boundary)
        self.expected.append(non_boundary_value_after_boundary)

        self.pkt_boundary_at_start = []
        self.pkt_boundary_at_start.extend(repeat(boundary_value, 3))
        self.pkt_boundary_at_start.extend(non_boundary_value_before_boundary)
        self.pkt_boundary_at_start.extend(non_boundary_value_after_boundary)
        self.pkt_boundary_at_start_expected = []
        self.pkt_boundary_at_start_expected.extend(
            non_boundary_value_before_boundary)
        self.pkt_boundary_at_start_expected.extend(
            non_boundary_value_after_boundary)

        self.pkt_boundary_at_start_and_middle = []
        self.pkt_boundary_at_start_and_middle.extend(repeat(boundary_value, 3))
        self.pkt_boundary_at_start_and_middle.extend(
            non_boundary_value_before_boundary)
        self.pkt_boundary_at_start_and_middle.extend(repeat(boundary_value, 3))
        self.pkt_boundary_at_start_and_middle.extend(
            non_boundary_value_after_boundary)
        self.pkt_boundary_at_start_and_middle_expected = []
        self.pkt_boundary_at_start_and_middle_expected.extend(
            [non_boundary_value_before_boundary])
        self.pkt_boundary_at_start_and_middle_expected.extend(
            [non_boundary_value_after_boundary])

        self.pkt_boundary_at_end = []
        self.pkt_boundary_at_end.extend(non_boundary_value_before_boundary)
        self.pkt_boundary_at_end.extend(non_boundary_value_after_boundary)
        self.pkt_boundary_at_end.extend(repeat(boundary_value, 3))
        self.pkt_boundary_at_end_expected = []
        self.pkt_boundary_at_end_expected.extend(
            non_boundary_value_before_boundary)
        self.pkt_boundary_at_end_expected.extend(
            non_boundary_value_after_boundary)

    def test_boundary_in_middle(self):
        input = self.current_pkt
        print(f'\nInput: {input}')
        nal_parser = NalParser()
        nal_parser.process_packet(input)
        output = nal_parser.pieces
        print(f'Output: {output}')
        self.assertEqual(output, self.expected)

    def test_boundary_at_start(self):
        input = self.pkt_boundary_at_start
        print(f'\nInput: {input}')
        nal_parser = NalParser()
        nal_parser.process_packet(self.pkt_boundary_at_start)
        output = nal_parser.pieces
        print(f'Output: {output}')
        self.assertEqual(output,
                         [self.pkt_boundary_at_start_expected])

    def test_boundary_at_start_and_middle(self):
        input = self.pkt_boundary_at_start_and_middle
        print(f'\nInput: {input}')
        nal_parser = NalParser()
        nal_parser.process_packet(input)
        output = nal_parser.pieces
        print(f'Output: {output}')
        self.assertEqual(output,
                         self.pkt_boundary_at_start_and_middle_expected)

    def test_boundary_at_end(self):
        """
        Won't test. The only time boundary can be at end is when it is a FU-A
        which is in the middle i.e. it does not have the end bit set. so we
        will always be fetching the next one before dealing with the zeros
        at the end of this pkt.

        This case is to be handled by multiple pkt flow.
        """
        pass


if __name__ == '__main__':
    main()
