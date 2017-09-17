import random
import unittest

import numpy as np

from fig_info import roll_with_new_data


class MyTest(unittest.TestCase):
    def test(self):
        chan = 5
        freq = 256
        events_in_view = 10
        total_events = int(freq * events_in_view)
        data = np.zeros((chan, total_events))
        # For a matrix with n rows and m columns, shape will be (n,m)
        print data.shape
        samples = []
        timestamps_from_sample = []

        for ii in range(0, 1024):
            events = []
            for jj in range(0, 5):
                events.append(1)
            samples.append(events)
            timestamps_from_sample.append(ii +1)
        print len(samples), len(samples[0])

        time_x = self.time = np.zeros(total_events)
        data, time_x = roll_with_new_data(data, samples, time_x, timestamps_from_sample)
        self.assertEqual(5, data.shape[0])
        self.assertEqual(total_events, data.shape[1])
        self.assertEqual(1, len(time_x.shape))
        self.assertEqual(total_events, time_x.shape[0])
        self.assertEqual(0., data[0, 0])
        self.assertEqual(0., data[0, total_events - 1024 - 1])
        self.assertEqual(1., data[0, total_events - 1024])
        self.assertEqual(1., data[4, total_events - 1024])

        self.assertEqual(0., time_x[total_events - 1024 -1])
        self.assertEqual(1., time_x[total_events - 1024 ])
        self.assertEqual(1024., time_x[-1])

