# coding: utf-8
import unittest
from pytddmon import Monitor


class TestChangeDetection(unittest.TestCase):
    def _set_up_monitor(self):
        self.t_files = ['file']
        self.t_fsize = 1
        self.t_modtime = 1
        file_finder = lambda: self.t_files
        get_file_size = lambda x: self.t_fsize
        get_file_modification_time = lambda x: self.t_modtime
        monitor = Monitor(file_finder, get_file_size,
                          get_file_modification_time)
        return monitor

    def test_nothing_changed(self):
        monitor = self._set_up_monitor()
        change_detected = monitor.look_for_changes()
        self.assertFalse(change_detected)

    def test_modification_time_changed(self):
        monitor = self._set_up_monitor()
        self.t_modtime = 2
        change_detected = monitor.look_for_changes()
        self.assertTrue(change_detected)

    def test_adding_file(self):
        monitor = self._set_up_monitor()
        self.t_files.append('file2')
        change_detected = monitor.look_for_changes()
        self.assertTrue(change_detected)

    def test_renaming_file(self):
        monitor = self._set_up_monitor()
        self.t_files[0] = 'renamed'
        change_detected = monitor.look_for_changes()
        self.assertTrue(change_detected)

    def test_change_is_only_detected_once(self):
        monitor = self._set_up_monitor()
        self.t_files = 'changed'
        change_detected = monitor.look_for_changes()
        change_detected = monitor.look_for_changes()
        self.assertFalse(change_detected)

    def test_file_size_changed(self):
        monitor = self._set_up_monitor()
        self.t_fsize = 2
        change_detected = monitor.look_for_changes()
        self.assertTrue(change_detected)

    def test_file_order_does_not_matter(self):
        monitor = self._set_up_monitor()
        self.t_files = ['file', 'file2']
        change_detected = monitor.look_for_changes()
        self.t_files[:] = ['file2', 'file']
        change_detected = monitor.look_for_changes()
        self.assertFalse(change_detected)


if __name__ == '__main__':
    unittest.main()
