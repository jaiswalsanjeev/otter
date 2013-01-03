""" CQL Batch wrapper test """
from twisted.trial.unittest import TestCase
from otter.util.cqlbatch import Batch
import mock
from twisted.internet import defer
from otter.test.utils import DeferredTestMixin


class CqlBatchTestCase(DeferredTestMixin, TestCase):
    """
    CQL Batch wrapper test case
    """

    def setUp(self):
        """
        setup
        """
        self.connection = mock.MagicMock()
        self.connection.execute.return_value = defer.succeed(None)

    def test_batch(self):
        """
        Test a simple batch
        """
        batch = Batch(['INSERT * INTO BLAH', 'INSERT * INTO BLOO'], {})
        d = batch.execute(self.connection)
        self.assert_deferred_succeeded(d)
        expected = 'BEGIN BATCH USING CONSISTENCY ONE INSERT * INTO BLAH'
        expected += ' INSERT * INTO BLOO APPLY BATCH;'
        self.connection.execute.assert_called_once_with(expected, {})

    def test_batch_param(self):
        """
        Test a simple batch with params
        """
        params = {"blah": "ff"}
        batch = Batch(['INSERT :blah INTO BLAH', 'INSERT * INTO BLOO'],
                      params)
        d = batch.execute(self.connection)
        self.assert_deferred_succeeded(d)
        expected = 'BEGIN BATCH USING CONSISTENCY ONE INSERT :blah INTO BLAH'
        expected += ' INSERT * INTO BLOO APPLY BATCH;'
        self.connection.execute.assert_called_once_with(expected, params)

    def test_batch_ts(self):
        """
        Test a simple batch with timestamp set
        """
        batch = Batch(['INSERT * INTO BLAH'], {}, timestamp=123)
        d = batch.execute(self.connection)
        self.assert_deferred_succeeded(d)
        expected = 'BEGIN BATCH USING CONSISTENCY ONE AND WITH TIMESTAMP 123'
        expected += ' INSERT * INTO BLAH APPLY BATCH;'
        self.connection.execute.assert_called_once_with(expected, {})

    def test_batch_consistency(self):
        """
        Test a simple batch with consistency set
        """
        batch = Batch(['INSERT * INTO BLAH'], {}, consistency='QUORUM')
        d = batch.execute(self.connection)
        self.assert_deferred_succeeded(d)
        expected = 'BEGIN BATCH USING CONSISTENCY QUORUM'
        expected += ' INSERT * INTO BLAH APPLY BATCH;'
        self.connection.execute.assert_called_once_with(expected, {})
