import sosowa_requester
import sys

sr1 = sosowa_requester.sosowa_requester(sys.argv[1])

p = sr1.get_sosowa_product_list(50)

for k in p.keys():
    sr1.get_sosowa_article(p[k])
    p[k].show_detail()
    p[k].show_content()

