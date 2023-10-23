import unittest
from invokerMultiRequest import InvokerMultiRequest
from invokerRequest import InvokerRequest

class TestInvokerMultiRequest(unittest.TestCase):
    def test_create(self):
        irs=[InvokerRequest(), InvokerRequest()]
        imr1=InvokerMultiRequest(irs,self,10)
        self.assertGreater(1000000000001,imr1.id)
    def test_invokers_count(self):
        irs=[InvokerRequest(), InvokerRequest()]
        imr1=InvokerMultiRequest(irs,self,10)
        self.assertEqual(imr1.invoker_requests_count,len(irs))
    def test_same_priority_queue(self):
        irs=[InvokerRequest(), InvokerRequest()]
        imr1=InvokerMultiRequest(irs,self,10)
        imr2=InvokerMultiRequest(irs,self,10)
        self.assertEqual(imr1.invoker_priority_queue, imr2.invoker_priority_queue)
    def test_unique(self):
        irs=[InvokerRequest(), InvokerRequest()]
        imr1=InvokerMultiRequest(irs,self,10)
        imr2=InvokerMultiRequest(irs,self,10)
        self.assertNotEqual(imr1.id, imr2.id)