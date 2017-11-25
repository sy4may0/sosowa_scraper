import sosowa_requester
import sys

sr1 = sosowa_requester.sosowa_requester(sys.argv[1])

sr1.get_sosowa_product_list(217)
